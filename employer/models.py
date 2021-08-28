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


# load question text
with open('applicant/static/applicant/question_text.json', 'r', encoding='utf-8') as fh:
    qtext = json.load(fh)
# load applicant data
with open('interface/applicant_data.json', 'r', encoding='utf-8') as fh:
    applicant_data = json.load(fh)


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


class Subsession(BaseSubsession):

    def creating_session(self):
        players = self.get_players()
        num_players = len(players)
        employer_indices = list(range(num_players))
        applicant_assignments = {j: [] for j in employer_indices}

        # assign applicants to employers
        i = 0
        applicant_ids = list(applicant_data.keys())
        for j in employer_indices:
            for _ in range(APPS_PER_EMP):
                applicant_assignments[j].append(applicant_ids[i])
                i = (i + 1) % len(applicant_ids)
        print(applicant_assignments)

        for j, p in zip(employer_indices, players):
            p.applicants = '-'.join(map(str, applicant_assignments[j]))
            p.participant.vars['treatment'] = '-'.join(str(applicant_data[a]['treatment'])
                                                       for a in applicant_assignments[j])
            p.participant.vars['gender'] = '-'.join(applicant_data[a]['gender'] for a in applicant_assignments[j])
            p.participant.vars['avatar'] = '-'.join(applicant_data[a]['avatar'] for a in applicant_assignments[j])
            p.participant.vars['eval_correct'] = '-'.join(
                    str(applicant_data[a]['eval_correct']) for a in applicant_assignments[j]
                )
            p.participant.vars['self_eval'] = '-'.join(applicant_data[a]['self_eval']
                                                       for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree0'] = '-'.join(applicant_data[a]['self_eval_agree0']
                                                              for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree1'] = '-'.join(applicant_data[a]['self_eval_agree1']
                                                              for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree2'] = '-'.join(applicant_data[a]['self_eval_agree2']
                                                              for a in applicant_assignments[j])
            p.participant.vars['self_eval_statement'] = '-'.join(applicant_data[a]['self_eval_statement']
                                                                 for a in applicant_assignments[j])
            p.participant.vars['num_applicants'] = APPS_PER_EMP


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    applicants = models.StringField()
    bids = models.StringField()
    captcha = models.CharField(blank=True)
    understanding1a = models.StringField()
    understanding1b = models.StringField()
    age = models.StringField(choices=qtext['age'])
    gender = models.StringField(choices=qtext['gender'])
    gender = models.StringField(choices=qtext['gender'])
    ethnicity = models.StringField(choices=qtext['ethnicity'])
    home_state = models.StringField(choices=qtext['home_state'])
    education = models.StringField(choices=qtext['education'])
    married = models.StringField(choices=qtext['married'])
    household_income = models.StringField(choices=qtext['household_income'])
    employed = models.StringField(choices=qtext['employed'])
    religion = models.StringField(choices=qtext['religion'])
    politics = models.StringField(choices=qtext['politics'])
