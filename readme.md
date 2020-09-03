# What is this?

This repository contains the files for the oTree-based web-app for a study on gender norms of self-promotion. There are two versions of the app contained in this folder. The first, `gender_norms`, is a basic version, while the second, `gender_norms_v2`, is the same thing with more questions added.

## How the project is structured

The project is structured like a normal oTree project; you can read the details on [the oTree documentation](https://otree.readthedocs.io/en/latest/index.html).

I've included a basic description of where everything is and what it does below (some files and folders are excluded because they're automatically generated by oTree and not edited by me).

* `_static` Contains files that are used by both the apps, e.g., the image in the example ASFAB questions
* `_templates` Contains a `Page.html` document that the other templates in the project are based on, as well as an `mturk_template.html` document, which is displayed to workers on MTurk before they are directed to the survey.
* `gender_norms`
 * `static` Contains JavaScript and CSS files that are referenced in the HTML documents in `templates` and are used to change how the pages of the app look and behave in the web browser.
 * `templates` Contains HTML documents that tell the web browser how to display each page. There is a document for each page, labeled by their names given in `pages.py`. This is where the real meat of the app is -- these files define what you actually see on screen. Most of the HTML documents contain Javascript code that gives the pages additional interactivity that isn't built into oTree.
 * `models.py` Defines all the variables associated with each participant and assigns participants to treatment groups.
 * `pages.py` Defines the pages in the experiment, including the variables (e.g., question responses) that are accessible on those pages, and tells oTree what order to display the pages in.
* `gender_norms_v2` Structured the same as `gender_norms`, but has more pages and more variables
* `interface` Contains Python code for automatically running the experiment on the Heroku server, approving HITs, and sending payments. These are meant to be executed locally: although they interact with the server, they do not run *on* the server.
 * `interface.py` Automatically runs an experiment with the `gender_norms` version of the app.
 * `interface.py` Does the same thing as `interface.py`, but with the `gender_norms_v2` version of the app.
* `requirements_base.txt` Tells the server which Python packages are needed to run the app properly.
* `settings.py` Contains settings, including the experiment's participation fee and the qualification requirements for MTurk workers meant to take the survey.


To run the app, you need to have installed the latest version of oTree on your computer. If you already have Python, you can install oTree via pip with `pip install otree`.

Once you have oTree installed, you can launch a development server for the app by navigating to the project directory (the directory you have all the contents of this repository downloaded to) in a command line interface, then running `otree devserver`. You can then open the development interface in a web browser at `localhost:8000`.

From the development interface, you can launch either the `gender_norms` or `gender_norms_v2` version of the app for testing.

## How to deploy the app to be available on MTurk

The app should be hosted on a production server when the experiment is run. I currently have it hosted at <https://otree-uofu.herokuapp.com>. The interface is password-protected. If you want to create your own production server, oTree recommends using Heroku to make the process relatively simple; you can see instructions [here](https://github.com/oTree-org/otree-docs/blob/143a6ab7b61d54ec2be1a8bc09515d78e0b07c71/source/server/heroku.rst#heroku-setup-option-2).

If you have administrator access to the production server, you can launch the survey to be available to MTurk users in the Sessions tab.

**Note: depending on which version of the app you want to run, you will have to change the `participation_fee` variable in `settings.py` and the information in `_templates/global/mturk_template.html` to reflect the proper payments for the experiment. These changes must be made before deploying to the production server.**

I have also included Python scripts in the `interface` that will automatically create a session on the Heroku server, collect the responses received, and send payments to respondents. **You will need to have the Selenium package installed in Python along with its Chrome webdriver (on your system PATH) in order to automatically control the oTree interface, and Amazon's AWS CLI and Python boto3 package installed and properly configured for the code to work correctly.**
