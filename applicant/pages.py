# from otree.api import Currency as c, currency_range
from ._builtin import Page
# from .models import Constants
from captcha.fields import ReCaptchaField

import json

# load question text
with open('applicant/static/applicant/question_text.json', 'r') as fh:
    qtext = json.load(fh)


class Captcha(Page):
    form_model = 'player'
    form_fields = ['captcha']

    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields['captcha'] = ReCaptchaField(label='')
        return frm


class ConsentForm(Page):
    pass


class Overview(Page):
    form_model = 'player'
    form_fields = ['understanding1']


class DemographicSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class ASVABInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding2']


class ASVABQuestions(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']
    def before_next_page(self):
        player = self.player
        eval_correct = 0
        noneval_correct = 0
        evqs = player.participant.vars['eval_qs']
        if 1 in evqs and player.q1 == qtext['q1'][1]:
            eval_correct += 1
        elif player.q1 == qtext['q1'][1]:
            noneval_correct += 1
        if 2 in evqs and player.q2 == qtext['q2'][3]:
            eval_correct += 1
        elif player.q2 == qtext['q2'][3]:
            noneval_correct += 1
        if 3 in evqs and player.q3 == qtext['q3'][2]:
            eval_correct += 1
        elif player.q3 == qtext['q3'][2]:
            noneval_correct += 1
        if 4 in evqs and player.q4 == qtext['q4'][2]:
            eval_correct += 1
        elif player.q4 == qtext['q4'][2]:
            noneval_correct += 1
        player.eval_correct = eval_correct
        player.noneval_correct = noneval_correct


class ApplicationInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding3']


class Application(Page):
    form_model = 'player'
    form_fields = ['self_eval']

class WageGuess(Page):
    form_model = 'player'
    form_fields = ['wage_guess']

class CompletionCode(Page):
    pass


page_sequence = [Captcha, ConsentForm, Overview, DemographicSurvey, ASVABInstructions,
                    ASVABQuestions, Application, WageGuess, CompletionCode]
