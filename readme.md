# What is this?

This repository contains the files for the oTree-based web-app for a study on gender norms of self-promotion. There are two versions of the app contained in this folder. The first, `gender_norms`, is a basic version, while the second, `gender_norms_v2`, is the same thing with more questions added.

## How to run a demo of the app

To run the app, you need to have installed the latest version of oTree on your computer. If you already have Python, you can install oTree via pip with `pip install otree`.

Once you have oTree installed, you can launch a development server for the app by navigating to the project directory (the directory you have all the contents of this repository downloaded to) in a command line interface, then running `otree devserver`. You can then open the development interface in a web browser at `localhost:8000`.

From the development interface, you can launch either the `gender_norms` or `gender_norms_v2` version of the app for testing.

## How to deploy the app to be available on MTurk

The app should be hosted on a production server when the experiment is run. I currently have it hosted at <https://otree-uofu.herokuapp.com>. The interface is password-protected. If you want to create your own production server, oTree recommends using Heroku to make the process relatively simple; you can see instructions [here](https://github.com/oTree-org/otree-docs/blob/143a6ab7b61d54ec2be1a8bc09515d78e0b07c71/source/server/heroku.rst#heroku-setup-option-2).

If you have administrator access to the production server, you can launch the survey to be available to MTurk users in the Sessions tab.

*Note: depending on which version of the app you want to run, you will have to change the `participation_fee` variable in `settings.py` and the information in `_templates/global/mturk_template.html` to reflect the proper payments for the experiment. These changes must be made before deploying to the production server.*

I have also included Python scripts in the `interface` that will automatically create a session on the Heroku server, collect the responses received, and send payments to respondents. *You will need to have the Selenium package installed in Python along with its Chrome webdriver (on your system PATH) in order to automatically control the oTree interface, and Amazon's AWS CLI and Python boto3 package installed and properly configured for the code to work correctly.*
