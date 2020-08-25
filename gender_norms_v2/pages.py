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


class DecisionScreen1a(Page):
    form_model = 'player'
    form_fields = ['match_guess_terrible', 'match_guess_very_poor', 'match_guess_neutral',
                   'match_guess_good', 'match_guess_very_good', 'match_guess_exceptional']

class DecisionScreen1b(Page):
    form_model = 'player'
    form_fields = ['match_guess_perform5', 'match_guess_perform25', 'match_guess_perform55',
                    'match_guess_perform75', 'match_guess_perform95']

class DecisionScreen1c(Page):
    form_model = 'player'
    form_fields = ['match_guess_succeed5', 'match_guess_succeed25', 'match_guess_succeed55',
                    'match_guess_succeed75', 'match_guess_succeed95']


class ExperimentInstructions2(Page):
    form_model = 'player'
    form_fields = ['understanding3']


class DecisionScreen2a(Page):
    form_model = 'player'
    form_fields = ['personal_terrible', 'personal_very_poor', 'personal_neutral',
                   'personal_good', 'personal_very_good', 'personal_exceptional']

class DecisionScreen2b(Page):
    form_model = 'player'
    form_fields = ['personal_perform5', 'personal_perform25', 'personal_perform55',
                    'personal_perform75', 'personal_perform95']

class DecisionScreen2c(Page):
    form_model = 'player'
    form_fields = ['personal_succeed5', 'personal_succeed25', 'personal_succeed55',
                    'personal_succeed75', 'personal_succeed95']


class DemographicSurvey(Page):
    pass

class CompletionCode(Page):
    pass

# TOOD: Reinsert Captcha
page_sequence = [ConsentForm, ExperimentInstructions, ExperimentInstructionsContd, SituationDescription,
                 DecisionScreen1a, DecisionScreen1b, DecisionScreen1c, ExperimentInstructions2,
                 DecisionScreen2a, DecisionScreen2b, DecisionScreen2c, DemographicSurvey, CompletionCode]
