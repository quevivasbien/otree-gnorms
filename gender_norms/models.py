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
from random import shuffle

with open('_static/gender_norms/question_text.json', 'r') as fh:
    qtext = json.load(fh)


author = 'Mckay D Jensen'

doc = """
Gender norms of self-promotion
"""


class Constants(BaseConstants):
    name_in_url = 'gnorms_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        names = ['Greg', 'Emily']
        shuffle(names)
        abilities = [25, 50, 75]
        scores = {25: 6, 50: 10, 75: 12}
        shuffle(abilities)
        i = 0
        j = 0
        for p in self.get_players():
            name = names[i]
            p.name = name
            p.pronoun = 'he' if name == 'Greg' else 'she'
            p.pronoun_possessive = 'his' if name == 'Greg' else 'her'
            p.pronoun_object = 'him' if name == 'Greg' else 'her'
            p.ability = abilities[j]
            p.ability_comp = 100 - abilities[j]
            p.ability_score = scores[abilities[j]]
            # increment indices
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
    ability_score = models.IntegerField()
    captcha = models.CharField(blank=True)
    understanding1a = models.StringField()
    understanding1b = models.StringField()
    understanding1c = models.StringField()
    understanding2 = models.StringField(choices=qtext['understanding2'], widget=widgets.RadioSelect)
    understanding3 = models.StringField()
    match_guess_terrible = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    match_guess_very_poor = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    # match_guess_poor = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    match_guess_neutral = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    match_guess_good = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    match_guess_very_good = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    match_guess_exceptional = models.StringField(choices=qtext['social_appropriate_ratings'], widget=widgets.RadioSelect)
    personal_terrible = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)
    personal_very_poor = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)
    # personal_poor = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)
    personal_neutral = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)
    personal_good = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)
    personal_very_good = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)
    personal_exceptional = models.StringField(choices=qtext['appropriate_ratings'], widget=widgets.RadioSelect)

    def understanding1a_error_message(self, value):
        if value not in ['1.00', '1', '1.0', '1.000', 'one', '1,0', '1,00', '1.']:
            return 'One of your answers was incorrect. Please choose the correct answers to proceed.'

    def understanding1b_error_message(self, value):
        if value not in ['3', 'three', '3.0']:
            return 'One of your answers was incorrect. Please choose the correct answers to proceed.'

    def understanding1c_error_message(self, value):
        if value not in ['1.20', '1.2', '1,2', '1.200', '1,20']:
            return 'One of your answers was incorrect. Please choose the correct answers to proceed.'

    def understanding2_error_message(self, value):
        if value != qtext['understanding2'][0]:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'

    def understanding3_error_message(self, value):
        if value.lower() != 'true':
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'
