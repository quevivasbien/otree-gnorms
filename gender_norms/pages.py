# from otree.api import Currency as c, currency_range
from ._builtin import Page
# from .models import Constants
from captcha.fields import ReCaptchaField


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
    form_fields = ['understanding1a', 'understanding1b', 'understanding1c']


class ExperimentInstructionsContd(Page):
    form_model = 'player'
    form_fields = ['understanding2']


class SituationDescription(Page):
    pass


class DecisionScreen(Page):
    form_model = 'player'
    form_fields = ['match_guess_terrible', 'match_guess_very_poor', 'match_guess_neutral',
                   'match_guess_good', 'match_guess_very_good', 'match_guess_exceptional']


class ExperimentInstructions2(Page):
    form_model = 'player'
    form_fields = ['understanding3']


class DecisionScreen2(Page):
    form_model = 'player'
    form_fields = ['personal_terrible', 'personal_very_poor', 'personal_neutral',
                   'personal_good', 'personal_very_good', 'personal_exceptional']


class DemographicSurvey(Page):
    pass


page_sequence = [Captcha, ConsentForm, ExperimentInstructions, ExperimentInstructionsContd,
                 SituationDescription, DecisionScreen, ExperimentInstructions2, DecisionScreen2, DemographicSurvey]
