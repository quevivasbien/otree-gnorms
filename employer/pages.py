# from otree.api import Currency as c, currency_range
from ._builtin import Page
# from .models import Constants
from captcha.fields import ReCaptchaField

import json

# load question text
with open('employer/static/employer/question_text.json', 'r') as fh:
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
    def vars_for_template(self):
        return dict(num_applicants=len(self.player.participant.vars['applicants']))


class DemographicSurvey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']

class BiddingPage(Page):
    form_model = 'player'
    live_method = 'live_bid'
    def vars_for_template(self):
        return dict(num_applicants=len(self.player.participant.vars['applicants']))

class CompletionCode(Page):
    pass


page_sequence = [Captcha, ConsentForm, Overview, DemographicSurvey, BiddingPage, CompletionCode]
