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
# from botocore.exceptions import ClientError
import re

from interface import MTurkHandler

os.chdir(os.path.dirname(os.path.realpath(__file__)))


with open('config.json', 'r') as fh:
    config = json.load(fh)

# TODO: Change endpoint to None before deploying
ENDPOINT = config['endpoint'] if config['endpoint'] != 'None' else None
# TODO: Set this as the correct experiment size
EXPERIMENT_SIZE = config['experiment_size']
# TODO: Set this as the local downloads directory
DOWNLOAD_FOLDER = config['downloads']


class MTurkHandler_v2(MTurkHandler):

    def start_experiment(self):
        self.start_experiment_('Gender norms of self-promotion, with extra questions')

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
                            'exceptional': row['match_guess_exceptional'],
                            'perform5': row['match_guess_perform5'],
                            'perform25': row['match_guess_perform25'],
                            'perform55': row['match_guess_perform55'],
                            'perform75': row['match_guess_perform75'],
                            'perform95': row['match_guess_perform95'],
                            'succeed5': row['match_guess_succeed5'],
                            'succeed25': row['match_guess_succeed25'],
                            'succeed55': row['match_guess_succeed55'],
                            'succeed75': row['match_guess_succeed75'],
                            'succeed95': row['match_guess_succeed95']
                        }
                    else:
                        matching_responses = [
                            row['match_guess_terrible'] == last_resp.get('terrible'),
                            row['match_guess_very_poor'] == last_resp.get('very_poor'),
                            row['match_guess_neutral'] == last_resp.get('neutral'),
                            row['match_guess_good'] == last_resp.get('good'),
                            row['match_guess_very_good'] == last_resp.get('very_good'),
                            row['match_guess_exceptional'] == last_resp.get('exceptional'),
                            row['match_guess_perform5'] == last_resp.get('perform5'),
                            row['match_guess_perform25'] == last_resp.get('perform25'),
                            row['match_guess_perform55'] == last_resp.get('perform55'),
                            row['match_guess_perform75'] == last_resp.get('perform75'),
                            row['match_guess_perform95'] == last_resp.get('perform95'),
                            row['match_guess_succeed5'] == last_resp.get('succeed5'),
                            row['match_guess_succeed25'] == last_resp.get('succeed25'),
                            row['match_guess_succeed55'] == last_resp.get('succeed55'),
                            row['match_guess_succeed75'] == last_resp.get('succeed75'),
                            row['match_guess_succeed95'] == last_resp.get('succeed95')
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
        # mark as "close-dated" any responses that were submitted more than 20 hours ago
        close_dated = unapproved[unapproved['time_fetched'].apply(lambda x: now - x > 20 * 60 * 60)]
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
                row['match_guess_exceptional'] == comp['match_guess_exceptional'],
                row['match_guess_perform5'] == comp['match_guess_perform5'],
                row['match_guess_perform25'] == comp['match_guess_perform25'],
                row['match_guess_perform55'] == comp['match_guess_perform55'],
                row['match_guess_perform75'] == comp['match_guess_perform75'],
                row['match_guess_perform95'] == comp['match_guess_perform95'],
                row['match_guess_succeed5'] == comp['match_guess_succeed5'],
                row['match_guess_succeed25'] == comp['match_guess_succeed25'],
                row['match_guess_succeed55'] == comp['match_guess_succeed55'],
                row['match_guess_succeed75'] == comp['match_guess_succeed75'],
                row['match_guess_succeed95'] == comp['match_guess_succeed95']
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


def main(wait_interval=600, max_checks=1000):
    mTurkHandler = MTurkHandler_v2(start=True)  # starts experiment upon init
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
        print('Syntax is "python interface_v2.py [wait_interval] [max_checks]"')
