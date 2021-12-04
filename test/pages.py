# from otree.api import Currency as c, currency_range
from ._builtin import Page

from .models import Constants
from captcha.fields import ReCaptchaField

import json

# load question text
with open("_static/global/question_text.json", "r", encoding="utf-8") as fh:
    qtext = json.load(fh)


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
    form_fields = ["age", "gender", "education", "employed"]


class Instructions(Page):
    form_model = "player"
    form_fields = ["understanding2", "understanding2_attempts"]


class ASVABQuestions(Page):
    form_model = "player"
    form_fields = [f"q{i+1}" for i in range(32)]

    def vars_for_template(self):
        return {"title": "ASVAB Questions"}

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


class ExitSurvey(Page):
    form_model = 'player'
    form_fields = ['study_topic_guess', 'male_avg_answers_guess', 'female_avg_answers_guess']

    def vars_for_template(self):
        total_bonus = f'{self.player.eval_correct * float(Constants.bonus_per_question) / 100:.2f}'
        return dict(total_bonus=total_bonus)


class CompletionCode(Page):
    form_model = 'player'


page_sequence = [
    Captcha,
    ConsentForm,
    DemographicSurvey,
    Instructions,
    ASVABQuestions,
    ExitSurvey,
    CompletionCode
]
