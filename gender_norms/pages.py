# from otree.api import Currency as c, currency_range
from ._builtin import Page
# from .models import Constants
# from captcha.fields import ReCaptchaField


# class Captcha(Page):
#     form_model = 'player'
#     form_fields = ['captcha']

#     def get_form(self, data=None, files=None, **kwargs):
#         frm = super().get_form(data, files, **kwargs)
#         frm.fields['captcha'] = ReCaptchaField(label='')
#         return frm


class ConsentForm(Page):
    pass


class ExperimentInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding1a', 'understanding1b', 'understanding1c']

    def error_message(self, values):
        """This is redundant! Form validation is now handled in JS <script> in ExperimentInstructions.html
        """
        incorrect = 0
        if values['understanding1a'] not in ['1.00', '1', '1.0', '1.000', 'one', '1,0', '1,00', '1.']:
            incorrect += 1
        if values['understanding1b'] not in ['1', 'one', '1.0', 'One', 'ONE']:
            incorrect += 1
        if values['understanding1c'] not in ['1.20', '1.2', '1,2', '1.200', '1,20']:
            incorrect += 1
        if incorrect > 0:
            num = 'One' if incorrect == 1 else 'Two' if incorrect == 2 else 'All'
            verb = 'is' if incorrect == 1 else 'are'
            return f'{num} of your answers {verb} incorrect. Please choose the correct answers to proceed.'


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

class CompletionCode(Page):
    pass


page_sequence = [ConsentForm, ExperimentInstructions, ExperimentInstructionsContd, SituationDescription,
                 DecisionScreen, ExperimentInstructions2, DecisionScreen2, DemographicSurvey, CompletionCode]
