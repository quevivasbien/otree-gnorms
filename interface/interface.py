#!/usr/bin/env python3
"""Scripts for interacting with MTurk via AWS boto3 client
Check on hit status, send custom bonuses, etc.

Author: Mckay Jensen
"""

import os
import sys
import pandas as pd
import time
import boto3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO: Change endpoint to None before deploying
ENDPOINT = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# TODO: Change this to the correct experiment size before deploying
EXPERIMENT_SIZE = 10

DOWNLOAD_FOLDER = '/home/mckay/Descargas/'


class MTurkHandler:

    def __init__(self, endpoint_url=ENDPOINT, start=False):
        self.client = boto3.client('mturk', endpoint_url=endpoint_url)
        self.browser = webdriver.Chrome()
        if start:
            self.start_experiment()

    def login(self):
        username = self.browser.find_element_by_name('username')
        username.send_keys('admin')
        password = self.browser.find_element_by_name('password')
        password.send_keys('gendernorms271828')
        password.submit()

    def start_experiment(self):
        self.browser.get('https://otree-uofu.herokuapp.com/create_session/?is_mturk=1')
        try:
            session_config = Select(self.browser.find_element_by_name('session_config'))
        except NoSuchElementException:
            self.login()
            session_config = Select(self.browser.find_element_by_name('session_config'))
        session_config.select_by_visible_text('Gender norms of self-promotion')
        num_workers = self.browser.find_element_by_name('num_participants')
        num_workers.send_keys(str(EXPERIMENT_SIZE))
        create_button = self.browser.find_element_by_id('btn-create-session')
        create_button.click()
        if ENDPOINT is None:
            use_sandbox = self.browser.find_element_by_name('use_sandbox')
            use_sandbox.click()
        WebDriverWait(self.browser, 1)
        publish_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'btn-publish-hit'))
        )
        publish_button.click()
        self.session_code = self.browser.find_element_by_tag_name('code').text
        print(f'Started session {self.session_code}')

    def process_df(self, df, static_df=None):
        if static_df is None:
            static_df = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mturk_status_data.csv')
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
        # check for participants who did not complete the survey but submitted the HIT
        dont_approve = df[(df['hit_approved'] == 0) & (df['_index_in_pages'] != df['_max_page_index']) \
            & (pd.notna(df['mturk_assignment_id']))]
        for i, row in dont_approve.iterrows():
            try:
                self.client.reject_assignment(
                    AssignmentId=row['mturk_assignment_id'],
                    RequesterFeedback='Did not complete.'
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.reject_assignment(
                    AssignmentId=row['mturk_assignment_id'],
                    RequesterFeedback='Did not complete.'
                )
        dont_approve['hit_approved'] = -1
        # review completed but unapproved assignments
        bonuses = []
        to_review = df[df['hit_approved'] == 0]
        for name in to_review['name'].unique():
            for ability in to_review['ability'].unique():
                pair = 0
                last_idx = None
                last_resp = {}
                for i, row in to_review[(to_review['name'] == name) \
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
            try:
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'mturk_assignment_id']
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'mturk_assignment_id']
                )
            if bonus > 0:
                try:
                    self.client.send_bonus(
                        WorkerId=df.loc[i, 'mturk_worker_id'],
                        BonusAmount=f'{bonus:.2f}',
                        AssignmentId=df.loc[i, 'mturk_assignment_id'],
                        Reason=f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                    )
                except self.client.exceptions.ServiceFault:
                    time.wait(5)
                    self.client.send_bonus(
                        WorkerId=df.loc[i, 'mturk_worker_id'],
                        BonusAmount=f'{bonus:.2f}',
                        AssignmentId=df.loc[i, 'mturk_assignment_id'],
                        Reason=f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
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
            same_tt = df[(df['hit_approved'] == 1) \
                            & (df['name'] == row['name']) \
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
            try:
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'mturk_assignment_id']
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'mturk_assignment_id']
                )
            if bonus > 0:
                try:
                    self.client.send_bonus(
                        WorkerId=df.loc[i, 'mturk_worker_id'],
                        BonusAmount=f'{bonus:.2f}',
                        AssignmentId=df.loc[i, 'mturk_assignment_id'],
                        Reason=f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                    )
                except self.client.exceptions.ServiceFault:
                    time.wait(5)
                    self.client.send_bonus(
                        WorkerId=df.loc[i, 'mturk_worker_id'],
                        BonusAmount=f'{bonus:.2f}',
                        AssignmentId=df.loc[i, 'mturk_assignment_id'],
                        Reason=f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                    )
            df.loc[i, 'hit_approved'] = 1
            df.loc[i, 'bonus'] = bonus
        df.to_csv(static_df)


    def get_and_process_df(self, downloads_dir=DOWNLOAD_FOLDER):
        candidate_files = [f for f in os.listdir(downloads_dir) if 'all apps' in f.lower()]
        if not candidate_files:
            return False
        filename = os.path.join(downloads_dir, candidate_files[0])
        df = pd.read_csv(filename, index_col='participant.code')
        self.process_df(df)
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
