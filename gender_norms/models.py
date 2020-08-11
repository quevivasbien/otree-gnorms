from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import json
from random import shuffle

with open('_static/gender_norms/question_text.json', 'r') as fh:
    qtext = json.load(fh)


author = 'Mckay D Jensen'

doc = """
Gender norms of self-promotion
"""


class Constants(BaseConstants):
    name_in_url = 'gender_norms'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    
    def creating_session(self):
        names = ['Greg', 'Emily']
        shuffle(names)
        abilities = [25, 50, 75]
        shuffle(abilities)
        eval_levels = ['terrible', 'very poor', 'neutral', 'good', 'very good', 'exceptional']
        shuffle(eval_levels)
        i = 0
        j = 0
        k = 0
        for p in self.get_players():
            name = names[i]
            p.name = name
            p.pronoun = 'he' if name == 'Greg' else 'she'
            p.pronoun_possessive = 'his' if name == 'Greg' else 'her'
            p.pronoun_object = 'him' if name == 'Greg' else 'her'
            p.ability = abilities[j]
            p.ability_comp = 100 - abilities[j]
            p.eval_level = eval_levels[k]
            # increment indices
            k = (k + 1) % len(eval_levels)
            if k == 0:
                j = (j + 1) % len(abilities)
                if j == 0:
                    i = (i + 1) % len(names)
                    


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()
    pronoun = models.StringField()
    pronoun_possessive = models.StringField()
    pronoun_object = models.StringField()
    ability = models.IntegerField()
    ability_comp = models.IntegerField()
    eval_level = models.StringField()
    captcha = models.CharField(blank=True)
    understanding1 = models.StringField(choices=qtext['understanding1'], widget=widgets.RadioSelect)
    understanding2 = models.StringField(choices=qtext['understanding2'], widget=widgets.RadioSelect)
    understanding3 = models.StringField(choices=qtext['understanding3'], widget=widgets.RadioSelect)
    match_guess = models.StringField(choices=qtext['appropriate_ratings'])
    personal_opinion = models.StringField(choices=qtext['appropriate_ratings'])
    
    def understanding1_error_message(self, value):
        if value != qtext['understanding1'][1]:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'
    
    def understanding2_error_message(self, value):
        if value != qtext['understanding2'][0]:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'
