#!/usr/bin/env python3
"""Scripts for interacting with MTurk via AWS boto3 client
Check on hit status, send custom bonuses, etc.

Author: Mckay Jensen
"""

import os
import sys
import json
import pandas as pd
import time
import boto3
# from botocore.exceptions import ClientError
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('config.json', 'r') as fh:
    config = json.load(fh)

# TODO: Change endpoint to None before deploying
ENDPOINT = config['endpoint'] if config['endpoint'] != 'None' else None
# TODO: Set this as the correct experiment size
EXPERIMENT_SIZE = config['experiment_size']
# TODO: Set this as the local downloads directory
DOWNLOAD_FOLDER = config['downloads']


class MTurkHandler:

    def __init__(self, endpoint_url=ENDPOINT, start=False):
        self.client = boto3.client('mturk', endpoint_url=endpoint_url, region_name='us-east-1')
        self.browser = webdriver.Chrome()
        self.hit_id = None
        if start:
            self.start_experiment()

    def login(self):
        username = self.browser.find_element_by_name('username')
        username.send_keys('admin')
        password = self.browser.find_element_by_name('password')
        password.send_keys(os.environ.get('OTREE_ADMIN_PASSWORD'))
        password.submit()

    def start_experiment_(self, experiment_name):
        hits_before = [x['HITId'] for x in self.client.list_hits()['HITs']]
        self.browser.get('https://otree-uofu.herokuapp.com/create_session/?is_mturk=1')
        try:
            session_config = Select(self.browser.find_element_by_name('session_config'))
        except NoSuchElementException:
            self.login()
            session_config = Select(self.browser.find_element_by_name('session_config'))
        session_config.select_by_visible_text(experiment_name)
        num_workers = self.browser.find_element_by_name('num_participants')
        num_workers.send_keys(str(EXPERIMENT_SIZE))
        create_button = self.browser.find_element_by_id('btn-create-session')
        create_button.click()
        if ENDPOINT is None:
            use_sandbox = self.browser.find_element_by_name('use_sandbox')
            use_sandbox.click()
        WebDriverWait(self.browser, 1)
        publish_button = WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located((By.ID, 'btn-publish-hit'))
        )
        publish_button.click()
        self.session_code = self.browser.find_element_by_tag_name('code').text
        print(f'Started session {self.session_code}')
        # Hacky way to get HIT ID of just-created HIT
        # (Let's be real, so much of this project is hacky...))
        time.sleep(1)  # wait a bit so the HIT has time to be posted
        hits_after = [x['HITId'] for x in self.client.list_hits()['HITs']]
        hits_diff = [x for x in hits_after if x not in hits_before]
        while len(hits_diff) != 1:
            # wait a bit more and try again
            time.sleep(1)
            hits_after = [x['HITId'] for x in self.client.list_hits()['HITs']]
            hits_diff = [x for x in hits_after if x not in hits_before]
        self.hit_id = hits_diff[0]

    def start_experiment(self):
        self.start_experiment_('Gender norms of self-promotion')

    def get_assignments_to_review(self):
        response = self.client.list_assignments_for_hit(
            HITId=self.hit_id,
            AssignmentStatuses=['Submitted']
        )
        assignments = response['Assignments']
        while response.get('NextToken'):
            response = self.client.list_assignments_for_hit(
                NextToken=response['NextToken'],
                HITId=self.hit_id,
                AssignmentStatuses=['Submitted']
            )
            assignments += response['Assignments']
        return assignments

    def reject_hit(self, assignment_id, feedback='', max_retry=1):
        try:
            self.client.reject_assignment(
                AssignmentId=assignment_id,
                RequesterFeedback=feedback
            )
        except self.client.exceptions.ServiceFault:
            print(f'ServiceFault when attempting to reject {assignment_id}')
            if max_retry > 0:
                print('Retrying in 5s...')
                time.wait(5)
                self.reject_hit(assignment_id, feedback, max_retry-1)

    def approve_hit(self, assignment_id, feedback='Thanks for participating!', max_retry=1):
        try:
            self.client.approve_assignment(
                AssignmentId=assignment_id,
                RequesterFeedback=feedback
            )
        except self.client.exceptions.ServiceFault:
            print(f'ServiceFault when attempting to approve {assignment_id}')
            if max_retry > 0:
                print('Retrying in 5s...')
                time.wait(5)
                self.approve_hit(assignment_id, feedback, max_retry-1)

    def send_bonus(self, worker_id, amount, assignment_id, reason='', max_retry=1):
        try:
            self.client.send_bonus(
                WorkerId=worker_id,
                BonusAmount=f'{amount:.2f}',
                AssignmentId=assignment_id,
                Reason=reason
            )
        except self.client.exceptions.ServiceFault:
            print(f'ServiceFault when attempting to send bonus for {assignment_id}')
            if max_retry > 0:
                print('Retrying in 5s...')
                time.wait(5)
                self.send_bonus(worker_id, amount, assignment_id, reason, max_retry-1)

    def process_df(self, df, static_df=None):
        if static_df is None:
            static_df = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gnorms_data.csv')
        # get rid of all the junk on the beginning of the column names
        df.rename(columns=lambda x: re.search(r'[^.]+$', x).group(), inplace=True)
        # drop problematic columns
        df.drop(columns=['label', 'payoff'], inplace=True)
        # drop empty rows
        df.dropna(subset=['mturk_assignment_id'], inplace=True)
        # add new columns for determining payoffs
        df['time_fetched'] = time.time()
        df['hit_approved'] = 0
        df['bonus'] = 0
        if os.path.isfile(static_df):
            df = pd.concat((pd.read_csv(static_df, index_col=0), df))
            df.sort_values(by=['time_started'], ascending=True, inplace=True)
            df = df[~df.index.duplicated(keep='first')]
        # get list of submitted assignments ready for review
        assignment_ids = [x['AssignmentId'] for x in self.get_assignments_to_review()]
        to_review = df[df['mturk_assignment_id'].isin(assignment_ids)]
        # check for participants who did not complete the survey but submitted the HIT
        dont_approve = to_review[to_review['_index_in_pages'] != to_review['_max_page_index']]
        for i, row in dont_approve.iterrows():
            self.reject_hit(row['mturk_assignment_id'], 'Did not complete.')
        dont_approve['hit_approved'] = -1
        # review completed but unapproved assignments
        bonuses = []
        to_review = df[to_review['hit_approved'] == 0]
        for name in to_review['name'].unique():
            for ability in to_review['ability'].unique():
                pair = 0
                last_idx = None
                last_resp = {}
                for i, row in to_review[(to_review['name'] == name)
                                        & (to_review['ability'] == ability)].iterrows():
                    if pair == 0:
                        last_idx = i
                        last_resp = {
                            'terrible': row['match_guess_terrible'],
                            'very_poor': row['match_guess_very_poor'],
                            'neutral': row['match_guess_neutral'],
                            'good': row['match_guess_good'],
                            'very_good': row['match_guess_very_good'],
                            'exceptional': row['match_guess_exceptional']
                        }
                    else:
                        matching_responses = [
                            row['match_guess_terrible'] == last_resp.get('terrible'),
                            row['match_guess_very_poor'] == last_resp.get('very_poor'),
                            row['match_guess_neutral'] == last_resp.get('neutral'),
                            row['match_guess_good'] == last_resp.get('good'),
                            row['match_guess_very_good'] == last_resp.get('very_good'),
                            row['match_guess_exceptional'] == last_resp.get('exceptional')
                        ]
                        bonus = 0.2 * sum(matching_responses)
                        bonuses.append((last_idx, bonus))
                        bonuses.append((i, bonus))
                    pair = (pair + 1) % 2
        for i, bonus in bonuses:
            self.approve_hit(df.loc[i, 'mturk_assignment_id'])
            if bonus > 0:
                self.send_bonus(
                    df.loc[i, 'mturk_worker_id'],
                    bonus,
                    df.loc[i, 'mturk_assignment_id'],
                    f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                )
            df.loc[i, 'hit_approved'] = 1
            df.loc[i, 'bonus'] = bonus
        # Check for unpaired responses about to expire
        unapproved = df[df['hit_approved'] == 0]
        now = time.time()
        # mark as "close-dated" any responses that were submitted more than 18 hours ago
        close_dated = unapproved[unapproved['time_fetched'].apply(lambda x: now - x > 18 * 60 * 60)]
        bonuses = []
        for i, row in close_dated.iterrows():
            # Find the most recent person who got the same treatment
            same_tt = df[(df['hit_approved'] == 1)
                         & (df['name'] == row['name'])
                         & (df['ability'] == row['ability'])]
            comp = same_tt.iloc[-1]
            matching_responses = [
                row['match_guess_terrible'] == comp['match_guess_terrible'],
                row['match_guess_very_poor'] == comp['match_guess_very_poor'],
                row['match_guess_neutral'] == comp['match_guess_neutral'],
                row['match_guess_good'] == comp['match_guess_good'],
                row['match_guess_very_good'] == comp['match_guess_very_good'],
                row['match_guess_exceptional'] == comp['match_guess_exceptional']
            ]
            bonus = 0.2 * sum(matching_responses)
            bonuses.append((i, bonus))
        for i, bonus in bonuses:
            self.approve_hit(df.loc[i, 'mturk_assignment_id'])
            if bonus > 0:
                self.send_bonus(
                    df.loc[i, 'mturk_worker_id'],
                    bonus,
                    df.loc[i, 'mturk_assignment_id'],
                    f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                )
            df.loc[i, 'hit_approved'] = 1
            df.loc[i, 'bonus'] = bonus
        df.to_csv(static_df)

    def get_and_process_df(self, downloads_dir=DOWNLOAD_FOLDER, static_df=None):
        candidate_files = [os.path.join(downloads_dir, f) \
                           for f in os.listdir(downloads_dir) if 'all_apps_wide' in f.lower()]
        if not candidate_files:
            return False
        filename = max(candidate_files, key=os.path.getctime)
        df = pd.read_csv(filename, index_col='participant.code')
        self.process_df(df, static_df)
        os.remove(filename)
        return True

    def check_progress(self):
        self.browser.get('https://otree-uofu.herokuapp.com/ExportSessionWide/{}/'.format(self.session_code))
        time.sleep(3)  # wait a few seconds to allow the file to download
        while not self.get_and_process_df():
            self.login()
            self.browser.get('https://otree-uofu.herokuapp.com/ExportSessionWide/{}/'.format(self.session_code))
            time.sleep(3)


def main(wait_interval=600, max_checks=1000):
    mTurkHandler = MTurkHandler(start=True)  # starts experiment upon init
    # make periodic checks to update data and approve tasks
    for _ in range(max_checks):
        print(f'Sleeping for {wait_interval} seconds...')
        time.sleep(wait_interval)
        mTurkHandler.check_progress()


# handler = MTurkHandler()
# handler.get_and_process_df()

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        main()
    elif len(args) == 2:
        main(int(args[1]))
    elif len(args) == 3:
        main(int(args[1]), int(args[2]))
    else:
        print('Syntax is "python interface.py [wait_interval] [max_checks]"')
