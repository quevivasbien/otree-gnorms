# from otree.api import Currency as c, currency_range
from ._builtin import Page
# from .models import Constants
from captcha.fields import ReCaptchaField

import json

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
    form_fields = ['understanding1a', 'understanding1b']


class DemographicSurvey(Page):
    form_model = 'player'
    form_fields = [
        'age', 'gender', 'education', 'employed', 'resident'
    ]


class BiddingPage(Page):
    form_model = 'player'
    live_method = 'live_bid'
    form_fields = ['bids']


class CompletionCode(Page):
    pass


page_sequence = [Captcha, ConsentForm, DemographicSurvey, Overview, BiddingPage, CompletionCode]
