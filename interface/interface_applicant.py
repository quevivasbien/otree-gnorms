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

    def create_json(self, df):
        print(df.columns)
        dict_ = df[[
                'treatment',
                'gender',
                'eval_correct',
                'wage_guess',
                'self_eval',
                'mturk_assignment_id'
            ]].transpose().to_dict()
        with open('applicant_data.json', 'w') as fh:
            json.dump(dict_, fh)

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
        for i, row in to_review.iterrows():
            self.approve_hit(df.loc[i, 'mturk_assignment_id'], 'Your bonus payment will be sent soon.')
            df.loc[i, 'hit_approved'] = 1
        # bonuses will be sent out later
        df.to_csv(static_df)
        self.create_json(df[df['hit_approved'] == 1])



def main(wait_interval=600, max_checks=1000):
    mTurkHandler = ApplicantHandler(start=True)  # starts experiment upon init
    # make periodic checks to update data and approve tasks
    for _ in range(max_checks):
        print(f'Sleeping for {wait_interval} seconds...')
        time.sleep(wait_interval)
        mTurkHandler.check_progress()


# handler = ApplicantHandler()
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
