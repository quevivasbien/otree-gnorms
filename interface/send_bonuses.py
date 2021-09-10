#!/usr/bin/env python3

import pandas as pd
import boto3
import random
import os


def run_auction(applicant_dict, bid_dict):
    all_applicants = set(sum(applicant_dict.values(), []))
    winners, winning_bids = {}, {}
    for applicant in all_applicants:
        winner = ''
        top_bid = -1
        tie = 1
        for bidder in applicant_dict.keys():
            if applicant in applicant_dict[bidder]:
                # get index and look up bid
                idx = applicant_dict[bidder].index(applicant)
                bid = bid_dict[bidder][idx]
                # determine if top bid
                # TODO: if we decide on second-price auction, change this
                if bid > top_bid:
                    winner = bidder
                    top_bid = bid
                    tie = 1
                elif bid == top_bid:
                    tie += 1
                    # resolve ties randomly
                    if random.random() < 1 / tie:
                        winner = bidder
        winners[applicant] = winner
        winning_bids[applicant] = top_bid
    return winners, winning_bids
    

class BonusResolver:
    
    def __init__(self, applicant_csv='applicant_data.csv', employer_csv='employer_data.csv'):
        self.app_df = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), applicant_csv),
                                  index_col=0)
        self.emp_df = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), employer_csv),
                                  index_col=0)
        
    def get_bonus(self, employer, applicant, winners, bid):
        if winners[applicant] == employer:
            return 1 - bid + 0.1 * self.app_df.at[applicant, 'noneval_correct']
        else:
            return 1

    def handle_wages(self, bonuses_per_employer=1):
        # first run the auctions to determine who hires whom
        applicants = dict(self.emp_df['applicants'].apply(lambda x: x.split('-')))
        bids = dict(self.emp_df['bids'].apply(lambda x: x.split('-')))
        # I'm going to treat each self-promotion type as a separate hire
        applicants_1 = {key: values[:10] for (key, values) in applicants.items()}
        applicants_2 = {key: values[10:20] for (key, values) in applicants.items()}
        applicants_3 = {key: values[20:] for (key, values) in applicants.items()}
        bids_1 = {key: values[:10] for (key, values) in bids.items()}
        bids_2 = {key: values[10:20] for (key, values) in bids.items()}
        bids_3 = {key: values[20:] for (key, values) in bids.items()}
        winners_1, winning_bids_1 = run_auction(applicants_1, bids_1)
        winners_2, winning_bids_2 = run_auction(applicants_2, bids_2)
        winners_3, winning_bids_3 = run_auction(applicants_3, bids_3)
        # record employer bonuses
        self.emp_df['bonus'] = 0
        for employer, row in self.emp_df.iterrows():
            for _ in range(bonuses_per_employer):
                i = random.randrange(0, 30)  # randomly select a bid, with replacement
                applicant = applicants[employer][i]
                bid = bids[employer][i]
                row['bonus'] += (self.get_bonus(employer, applicant, winners_1, bid) if i < 10
                                 else self.get_bonus(employer, applicant, winners_2, bid) if i < 20
                                 else self.get_bonus(employer, applicant, winners_3, bid))
        # record wages for applicants for each of the three self-promotion types
        self.app_df['wage_1'], self.app_df['wage_2'], self.app_df['wage_3'] = 0, 0, 0
        for applicant in self.app_df.index:
            self.app_df.at[applicant, 'wage_1'] = winning_bids_1[applicant]
            self.app_df.at[applicant, 'wage_2'] = winning_bids_2[applicant]
            self.app_df.at[applicant, 'wage_3'] = winning_bids_3[applicant]
        
    def get_applicant_bonuses(self):
        
            