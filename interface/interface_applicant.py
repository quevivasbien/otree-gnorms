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
from botocore.exceptions import ClientError
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('config.json', 'r') as fh:
    config = json.load(fh)

# TODO: Change endpoint to None before deploying
ENDPOINT = config['endpoint']
# TODO: Set this as the correct experiment size
EXPERIMENT_SIZE = config['experiment_size']
# TODO: Set this as the local downloads directory
DOWNLOAD_FOLDER = config['downloads']

from interface import MTurkHandler


class ApplicantHandler(MTurkHandler):

    def start_experiment(self):
        self.start_experiment_('Applicant side of part 2')

    def process_df(self, df, static_df=None):
        if static_df is None:
            static_df = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'applicant_data.csv')
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
        # approve completed but unapproved assignments
        to_review = df[df['hit_approved'] == 0]
        for i, row in to_review.iterrows():
            try:
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'mturk_assignment_id'],
                    RequesterFeedback='Your bonus payment will be sent soon.'
                )
            except self.client.exceptions.ServiceFault:
                time.wait(5)
                self.client.approve_assignment(
                    AssignmentId=df.loc[i, 'mturk_assignment_id'],
                    RequesterFeedback='Your bonus payment will be sent soon.'
                )
            except ClientError:  # worker has not yet submitted HIT
                continue
            df.loc[i, 'hit_approved'] = 1
        # bonuses will be sent out later
        df.to_csv(static_df)



def main(wait_interval=600, max_checks=1000):
    mTurkHandler = ApplicantHandler(start=True)  # starts experiment upon init
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
        print('Syntax is "python interface_applicant.py [wait_interval] [max_checks]"')
