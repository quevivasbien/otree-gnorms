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


class Overview(Page):
    form_model = 'player'
    form_fields = ['understanding1']


class DemographicSurvey(Page):
    # form_model = 'player'
    # form_fields = ['age', 'gender']
    pass


class ASVABInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding2']


class ASVABQuestions(Page):
    form_model = 'player'
    # answers are also on this page, but not in native otree


class Application(Page):
    form_model = 'player'
    form_fields = ['understanding3', 'self_eval']

class WageGuess(Page):
    form_model = 'player'
    form_fields = ['wage_guess']

class CompletionCode(Page):
    pass


page_sequence = [Captcha, ConsentForm, Overview, DemographicSurvey, ASVABInstructions,
                    ASVABQuestions, Application, WageGuess, CompletionCode]
