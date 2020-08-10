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

from random import sample


author = 'Mckay Jensen'

doc = """
Your app description
"""

questions = 'prefsranker/questions.json'
INIT_SCORE = 1500    



class Constants(BaseConstants):
    name_in_url = 'stackranker'
    players_per_group = None
    num_rounds = 5
    with open(questions) as fp:
        qdict = json.load(fp)
    
    def construct_option_string(option):
        if option['category'] == 'an extra year of life':
            return '{0} of {1}, {2}'.format(
                    option['modifiers']['risk_aversion'],
                    option['category'],
                    option['modifiers']['altruism']
                    )
        else:
            return '{0} of {1} {2}, {3}'.format(
                    option['modifiers']['risk_aversion'],
                    option['category'],
                    option['modifiers']['time_discount'],
                    option['modifiers']['altruism']
                    )
    
    all_options = set()
    categories = qdict['categories']
    modifiers = qdict['modifiers']
    for category in categories:
        for risk_aversion in modifiers['risk_aversion']:
            for time_discount in modifiers['time_discount']:
                for altruism in modifiers['altruism']:
                    all_options.add(construct_option_string(
                            {
                                'category': category,
                                'modifiers': {
                                                'risk_aversion': risk_aversion,
                                                'time_discount': time_discount,
                                                'altruism': altruism
                                        }
                                    }
                            ))

    
class Subsession(BaseSubsession):
    
    def creating_session(self):
        # Runs only on first session. Initializes preferences dict.
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['preferences'] = {
                            option: INIT_SCORE for option in Constants.all_options
                        }
        # Runs whenever new session is created. Chooses options to compare in that session.
            # TODO: Make this depend on current vals of the player's preferences dict
        # Although I think this runs all at the beginning, so that might not work...
        for p in self.get_players():
            p.pick_choice1, p.pick_choice2 = tuple(sample(Constants.all_options, 2))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    pick_choice1 = models.StringField()
    pick_choice2 = models.StringField()
    your_pick = models.StringField(widget=widgets.RadioSelect)
    
    def your_pick_choices(self):
        # For now just randomly select
        return [self.pick_choice1, self.pick_choice2]