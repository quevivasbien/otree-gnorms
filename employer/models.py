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
# load applicant data
with open('interface/interface_applicant.json', 'r') as fh:
    applicant_data = json.load(fh)



author = 'Mckay D Jensen'

doc = """
Gender norms of self-promotion
"""

# The number of employers to bid on each applicant
# This is double what we actually want since oTree automatically doubles things for mTurk studies
NUM_BIDDERS = 20


class Constants(BaseConstants):
    name_in_url = 'applicant'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        players = self.get_players()
        num_players = len(players)
        employer_indices = list(range(num_players))
        applicant_assignments = {j: [], for j in employer_indices}

        # helper function for assigning applicants to employers
        def add_applicant(applicant, employers):
            for j in employers:
                applicant_assignments[j].append(applicant)

        # Assign applicants to employers
        layer = 0
        for applicant in applicant_data:
            available_employers = [j for j in employer_indices if len(applicant_assignments[j]) == layer]
            if len(available_employers) < NUM_BIDDERS:
                num_first_assign = len(available_employers)
                add_applicant(applicant, available_employers)
                layer += 1
                add_applicant(applicant, sample(employer_indices, NUM_BIDDERS - num_first_assign))
            else:
                add_applicant(applicant, sample(employer_indices, NUM_BIDDERS))
        print([len(a) for a in applicant_assignments.values()])

        i = 0
        for j, p in zip(employer_indices, players):
            p.treatment = i
            i = (i + 1) % 3
            p.applicants = '-'.join(map(str, applicant_assignments[j]))
            p.applicant_ids = '-'.join(applicant_data[a]['mturk_assignment_id'] for a in applicant_assignments[j])
            p.participant.vars['gender'] = '-'.join(applicant_data[a]['gender'] for a in applicant_assignments[j])
            p.participant.vars['eval_correct'] = '-'.join(
                    applicant_data[a]['eval_correct'] for a in applicant_assignments[j
                )
            p.participant.vars['self_eval'] = '-'.join(applicant_data[a]['self_eval'] for a in applicant_assignments[j])
            p.bids = '-'.join(['0.0']*len(applicant_assignments[j]))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.IntegerField()
    applicants = models.StringField()
    bids = models.StringField()
    captcha = models.CharField(blank=True)
    understanding1a = models.StringField()
    understanding1b = models.StringField()
    age = models.IntegerField(min=0, max=120)
    gender = models.StringField(choices=['male', 'female'])

    def live_bid(self, data):
        current_tab = int(data['currentTab'])
        bid = str(data['bid'])
        bids_list = self.bids.split('-')
        bids_list[currentTab - 1] = bid
        self.bids = '-'.join(bids_list)
