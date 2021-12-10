# from otree.api import Currency as c, currency_range
from ._builtin import Page

# from .models import Constants
from captcha.fields import ReCaptchaField

import json
import time
from random import randint, shuffle

# load question text
with open("_static/global/question_text.json", "r", encoding="utf-8") as fh:
    qtext = json.load(fh)

# load applicant data
with open("interface/applicant_data.json", "r", encoding="utf-8") as fh:
    applicant_data = json.load(fh)

# load constants
with open("_static/global/constants.json", "r", encoding="utf-8") as fh:
    constants = json.load(fh)


class Captcha(Page):
    form_model = "player"
    form_fields = ["captcha"]

    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields["captcha"] = ReCaptchaField(label="")
        return frm
    
    def before_next_page(self):
        self.player.time_start = int(time.time())


class ConsentForm(Page):
    pass


class DemographicSurvey(Page):
    form_model = "player"
    form_fields = ["age", "gender", "education", "employed"]

    def before_next_page(self):
        """Assign treatment based on response to gender question
        This is so treatments are more likely to be balanced by gender"""
        player = self.player
        sessionvars = self.session.vars
        playervars = player.participant.vars

        # Assign treatment based on gender
        if player.gender == "Male":
            treatment = sessionvars["male_idx"] % 3
            sessionvars["male_idx"] += 1
        elif player.gender == "Female":
            treatment = sessionvars["female_idx"] % 3
            sessionvars["female_idx"] += 1
        else:
            treatment = (sessionvars["male_idx"] + sessionvars["female_idx"]) % 3

        playervars["treatment"] = treatment
        playervars["apps_per_emp1"] = constants["apps_per_emp1"]
        playervars["apps_per_emp2"] = constants["apps_per_emp2"]
        playervars["apps_per_emp3"] = (
            constants["apps_per_emp3a"]
            if treatment == 0
            else constants["apps_per_emp3b"]
        )
        playervars["apps_per_emp"] = (
            playervars["apps_per_emp1"]
            + playervars["apps_per_emp2"]
            + playervars["apps_per_emp3"]
        )

        start_index = sessionvars["applicant_start_idxs"][treatment]
        applicant_ids = sessionvars["applicant_ids"]
        applicant_assignments = sessionvars["applicant_assignments"]

        idx = sessionvars["emp_idx"]

        for j in range(playervars["apps_per_emp"]):
            treatment_index = (start_index + j) % len(applicant_ids[treatment])
            if treatment_index == 0:
                # sample without replacement until all applicants exhausted, then resample
                shuffle(applicant_ids[treatment])
            applicant_assignments[idx].append(applicant_ids[treatment][treatment_index])

        player.applicants = "-".join(map(str, applicant_assignments[idx]))
        playervars["gender"] = "-".join(
            applicant_data[a]["gender"] for a in applicant_assignments[idx]
        )
        playervars["avatar"] = "-".join(
            applicant_data[a]["avatar"] for a in applicant_assignments[idx]
        )
        playervars["eval_correct"] = "-".join(
            str(applicant_data[a]["eval_correct"]) for a in applicant_assignments[idx]
        )
        playervars["eval_correct"] = "-".join(
            str(applicant_data[a]["eval_correct"]) for a in applicant_assignments[idx]
        )
        playervars["self_eval"] = "-".join(
            str(applicant_data[a]["self_eval"]) for a in applicant_assignments[idx]
        )
        playervars["self_eval_agree"] = "-".join(
            str(applicant_data[a]["self_eval_agree"])
            for a in applicant_assignments[idx]
        )
        playervars["self_eval_statement"] = "-".join(
            applicant_data[a]["self_eval_statement"] for a in applicant_assignments[idx]
        )

        sessionvars["emp_idx"] += 1
        sessionvars["applicant_start_idxs"][treatment] += playervars["apps_per_emp"]


class Overview(Page):
    form_model = "player"
    form_fields = ["understanding1", "understanding1_attempts"]


class BiddingInstructions1(Page):
    form_model = "player"
    form_fields = ["understanding2", "understanding2_attempts"]


class BiddingInstructions2(Page):
    form_model = "player"
    form_fields = ["understanding3", "understanding3_attempts"]


class BiddingPage(Page):
    form_model = "player"
    form_fields = ["bids"]


class PerformGuessInstructions(Page):
    form_model = "player"
    form_fields = ["understanding4", "understanding4_attempts"]


class PerformGuessPage(Page):
    form_model = "player"
    form_fields = ["perform_guesses"]


class SocAppropInstructions(Page):
    form_model = "player"
    form_fields = ["understanding5", "understanding5_attempts"]


class SocAppropPage(Page):
    form_model = "player"
    form_fields = ["soc_approp_ratings"]


class ExitSurvey(Page):
    form_model = "player"

    def vars_for_template(self):
        return {
            'perform_percentile': int(constants['perform_cdf'][self.player.exit_survey_perform] * 100)
        }

    def get_form_fields(self):
        fields = [
            'study_topic_guess',
            'male_avg_answers_guess',
            'female_avg_answers_guess'
        ]
        if self.participant.vars['treatment'] != 0:
            fields += [
                'male_enjoy_agree',
                'male_respect_agree',
                'male_approachable_agree',
                'male_interpersonal_agree',
                'male_recommend_agree',
                'male_confident_describe',
                'female_enjoy_agree',
                'female_respect_agree',
                'female_approachable_agree',
                'female_interpersonal_agree',
                'female_recommend_agree',
                'female_confident_describe'
            ]
        return fields
    
    def before_next_page(self):
        self.player.time_end = int(time.time())


class CompletionCode(Page):
    def vars_for_template(self):
        return {"completion_code": randint(1, 100) * 3}


page_sequence = [
    Captcha,
    ConsentForm,
    DemographicSurvey,
    Overview,
    BiddingInstructions1,
    BiddingInstructions2,
    BiddingPage,
    PerformGuessInstructions,
    PerformGuessPage,
    SocAppropInstructions,
    SocAppropPage,
    ExitSurvey,
    CompletionCode,
]
