#!/usr/bin/env python3
"""Scripts for interacting with MTurk via AWS boto3 client
Check on hit status, send custom bonuses, etc.

Author: Mckay Jensen
"""

from interface import MTurkHandler
import os
import sys
import json
import pandas as pd
import time
import re

with open("config.json", "r") as fh:
    config = json.load(fh)

# TODO: Change endpoint to None before deploying
ENDPOINT = config["endpoint"]
# TODO: Set this as the correct experiment size
EXPERIMENT_SIZE = config["experiment_size"]
# TODO: Set this as the local downloads directory
DOWNLOAD_FOLDER = config["downloads"]


class EmployerHandler(MTurkHandler):
    def start_experiment(self):
        self.start_experiment_("Employer")

    def process_df(self, df, static_df=None):
        if static_df is None:
            static_df = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "employer_data.csv"
            )
        # get rid of all the junk on the beginning of the column names
        df.rename(columns=lambda x: re.search(r"[^.]+$", x).group(), inplace=True)
        # drop problematic columns
        df.drop(columns=["label", "payoff"], inplace=True)
        # drop empty rows
        df.dropna(subset=["mturk_assignment_id"], inplace=True)
        # add new columns for determining payoffs
        df["time_fetched"] = time.time()
        df["hit_approved"] = 0
        if os.path.isfile(static_df):
            df = pd.concat((pd.read_csv(static_df, index_col=0), df))
            df.sort_values(
                by=["time_fetched", "time_started"], ascending=True, inplace=True
            )
            df = df[~df.index.duplicated(keep="last")]
        # get list of submitted assignments ready for review
        assignment_ids = [x["AssignmentId"] for x in self.get_assignments_to_review()]
        to_review = df.index[df["mturk_assignment_id"].isin(assignment_ids)]
        # check for participants who did not complete the survey but submitted the HIT, reject them
        dont_approve = to_review[
            df.loc[to_review, "_index_in_pages"] != df.loc[to_review, "_max_page_index"]
        ]
        for i in dont_approve:
            self.reject_hit(df.at[i, "mturk_assignment_id"], "Did not complete.")
        df.loc[dont_approve, "hit_approved"] = -1  # -1 indicates hit was rejected
        # review completed but unapproved assignments
        not_approved = df.index[df["hit_approved"] == 0]
        to_review = to_review.intersection(not_approved)
        for i in to_review:
            self.approve_hit(
                df.at[i, "mturk_assignment_id"], "Your bonus payment will be sent soon."
            )
        df.loc[to_review, "hit_approved"] = 1
        # bonuses will be sent out later
        df.to_csv(static_df)


def main(wait_interval=600, max_checks=1000):
    mTurkHandler = EmployerHandler(start=True)  # starts experiment upon init
    # make periodic checks to update data and approve tasks
    for _ in range(max_checks):
        print(f"Sleeping for {wait_interval} seconds...")
        time.sleep(wait_interval)
        mTurkHandler.check_progress()


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        main()
    elif len(args) == 2:
        main(int(args[1]))
    elif len(args) == 3:
        main(int(args[1]), int(args[2]))
    else:
        print('Syntax is "python interface_employer.py [wait_interval] [max_checks]"')
