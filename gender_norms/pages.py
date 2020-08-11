from otree.api import Currency as c, currency_range
from ._builtin import Page
from .models import Constants
from captcha.fields import ReCaptchaField

import json

with open('_static/gender_norms/question_text.json', 'r') as fh:
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


class ExperimentInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding1']


class ExperimentInstructionsContd(Page):
    form_model = 'player'
    form_fields = ['understanding2']
    

class SituationDescription(Page):
    pass


class DecisionScreen(Page):
    form_model = 'player'
    form_fields = ['match_guess', 'personal_opinion']


class DemographicSurvey(Page):
    pass


page_sequence = [Captcha, ConsentForm, ExperimentInstructions, ExperimentInstructionsContd,
                 SituationDescription, DecisionScreen, DemographicSurvey]
