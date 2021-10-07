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

perform_pdf = constants['perform_cdf'][:1] \
    + [constants['perform_cdf'][i] - constants['perform_cdf'][i-1] for i in range(1, len(constants['perform_cdf']))]


class Constants(BaseConstants):
    name_in_url = 'employer'
    players_per_group = None
    num_rounds = 1
    estimated_time = constants['employer_estimated_time']
    payment = '{:.2f}'.format(constants['employer_payment'])
    max_bonus = '{:.2f}'.format(constants['employer_max_bonus'])
    mean_performance = '{:.1f}'.format(sum([x * i for i, x in enumerate(perform_pdf)]))


class Subsession(BaseSubsession):

    def creating_session(self):
        players = self.get_players()
        num_players = len(players)
        employer_indices = list(range(num_players))
        applicant_assignments = {j: [] for j in employer_indices}

        # divide applicants by treatment so we can give employers only one type of treatment
        applicant_ids = {0: [], 1: [], 2: []}
        for a in applicant_data.keys():
            applicant_ids[applicant_data[a]['treatment']].append(a)
        # assign applicants to employers
        start_idxs = {i: 0 for i in range(3)}
        for i, emp_idx in enumerate(employer_indices):
            treatment = i % 3
            num_apps = (constants['apps_per_emp1']
                        + constants['apps_per_emp2']
                        + (constants['apps_per_emp3a'] if treatment == 0 else constants['apps_per_emp3b']))
            start_index = start_idxs[treatment]
            for j in range(num_apps):
                treatment_index = (start_index + j) % len(applicant_ids[treatment])
                if treatment_index == 0:
                    # sample without replacement until all applicants exhausted, then resample
                    shuffle(applicant_ids[treatment])
                applicant_assignments[emp_idx].append(applicant_ids[treatment][treatment_index])
            players[i].participant.vars['treatment'] = treatment
            players[i].participant.vars['apps_per_emp1'] = constants['apps_per_emp1']
            players[i].participant.vars['apps_per_emp2'] = constants['apps_per_emp2']
            players[i].participant.vars['apps_per_emp3'] = (
                constants['apps_per_emp3a'] if treatment == 0 else constants['apps_per_emp3b']
            )
            players[i].participant.vars['apps_per_emp'] = num_apps

        for j, p in zip(employer_indices, players):
            p.applicants = '-'.join(map(str, applicant_assignments[j]))
            p.participant.vars['gender'] = '-'.join(applicant_data[a]['gender'] for a in applicant_assignments[j])
            p.participant.vars['avatar'] = '-'.join(applicant_data[a]['avatar'] for a in applicant_assignments[j])
            p.participant.vars['eval_correct'] = '-'.join(
                    str(applicant_data[a]['eval_correct']) for a in applicant_assignments[j]
                )
            p.participant.vars['self_eval'] = '-'.join(applicant_data[a]['self_eval']
                                                       for a in applicant_assignments[j])
            p.participant.vars['self_eval_agree'] = '-'.join(str(applicant_data[a]['self_eval_agree'])
                                                             for a in applicant_assignments[j])
            p.participant.vars['self_eval_statement'] = '-'.join(applicant_data[a]['self_eval_statement']
                                                                 for a in applicant_assignments[j])


class Group(BaseGroup):
    pass


understanding1_choices = [x.replace('~', Constants.payment) for x in qtext['understanding1']]


class Player(BasePlayer):
    applicants = models.StringField()
    bids = models.StringField()
    perform_guesses = models.StringField()
    soc_approp_ratings = models.StringField()
    captcha = models.CharField(blank=True)
    understanding1 = models.StringField(choices=understanding1_choices, widget=widgets.RadioSelect)
    understanding2 = models.StringField(choices=qtext['emp_understanding2'], widget=widgets.RadioSelect)
    understanding3a = models.StringField(choices=qtext['emp_understanding3'], widget=widgets.RadioSelect)
    understanding3b = models.StringField(choices=qtext['emp_understanding3'], widget=widgets.RadioSelect)
    understanding4 = models.StringField(choices=qtext['emp_understanding4'], widget=widgets.RadioSelect)
    understanding5 = models.StringField(choices=qtext['emp_understanding5'], widget=widgets.RadioSelect)
    age = models.IntegerField(min=18, max=95)
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

    def check_q(self, value, correct):
        if value != correct:
            return 'Sorry. Your answer is incorrect. Please choose the correct answer to proceed.'

    def understanding1_error_message(self, value):
        return self.check_q(value, understanding1_choices[1])

    def understanding2_error_message(self, value):
        return self.check_q(value, qtext['emp_understanding2'][2])

    def understanding3a_error_message(self, value):
        return self.check_q(value, qtext['emp_understanding3'][2])

    def understanding3b_error_message(self, value):
        return self.check_q(value, qtext['emp_understanding3'][1])

    def understanding4_error_message(self, value):
        return self.check_q(value, qtext['emp_understanding4'][0])

    def understanding5_error_message(self, value):
        return self.check_q(value, qtext['emp_understanding5'][0])
