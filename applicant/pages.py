# from otree.api import Currency as c, currency_range
from ._builtin import Page

# from .models import Constants
from captcha.fields import ReCaptchaField

import json
import random


# load question text
with open("_static/global/question_text.json", "r", encoding="utf-8") as fh:
    qtext = json.load(fh)

with open("_static/global/constants.json", "r", encoding="utf-8") as fh:
    constants = json.load(fh)


class Captcha(Page):
    form_model = "player"
    form_fields = ["captcha"]

    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields["captcha"] = ReCaptchaField(label="")
        return frm


class ConsentForm(Page):
    pass


class DemographicSurvey(Page):
    form_model = "player"
    form_fields = ["age", "gender", "employed", "education", "resident"]

    def before_next_page(self):
        """Assign treatment based on response to gender question
        This is so treatments are more likely to be balanced by gender"""
        player = self.player
        if player.gender == "Male":
            player.treatment = self.session.vars["male_idx"] % 3
            self.session.vars["male_idx"] += 1
        elif player.gender == "Female":
            player.treatment = self.session.vars["female_idx"] % 3
            self.session.vars["female_idx"] += 1
        else:
            player.treatment = (
                self.session.vars["male_idx"] + self.session.vars["female_idx"]
            ) % 3

        # Also assign avatar
        gender = player.gender.lower()
        if gender not in ("male", "female"):
            gender = random.choice(("male", "female"))
        num = random.randint(1, 3)
        player.avatar = gender + str(num) + ".jpg"


class AvatarPage(Page):
    form_model = "player"


class Overview(Page):
    form_model = "player"
    form_fields = ["understanding1"]


class ASVABInstructions(Page):
    form_model = "player"
    form_fields = ["understanding2"]


class ASVABQuestions(Page):
    form_model = "player"
    form_fields = [f"q{i+1}" for i in range(32)]

    def vars_for_template(self):
        return {"title": "Part 1 of 4 - ASVAB Questions"}

    def before_next_page(self):
        # checks player's ASVAB answers and figures out how many are correct
        player = self.player
        correct_answers = [
            2,
            3,
            0,
            1,
            2,
            3,
            1,
            2,
            0,
            3,
            3,
            2,
            0,
            3,
            2,
            2,
            3,
            1,
            0,
            0,
            0,
            2,
            3,
            1,
            1,
            0,
            0,
            2,
            2,
            3,
            2,
            3,
        ]
        eval_correct = 0
        noneval_correct = 0
        evqs = player.participant.vars["eval_qs"]
        nevqs = player.participant.vars["noneval_qs"]
        for i, q in enumerate(
            [
                player.q1,
                player.q2,
                player.q3,
                player.q4,
                player.q5,
                player.q6,
                player.q7,
                player.q8,
                player.q9,
                player.q10,
                player.q11,
                player.q12,
                player.q13,
                player.q14,
                player.q15,
                player.q16,
                player.q17,
                player.q18,
                player.q19,
                player.q20,
                player.q21,
                player.q22,
                player.q23,
                player.q24,
                player.q25,
                player.q26,
                player.q27,
                player.q28,
                player.q29,
                player.q30,
                player.q31,
                player.q32,
            ]
        ):
            if i + 1 in evqs and q == qtext[f"q{i+1}"][correct_answers[i]]:
                eval_correct += 1
            elif i + 1 in nevqs and q == qtext[f"q{i+1}"][correct_answers[i]]:
                noneval_correct += 1
        player.eval_correct = eval_correct
        player.noneval_correct = noneval_correct


class ApplicationInstructions(Page):
    form_model = "player"
    form_fields = ["understanding3"]

    def vars_for_template(self):
        player = self.player
        stage1_bonus = "${:.2f}".format(
            player.eval_correct * constants["bonus_per_question"] / 100
        )
        return dict(stage1_bonus=stage1_bonus)


class Application(Page):
    form_model = "player"
    form_fields = ["self_eval", "self_eval_agree", "self_eval_statement"]

    def vars_for_template(self):
        perform_cdf = constants["perform_cdf"]
        better_than = int(perform_cdf[self.player.eval_correct] * 100)
        worse_than = 100 - better_than
        return dict(better_than=better_than, worse_than=worse_than)


class GuessInstructions(Page):
    form_model = "player"
    form_fields = ["understanding4"]


class WageGuess(Page):
    form_model = "player"
    form_fields = ["wage_guess1", "wage_guess2", "wage_guess3", "wage_guess_other"]

    def vars_for_template(self):
        perform_cdf = constants["perform_cdf"]
        better_than = int(perform_cdf[self.player.eval_correct] * 100)
        return dict(better_than=better_than)


class PerformanceGuess(Page):
    form_model = "player"
    form_fields = [
        "perform_guess1",
        "perform_guess2",
        "perform_guess3",
        "perform_guess_other",
    ]

    def vars_for_template(self):
        perform_cdf = constants["perform_cdf"]
        better_than = int(perform_cdf[self.player.eval_correct] * 100)
        return dict(better_than=better_than)

    def is_displayed(self):
        return self.player.show_perf_guess == 1


class SocAppropGuess(Page):
    form_model = "player"
    form_fields = [
        "approp_guess1",
        "approp_guess2",
        "approp_guess3",
        "approp_guess_other",
    ]

    def vars_for_template(self):
        perform_cdf = constants["perform_cdf"]
        better_than = int(perform_cdf[self.player.eval_correct] * 100)
        return dict(better_than=better_than)

    def is_displayed(self):
        return self.player.show_perf_guess == 0


class StudyTopic(Page):
    form_model = "player"
    form_fields = ["study_topic_guess"]


class CompletionCode(Page):
    pass


page_sequence = [
    Captcha,
    ConsentForm,
    DemographicSurvey,
    AvatarPage,
    Overview,
    ASVABInstructions,
    ASVABQuestions,
    ApplicationInstructions,
    Application,
    GuessInstructions,
    WageGuess,
    PerformanceGuess,
    SocAppropGuess,
    StudyTopic,
    CompletionCode,
]
