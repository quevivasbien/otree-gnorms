#!/usr/bin/env python3

import pandas as pd
import boto3
import random
import os
import json
import time

DRY_RUN = True

# load constants
with open("../_static/global/constants.json", "r", encoding="utf-8") as fh:
    constants = json.load(fh)

NBIDS = constants["apps_per_emp1"]
NBIDS_GUESSES = constants["apps_per_emp1"] + constants["apps_per_emp2"]

CLOSE_GUESS_PROXIMITY = constants["close_guess_proximity"] / 100
BONUS_PER_QUESTION = constants["bonus_per_question"] / 100

# retrieve question text
with open("../_static/global/question_text.json", "r", encoding="utf-8") as fh:
    qtext = json.load(fh)

# set up boto3 api client
with open("config.json", "r") as fh:
    # TODO: Change endpoint to None before deploying
    ENDPOINT = json.load(fh)["endpoint"]
client = boto3.client("mturk", endpoint_url=ENDPOINT, region_name="us-east-1")


def send_bonus(
    worker_id, amount, assignment_id, reason="", max_retry=1, dry_run=DRY_RUN
):
    if dry_run:
        print(f"Sending bonus of ${amount} to {worker_id}")
        return
    try:
        client.send_bonus(
            WorkerId=worker_id,
            BonusAmount=f"{amount:.2f}",
            AssignmentId=assignment_id,
            Reason=reason,
        )
    except client.exceptions.ServiceFault:
        print(f"ServiceFault when attempting to send bonus for {assignment_id}")
        if max_retry > 0:
            print("Retrying in 5s...")
            time.wait(5)
            send_bonus(worker_id, amount, assignment_id, reason, max_retry - 1)


# define some helper functions
def split_to_int(val):
    return [int(x) for x in val.split("-")]


def split_to_float(val):
    return [float(x) for x in val.split("-")]


def get_apps_by_type(applicants_str):
    applicants = applicants_str.split("-")
    return {
        "bids": applicants[:NBIDS],
        "perform_guesses": applicants[:NBIDS_GUESSES],
        "soc_approp_ratings": applicants[NBIDS_GUESSES:],
    }


class BonusResolver:
    def __init__(
        self, applicant_csv="applicant_data.csv", employer_csv="employer_data.csv"
    ):
        self.app_df = pd.read_csv(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), applicant_csv),
            index_col=0,
        )
        self.emp_df = pd.read_csv(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), employer_csv),
            index_col=0,
        )
        # emp_app_cwalk is the applicants evaluated by each employer
        self.emp_app_cwalk = dict(self.emp_df["applicants"].apply(get_apps_by_type))
        # emp_bid_cwalk is the bids from each employer
        self.emp_bid_cwalk = dict(self.emp_df["bids"].apply(split_to_float))
        # etc.
        self.emp_perform_guess_cwalk = dict(
            self.emp_df["perform_guesses"].apply(split_to_int)
        )
        self.emp_soc_approp_cwalk = dict(
            self.emp_df["soc_approp_ratings"].apply(split_to_int)
        )
        # app_bid_cwalk is the bids for each applicant
        # figure out bids for each applicant, need to keep track of which profile version they're for
        self.app_bid_cwalk = {app: ([], [], []) for app in self.app_df.index}
        self.app_perform_cwalk = {app: ([], [], []) for app in self.app_df.index}
        self.app_approp_cwalk = {app: ([], [], []) for app in self.app_df.index}
        for emp in self.emp_df.index:
            for i, (app, bid, perform_guess, soc_approp) in enumerate(
                zip(
                    self.emp_app_cwalk[emp],
                    self.emp_bid_cwalk[emp],
                    self.emp_perform_guess_cwalk[emp],
                    self.emp_soc_approp_cwalk[emp],
                )
            ):
                promote_type = 0 if i < NBIDS else 1 if i < NBIDS_GUESSES else 2
                self.app_bid_cwalk[app][promote_type].append(bid)
                self.app_perform_cwalk[app][promote_type].append(perform_guess)
                self.app_approp_cwalk[app][promote_type].append(soc_approp)

        # index all applicants by promotion values
        sp_types = []
        for app, row in self.app_df.iterrows():
            gender = row["gender"]
            treatment = row["treatment"]
            sp1 = qtext["self_eval"].index(row["self_eval"])
            sp2 = row["self_eval_agree"]
            sp3 = qtext["self_eval_statement"].index(row["self_eval_statement"])
            sp_types.append((gender, treatment, sp1, sp2, sp3))
        sp_types = pd.MultiIndex.from_tuples(sp_types)
        # a bit backward, we want the index of the sp_types Series to be the type, actual value is the applicant id
        # this makes it fast to sort through self-promote types later
        self.sp_types = pd.Series(data=self.app_df.index, index=sp_types)

    def get_employer_bonuses(self, bonuses_per_employer=1):
        bonuses = {emp: 0.0 for emp in self.emp_df.index}
        # For each employer, loop through applicants and bids
        for employer in self.emp_df.index:
            # choose a random applicants for each bonus
            app_for_bid_bonus = random.choice(self.emp_app_cwalk["bids"])
            app_for_guess_bonus = random.choice(self.emp_app_cwalk["perform_guesses"])
            app_for_soc_approp_bonus = random.choice(
                self.emp_app_cwalk["soc_approp_ratings"]
            )
            # compute bid bonus
            bid = self.emp_bid_cwalk[employer][app_for_bid_bonus]
            p = random.randint(0, constants["bonus_per_question"] * 10) / 100
            if p < bid:
                # "option A"
                bonuses[employer] += (
                    BONUS_PER_QUESTION
                    * self.app_df.at[app_for_bid_bonus, "noneval_correct"]
                )
            else:
                # "option B"
                bonuses[employer] += p
            # compute perform guess bonus
            guess = self.emp_perform_guess_cwalk[employer][app_for_guess_bonus]
            if abs(guess - self.app_df.at[app_for_guess_bonus, "noneval_correct"]) <= 1:
                bonuses[employer] += constants["bonus_per_part"]
            # compute social appropriateness guess bonus
            guess = self.emp_soc_approp_cwalk[employer][app_for_soc_approp_bonus]
            other_employer_guess = random.choice(self.emp_df["soc_approp_ratings"])
            if guess == other_employer_guess:
                bonuses[employer] += constants["bonus_per_part"]
        # record bonuses in dataframe
        self.emp_df["bonus"] = pd.Series(bonuses)

    def get_guess_to_compare(self, applicant, guess_type="wage"):
        promote_types = self.app_df.at[applicant, "wage_guess_promote_type"].split("-")
        n_other = len(promote_types)
        other_applicant = ""
        promote_type = 0
        guess = 0.0
        # decide whether to do one of the self guesses or try one of the other guesses
        if random.random() <= n_other / (n_other + 3):
            # try other guess
            gender = self.app_df.at[applicant, "wage_guess_gender"].split("-")
            treatment = split_to_int(self.app_df.at[applicant, "wage_guess_treatment"])
            promote1 = split_to_int(self.app_df.at[applicant, "wage_guess_promote1"])
            promote2 = split_to_int(self.app_df.at[applicant, "wage_guess_promote2"])
            promote3 = self.app_df.at[applicant, "wage_guess_promote3"].split("-")
            order = list(range(n_other))
            random.shuffle(order)
            for i in order:
                # look for someone with that type of promotion
                if promote_types[i] == 0:
                    candidates = self.sp_types.loc[gender, treatment, promote1, :, :]
                elif promote_types[i] == 1:
                    candidates = self.sp_types.loc[gender, treatment, :, promote2, :]
                else:
                    candidates = self.sp_types.loc[gender, treatment, :, :, promote3]
                if len(candidates) > 0:
                    other_applicant = random.choice(candidates)
                    promote_type = promote_types[i]
                    guess = split_to_float(
                        self.app_df.at[applicant, f"{guess_type}_guess_other"]
                    )[i]
                    break
        if not other_applicant:
            # try self guess
            other_applicant = applicant
            promote_type = random.randrange(3)
            guess = self.app_df.at[
                applicant,
                (
                    f"{guess_type}_guess1",
                    f"{guess_type}_guess2",
                    f"{guess_type}_guess3",
                )[promote_type],
            ]
        return guess, other_applicant, promote_type

    def get_wage_guess_bonus(self, applicant):
        wage_guess, other_applicant, promote_type = self.get_guess_to_compare(
            applicant, "wage"
        )
        # look up highest wage for selected applicant in selected treatment
        wage = max(self.app_bid_cwalk[other_applicant][promote_type])
        # give bonus if applicant's guess within close guess proximity
        if abs(wage - wage_guess) <= CLOSE_GUESS_PROXIMITY:
            return constants["bonus_per_part"]
        else:
            return 0.0

    def get_perf_guess_bonus(self, applicant):
        perform_guess, other_applicant, promote_type = self.get_guess_to_compare(
            applicant, "perform"
        )
        # randomly select an employer's performance guess for this applicant
        other_guess = random.choice(
            self.app_perform_cwalk[other_applicant][promote_type]
        )
        if abs(perform_guess - other_guess) <= 1:
            return constants["bonus_per_part"]
        else:
            return 0.0

    def get_approp_guess_bonus(self, applicant):
        approp_guess, other_applicant, promote_type = self.get_guess_to_compare(
            applicant, "approp"
        )
        # randomly select an employer's approp guess for this applicant
        other_guess = random.choice(
            self.app_approp_cwalk[other_applicant][promote_type]
        )
        if approp_guess == other_guess:
            return constants["bonus_per_part"]
        else:
            return 0.0

    def get_applicant_bonuses(self):
        self.app_df["bonus"] = 0.0
        # loop through applicants & add up bonuses for each stage
        for applicant in self.app_df.index:
            bonus = 0.0
            # stage 0 is score on job performance questions
            bonus += BONUS_PER_QUESTION * self.app_df.at[applicant, "noneval_correct"]
            # stage 1 is a randomly selected bid on a version of the application
            bonus += random.choice(sum(self.app_bid_cwalk[applicant], []))
            # stage 2 is the paid if wage guess is with 10 cents of random employer
            bonus += self.get_wage_guess_bonus(applicant)
            # stage 3/4 is performance / social approp guesses
            if self.app_df.at[applicant, "show_perf_guess"]:
                bonus += self.get_perf_guess_bonus(applicant)
            else:
                bonus += self.get_approp_guess_bonus(applicant)
            self.app_df.at[applicant, "bonus"] = bonus

    def send_bonuses(self):
        for _, row in self.app_df.iterrows():
            send_bonus(
                row["mturk_worker_id"],
                row["bonus"],
                row["mturk_assignment_id"],
                "Participation bonus",
            )
        for _, row in self.emp_df.iterrows():
            send_bonus(
                row["mturk_worker_id"],
                row["bonus"],
                row["mturk_assignment_id"],
                "Participation bonus",
            )


if __name__ == "__main__":
    br = BonusResolver()
    br.get_employer_bonuses()
    br.get_applicant_bonuses()
    br.send_bonuses()
