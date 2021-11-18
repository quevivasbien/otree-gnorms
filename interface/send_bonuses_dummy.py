#!/usr/bin/env python3

import pandas as pd

from send_bonuses import BONUS_PER_QUESTION, send_bonus

DRY_RUN = True


def main():
    df = pd.read_csv("dummy_data.csv", index_col=0)
    for idx, row in df.iterrows():
        amt_correct = row["noneval_correct"]
        bonus = amt_correct * BONUS_PER_QUESTION
        send_bonus(
            row["mturk_worker_id"],
            bonus,
            row["mturk_assignment_id"],
            f"Bonus for answering {amt_correct} of the bonus questions correctly",
        )


if __name__ == "__main__":
    main()
