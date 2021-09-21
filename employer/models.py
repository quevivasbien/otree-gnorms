from otree.api import (
    models,
    # widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    # Currency as c,
    # currency_range,
)
import json

from random import shuffle


# load question text
with open('_static/global/question_text.json', 'r', encoding='utf-8') as fh:
    qtext = json.load(fh)
# load applicant data
with open('interface/applicant_data.json', 'r', encoding='utf-8') as fh:
    applicant_data = json.load(fh)
# load constants
with open('_static/global/constants.json', 'r', encoding='utf-8') as fh:
    constants = json.load(fh)


author = 'Mckay D Jensen'

doc = """
Gender norms of self-promotion
"""

"""How to assign applicants to employers:
Want each employer to bid on 10*3 applicants,
so when assigning applicants to employers, can just loop through
applicant_data.json and assign 30 applicants to employer
"""

APPS_PER_EMP = 10*3


class Constants(BaseConstants):
    name_in_url = 'employer'
    players_per_group = None
    num_rounds = 1
    mean_performance = int(sum([x * i for i, x in enumerate(constants['perform_cdf'])]))


class Subsession(BaseSubsession):

    def creating_session(self):
        players = self.get_players()
        num_players = len(players)
        employer_indices = list(range(num_players))
        applicant_assignments = {j: [] for j in employer_indices}

        # divide applicants by treatment so we can give employers only one type of treatment
        applicant_ids = {0: [], 1: [], 2: []}
        for a in applicant_data.keys():
            applicant_ids[a['treatment']].append(a)
        # assign applicants to employers
        for i, emp_idx in enumerate(employer_indices):
            treatment = i % 3
            start_index = APPS_PER_EMP * (i // 3)
            for j in range(APPS_PER_EMP):
                treatment_index = (start_index + j) % len(applicant_ids[treatment])
                if treatment_index == 0:
                    # sample without replacement until all applicants exhausted, then resample
                    shuffle(applicant_ids[treatment])
                applicant_assignments[emp_idx].append(applicant_ids[treatment][treatment_index])
            players[i].participant.vars['treatment'] = treatment

        for j, p in zip(employer_indices, players):
            p.applicants = '-'.join(map(str, applicant_assignments[j]))
            p.participant.vars['gender'] = '-'.join(applicant_data[a]['gender'] for a in applicant_assignments[j])
            p.participant.vars['avatar'] = '-'.join(applicant_data[a]['avatar'] for a in applicant_assignments[j])
            p.participant.vars['eval_correct'] = '-'.join(
                    str(applicant_data[a]['eval_correct']) for a in applicant_assignments[j]
                )
            p.participant.vars['self_eval'] = '-'.join(applicant_data[a]['self_eval']
                                                       for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree0'] = '-'.join(str(applicant_data[a]['self_eval_agree0'])
                                                              for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree1'] = '-'.join(str(applicant_data[a]['self_eval_agree1'])
                                                              for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree2'] = '-'.join(str(applicant_data[a]['self_eval_agree2'])
                                                              for a in applicant_assignments[j])
            p.participant.vars['self_eval_statement'] = '-'.join(applicant_data[a]['self_eval_statement']
                                                                 for a in applicant_assignments[j])
            p.participant.vars['num_applicants'] = APPS_PER_EMP


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.IntegerField()
    applicants = models.StringField()
    bids = models.StringField()
    captcha = models.CharField(blank=True)
    understanding1 = models.StringField(choices=qtext['understanding1'])  # same as applicant's understanding1
    understanding2 = models.StringField()
    age = models.StringField(choices=qtext['age'])
    gender = models.StringField(choices=qtext['gender'])
    # ethnicity = models.StringField(choices=qtext['ethnicity'])
    # home_state = models.StringField(choices=qtext['home_state'])
    education = models.StringField(choices=qtext['education'])
    # married = models.StringField(choices=qtext['married'])
    # household_income = models.StringField(choices=qtext['household_income'])
    employed = models.StringField(choices=qtext['employed'])
    # religion = models.StringField(choices=qtext['religion'])
    # politics = models.StringField(choices=qtext['politics'])
    resident = models.StringField(choices=['Yes', 'No'])
