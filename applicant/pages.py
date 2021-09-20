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
    form_fields = ['understanding1']


class DemographicSurvey(Page):
    form_model = 'player'
    form_fields = [
        'age', 'gender', 'education', 'resident'
    ]


class ASVABInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding2']


class ASVABQuestions(Page):
    form_model = 'player'
    form_fields = [f'q{i+1}' for i in range(20)]

    def before_next_page(self):
        player = self.player
        correct_answers = [
            2, 3, 0, 0,
            2, 3, 1, 2,
            0, 3, 3, 2,
            0, 3, 2, 2,
            3, 1, 0, 0
        ]
        eval_correct = 0
        noneval_correct = 0
        evqs = player.participant.vars['eval_qs']
        for i, q in enumerate([
            player.q1, player.q2, player.q3, player.q4,
            player.q5, player.q6, player.q7, player.q8,
            player.q9, player.q10, player.q11, player.q12,
            player.q13, player.q14, player.q15, player.q16,
            player.q17, player.q18, player.q19, player.q20
        ]):
            if i + 1 in evqs and q == qtext[f'q{i+1}'][correct_answers[i]]:
                eval_correct += 1
            elif q == qtext[f'q{i+1}'][correct_answers[i]]:
                noneval_correct += 1
        player.eval_correct = eval_correct
        player.noneval_correct = noneval_correct


class ApplicationInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding3']

    def vars_for_template(self):
        player = self.player
        stage1_bonus = f'{player.eval_correct * 10} cents' if player.eval_correct < 10 else '$1.00'
        return dict(stage1_bonus=stage1_bonus)


class Application(Page):
    form_model = 'player'
    form_fields = ['avatar', 'self_eval',
                   'self_eval_agree0', 'self_eval_agree1', 'self_eval_agree2',
                   'self_eval_statement']

    def vars_for_template(self):
        # get the real performance pdf from the prelim questions we do
        # it's just a filler right now
        perform_cdf = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]
        better_than = int(perform_cdf[self.player.eval_correct]*100)
        worse_than = 100 - better_than
        return dict(better_than=better_than, worse_than=worse_than)


class GuessInstructions(Page):
    form_model = 'player'
    form_fields = ['understanding4']


class WageGuess(Page):
    form_model = 'player'
    form_fields = ['wage_guess1', 'wage_guess2', 'wage_guess3', 'wage_guess_other']


class PerformanceGuess(Page):
    form_model = 'player'
    form_fields = ['perform_guess1', 'perform_guess2', 'perform_guess3', 'perform_guess_other']


class SocAppropGuess(Page):
    form_model = 'player'
    form_fields = ['approp_guess1', 'approp_guess2', 'approp_guess3', 'approp_guess_other']


class CompletionCode(Page):
    pass


page_sequence = [Captcha, ConsentForm, DemographicSurvey, Overview, ASVABInstructions,
                 ASVABQuestions, ApplicationInstructions, Application,
                 GuessInstructions, WageGuess, PerformanceGuess, SocAppropGuess, CompletionCode]
