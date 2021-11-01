# from otree.api import Currency as c, currency_range
from ._builtin import Page
# from .models import Constants
from captcha.fields import ReCaptchaField

import json
from random import randint

# load question text
with open('_static/global/question_text.json', 'r', encoding='utf-8') as fh:
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
    form_fields = [
        'age', 'gender', 'education', 'employed', 'resident'
    ]


class BiddingInstructions1(Page):
    form_model = 'player'
    form_fields = ['understanding2']


class BiddingInstructions2(Page):
    form_model = 'player'
    form_fields = ['understanding3a', 'understanding3b']


class BiddingPage(Page):
    form_model = 'player'
    form_fields = ['bids']


class PerformGuessInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding4']


class PerformGuessPage(Page):
    form_model = 'player'
    form_fields = ['perform_guesses']


class SocAppropInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding5']


class SocAppropPage(Page):
    form_model = 'player'
    form_fields = ['soc_approp_ratings']


class CompletionCode(Page):
    def vars_for_template(self):
        return {'completion_code': randint(1, 100) * 3}


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
    CompletionCode
]
