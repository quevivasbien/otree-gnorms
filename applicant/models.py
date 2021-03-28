from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    # Currency as c,
    # currency_range,
)
import json
from random import shuffle, sample


# load question text
with open('applicant/static/applicant/question_text.json', 'r') as fh:
    qtext = json.load(fh)



author = 'Mckay D Jensen'

doc = """
Gender norms of self-promotion
"""


class Constants(BaseConstants):
    name_in_url = 'applicant'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        i = 0
        for p in self.get_players():
            p.treatment = i
            question_order = list(range(1, 21))
            shuffle(question_order)
            p.question_order = '-'.join([str(x) for x in question_order])
            eval_qs = sample(question_order, 10)
            noneval_qs = [i for i in question_order if i not in eval_qs]
            p.participant.vars['eval_qs'] = eval_qs
            p.participant.vars['noneval_qs'] = noneval_qs
            i = (i + 1) % 3
            # TODO: Add assignment of asvab questions and which will be eval questions




class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.IntegerField()
    question_order = models.StringField()
    captcha = models.CharField(blank=True)
    understanding1 = models.StringField(choices=qtext['understanding1'], widget=widgets.RadioSelect)
    age = models.IntegerField(min=0, max=120)
    gender = models.StringField(choices=['male', 'female'])
    understanding2 = models.StringField(choices=qtext['understanding2'], widget=widgets.RadioSelect)
    q1 = models.StringField(choices=qtext['q1'], widget=widgets.RadioSelect)
    q2 = models.StringField(choices=qtext['q2'], widget=widgets.RadioSelect)
    q3 = models.StringField(choices=qtext['q3'], widget=widgets.RadioSelect)
    q4 = models.StringField(choices=qtext['q4'], widget=widgets.RadioSelect)
    eval_correct = models.IntegerField()
    noneval_correct = models.IntegerField()
    understanding3 = models.StringField(choices=qtext['understanding3'], widget=widgets.RadioSelect)
    self_eval = models.StringField(choices=qtext['self_eval'], widget=widgets.RadioSelect)
    wage_guess = models.FloatField()  # is a slider, managed via html&js


    def understanding1_error_message(self, value):
        if value != qtext['understanding1'][1]:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'

    def understanding2_error_message(self, value):
        if value != qtext['understanding2'][1]:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'

    def understanding3_error_message(self, value):
        if value != qtext['understanding3'][0]:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'
