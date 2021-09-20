#!/usr/bin/env python3

import pandas as pd
# import boto3
import random
import os
import json

# TODO: update these values
BONUS_PER_QUESTION = 0.1
CLOSE_GUESS_PROXIMITY = 0.05
BONUS_FOR_CLOSE_guess1 = 1.0
WAGE_BIDS_PER_GROUP = 10

# retrieve question text
with open('../_static/global/question_text.json') as fh:
    qtext = json.load(fh)

# set up boto3 api client
with open('config.json', 'r') as fh:
    # TODO: Change endpoint to None before deploying
    ENDPOINT = json.load(fh)['endpoint']
client = boto3.client('mturk', endpoint_url=ENDPOINT, region_name='us-east-1')

def send_bonus(worker_id, amount, assignment_id, reason='', max_retry=1):
    try:
        client.send_bonus(
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
            send_bonus(worker_id, amount, assignment_id, reason, max_retry-1)
    
# define a couple of helper functions
def split_to_int(val):
    return [int(x) for x in val.split('-')]

def split_to_float(val):
    return [float(x) for x in val.split('-')]
    

class BonusResolver:

    def __init__(self, applicant_csv='applicant_data.csv', employer_csv='employer_data.csv'):
        self.app_df = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), applicant_csv),
                                  index_col=0)
        self.emp_df = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), employer_csv),
                                  index_col=0)
        self.emp_app_cwalk = dict(self.emp_df['applicants'].apply(lambda x: x.split('-')))
        self.emp_bid_cwalk = dict(self.emp_df['bids'].apply(split_to_float))
        # figure out bids for each applicant, need to keep track of which profile version they're for
        self.app_bid_cwalk = {app: ([], [], []) for app in self.app_df.index}
        for emp in self.emp_df.index:
            for i, (app, bid) in enumerate(zip(self.emp_app_cwalk[emp], self.emp_bid_cwalk[emp])):
                self.app_bid_cwalk[app][i // WAGE_BIDS_PER_GROUP].append(bid)
        # index all applicants by promotion values
        sp_types = []
        for app, row in self.app_df.iterrows():
            gender = row['gender']
            treatment = row['treatment']
            sp1 = qtext['self_eval'].index(row['self_eval'])
            sp2a = row['self_eval_agree0']
            sp2b = row['self_eval_agree1']
            sp2c = row['self_eval_agree2']
            sp3 = qtext['self_eval_statement'].index(row['self_eval_statement'])
            sp_types.append((gender, treatment, sp1, sp2a, sp2b, sp2c, sp3))
        sp_types = pd.MultiIndex.from_tuples(sp_types)
        # a bit backward, we want the index of the sp_types Series to be the type, actual value is the applicant id
        # this makes it fast to sort through self-promote types later
        self.sp_types = pd.Series(data=self.app_df.index, index=sp_types)
                

    def get_employer_bonuses(self, bonuses_per_employer=1):
        bonuses = {emp: 1.0 for emp in self.emp_df.index}
        # For each employer, loop through applicants and bids
        for employer in self.emp_df.index:
            for _ in range(bonuses_per_employer):
                # choose a random applicant that the employer bid on
                i = random.randrange(WAGE_BIDS_PER_GROUP * 3)
                applicant = self.emp_app_cwalk[employer][i]
                bid = self.emp_bid_cwalk[employer][i]
                # generate a random value `p` in [0,1]. If bid is >= p, hire for price p
                p = random.random()
                if bid >= p:
                    bonuses[employer] -= round(p, 2)
                    # adjust bonus based on performance of hired applicant
                    bonuses[employer] += 0.1 * self.app_df.at[applicant, 'noneval_correct']
        # record bonuses in dataframe
        self.emp_df['bonus'] = pd.Series(bonuses)

    def get_wage_guess_bonus(self, applicant):
        promote_types = self.app_df.at[applicant, 'wage_guess_promote_type'].split('-')
        n_other = len(promote_types)
        other_applicant = ''
        promote_type = 0
        wage_guess1 = 0.0
        # decide whether to do one of the self guesses or try one of the other guesses
        if random.random() <= n_other / (n_other + 3):
            # try other guess
            gender = self.app_df.at[applicant, 'wage_guess_gender'].split('-')
            treatment = split_to_int(self.app_df.at[applicant, 'wage_guess_treatment'])
            promote1 = split_to_int(self.app_df.at[applicant, 'wage_guess_promote1'])
            promote2a = split_to_int(self.app_df.at[applicant, 'wage_guess_promote1'])
            promote2b = split_to_int(self.app_df.at[applicant, 'wage_guess_promote1'])
            promote2c = split_to_int(self.app_df.at[applicant, 'wage_guess_promote1'])
            promote3 = split_to_int(self.app_df.at[applicant, 'wage_guess_promote1'])
            order = list(range(n_other))
            random.shuffle(order)
            for i in order:
                # look for someone with that type of promotion
                if promote_types[i] == 0:
                    candidates = self.sp_types.loc[gender, treatment, promote1, :, :, :, :]
                elif promote_types[i] == 1:
                    candidates = self.sp_types.loc[gender, treatment, :, promote2a, promote2b, promote2c, :]
                else:
                    candidates = self.sp_types.loc[gender, treatment, :, :, :, :, promote3]
                if len(candidates) > 0:
                    other_applicant = candidates.sample(1)[0]
                    promote_type = promote_types[i]
                    wage_guess1 = split_to_float(self.app_df.at[applicant, 'wage_guess_other'])[i]
                    break
        if not other_applicant:
            # try self guess
            other_applicant = applicant
            promote_type = random.randrange(3)
            wage_guess1 = self.app_df.at[applicant, ('wage_guess1', 'wage_guess2', 'wage_guess3')[promote_type]]
        # look up highest wage for selected applicant in selected treatment
        wage = max(self.app_bid_cwalk[other_applicant][promote_type])
        # give bonus if applicant's guess within CLOSE_GUESS_PROXIIMITY
        if abs(wage - wage_guess1) <= CLOSE_GUESS_PROXIMITY:
            return BONUS_FOR_CLOSE_guess1
        else:
            return 0.0

    def get_applicant_bonuses(self):
        self.app_df['bonus'] = 0.0
        # loop through applicants & randomly choose stage to pay bonus on
        for applicant in self.app_df.index:
            stage = random.randrange(3)
            # stage 0 is score on job performance questions
            # stage 1 is a randomly selected bid on a version of the application : change this?
            # stage 2
            if stage == 0:
                self.app_df.at[applicant, 'bonus'] = BONUS_PER_QUESTION * self.app_df.at[applicant, 'noneval_correct']
            elif stage == 1:
                self.app_df.at[applicant, 'bonus'] = random.choice(sum(self.app_bid_cwalk[applicant], []))
            elif stage == 2:
                self.app_df.at[applicant, 'bonus'] = self.get_wage_guess_bonus(applicant)
    
    def send_bonuses(self):
        for _, row in self.app_df.iterrows():
            send_bonus(row['mturk_worker_id'], row['bonus'], row['mturk_assignment_id'], 'Participation bonus')
        for _, row in self.emp_df.iterrows():
            send_bonus(row['mturk_worker_id'], row['bonus'], row['mturk_assignment_id'], 'Participation bonus')
            

if __name__ == '__main__':
    br = BonusResolver()
    br.get_employer_bonuses()
    br.get_applicant_bonuses()
    br.send_bonuses()
