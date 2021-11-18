#!/usr/bin/env python3

from interface_applicant import ApplicantHandler
import json
import time
import sys

with open("config.json", "r") as fh:
    config = json.load(fh)

# TODO: Change endpoint to None before deploying
ENDPOINT = config["endpoint"]
# TODO: Set this as the correct experiment size
EXPERIMENT_SIZE = config["experiment_size"]
# TODO: Set this as the local downloads directory
DOWNLOAD_FOLDER = config["downloads"]

CSV_NAME = "dummy_data.csv"
JSON_NAME = "dummy_data.json"


class DummyHandler(ApplicantHandler):
    def start_experiment(self):
        self.start_experiment_("Test to establish performance distribution")


def main(wait_interval=600, max_checks=1000):
    mTurkHandler = DummyHandler(start=True)  # starts experiment upon init
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
        print('Syntax is "python interface_dummy.py [wait_interval] [max_checks]"')
