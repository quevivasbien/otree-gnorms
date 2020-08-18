#!/usr/bin/env python3
"""Scripts for interacting with MTurk via AWS boto3 client
Check on hit status, send custom bonuses, etc.

Author: Mckay Jensen
"""



client = boto3.client('mturk', endpoint_url=ENDPOINT)

client.list_hits()
client.list_assignments_for_hit(HITId='311HQEI8RSE3KZIHUX3GXTGKYTZZ7O')

client.get_assignment(AssignmentId='3C2NJ6JBKBF43T5MBZGTVZNJFZRN24')

import os
import sys
import pandas as pd
import time
import boto3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

type(client)

# TODO: Change endpoint before deploying
ENDPOINT = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# TODO: Change this to the correct experiment size before deploying
EXPERIMENT_SIZE = 10


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
        num_workers.submit()

    def process_df(self, df, static_df=os.path.join(__file__, 'mturk_status_data.csv')):
        df['time_fetched'] = time.time()
        df['hit_approved'] = 0
        if os.path.isfile(static_df):
            df = pd.concat(
                    (pd.read_csv(static_df), df)
            ).drop_duplicates(subset=['participant.code'], keep='first').reset_index(drop=True)
        # check for participants who did not complete the survey but submitted the HIT
        dont_approve = df[(df['hit_approved'] == 0) & (df['participant._index_in_pages'] != df['participant._max_page_index']) \
            & (pd.notna(df['participant.mturk_assignment_id']))]
        for i, row in dont_approve.iterrows():
            try:
                self.client.reject_assignment(
                    AssignmentId=row['participant.mturk_assignment_id'],
                    RequesterFeedback='Did not complete.'
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.reject_assignment(
                    AssignmentId=row['participant.mturk_assignment_id'],
                    RequesterFeedback='Did not complete.'
                )
        dont_approve['hit_approved'] = -1
        # review completed but unapproved assignments
        bonuses = []
        to_review = df[df['hit_approved'] == 0]
        for name in to_review['gender_norms.1.player.name'].unique():
            for ability in to_review['gender_norms.1.player.ability'].unique():
                pair = 0
                last_idx = None
                last_resp = {}
                for i, row in to_review[(to_review['gender_norms.1.player.name'] == name) \
                                        & (to_review['gender_norms.1.player.ability'] == ability)]:
                    if pair == 0:
                        last_idx = i
                        last_resp = {
                            'terrible': row['gender_norms.1.player.match_guess_terrible'],
                            'very_poor': row['gender_norms.1.player.match_guess_very_poor'],
                            'neutral': row['gender_norms.1.player.match_guess_neutral'],
                            'good': row['gender_norms.1.player.match_guess_good'],
                            'very_good': row['gender_norms.1.player.match_guess_very_good'],
                            'exceptional': row['gender_norms.1.player.match_guess_exceptional']
                        }
                    else:
                        bonus = 0
                        if row['gender_norms.1.player.match_guess_terrible'] == last_resp.get('terrible'):
                            bonus += 0.2
                        if row['gender_norms.1.player.match_guess_very_poor'] == last_resp.get('very_poor'):
                            bonus += 0.2
                        if row['gender_norms.1.player.match_guess_neutral'] == last_resp.get('neutral'):
                            bonus += 0.2
                        if row['gender_norms.1.player.match_guess_good'] == last_resp.get('good'):
                            bonus += 0.2
                        if row['gender_norms.1.player.match_guess_very_good'] == last_resp.get('very_good'):
                            bonus += 0.2
                        if row['gender_norms.1.player.match_guess_exceptional'] == last_resp.get('exceptional'):
                            bonus += 0.2
                        bonuses.append((last_idx, bonus))
                        bonuses.append((i, bonus))
                    pair = (pair + 1) % 2
        for i, bonus in bonuses:
            # TODO: be robust to MTurk.Client.exceptions.ServiceFault exception
            try:
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'participant.mturk_assignment_id']
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'participant.mturk_assignment_id']
                )
            try:
                self.client.send_bonus(
                    WorkerId=df.loc[i, 'participant.mturk_worker_id'],
                    BonusAmount=f'{bonus:.2f}',
                    AssignmentId=df.loc[i, 'participant.mturk_assignment_id'],
                    Reason=f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.send_bonus(
                    WorkerId=df.loc[i, 'participant.mturk_worker_id'],
                    BonusAmount=f'{bonus:.2f}',
                    AssignmentId=df.loc[i, 'participant.mturk_assignment_id'],
                    Reason=f'Bonus for answering {int(bonus / 0.2)} questions the same as your match.'
                )
            df.loc[i, 'hit_approved'] = 1
        # TODO: Check for unpaired responses about to expire


    def get_and_process_df(self, downloads_dir='~/Descargas'):
        candidate_files = [f for f in os.listdir(downloads_dir) if 'all apps' in f.lower()]
        if not candidate_files:
            return False
        filename = os.path.join(downloads_dir, candidate_files[0])
        df = pd.read_csv(filename)
        os.remove(filename)
        self.process_df(df)
        return True

    def check_progress(self):
        self.browser.get('https://otree-uofu.herokuapp.com/ExportSessionWide/{}/'.format(self.session_code))
        while not self.get_and_process_df():
            self.login()
            self.browser.get('https://otree-uofu.herokuapp.com/ExportSessionWide/{}/'.format(self.session_code))



def main(wait_interval=600, max_checks=100):
    mTurkHandler = MTurkHandler(start=True)  # starts experiment upon init
    # make periodic checks to update data and approve tasks
    for _ in range(max_checks):
        time.sleep(wait_interval)
        mTurkHandler.check_progress()



if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        main()
    elif len(args) == 2:
        main(args[1])
    elif len(args) == 3:
        main(args[1], args[2])
    else:
        print('Syntax is "python aws.py [wait_interval] [max_checks]"')
