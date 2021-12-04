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
with open("_static/global/question_text.json", "r", encoding="utf-8") as fh:
    qtext = json.load(fh)
# load applicant data
with open("interface/applicant_data.json", "r", encoding="utf-8") as fh:
    applicant_data = json.load(fh)
# load constants
with open("_static/global/constants.json", "r", encoding="utf-8") as fh:
    constants = json.load(fh)


author = "Mckay D Jensen"

doc = """
Gender norms of self-promotion
"""

"""How to assign applicants to employers:
Want each employer to bid on 10*3 applicants,
so when assigning applicants to employers, can just loop through
applicant_data.json and assign 30 applicants to employer
"""

perform_pdf = constants["perform_cdf"][:1] + [
    constants["perform_cdf"][i] - constants["perform_cdf"][i - 1]
    for i in range(1, len(constants["perform_cdf"]))
]


class Constants(BaseConstants):
    name_in_url = "employer"
    players_per_group = None
    num_rounds = 1
    estimated_time = constants["employer_estimated_time"]
    payment = "{:.2f}".format(constants["employer_payment"])
    max_bonus = "{:.2f}".format(constants["employer_max_bonus"])
    perform_cdf = "-".join(map(str, constants["perform_cdf"]))
    mean_performance = "{:.1f}".format(sum([x * i for i, x in enumerate(perform_pdf)]))
    bonus_per_part = "{:.2f}".format(constants["bonus_per_part"])
    bonus_per_question = str(constants["bonus_per_question"])


class Subsession(BaseSubsession):
    def creating_session(self):
        players = self.get_players()
        employer_indices = list(range(len(players)))
        self.session.vars["applicant_assignments"] = {j: [] for j in employer_indices}

        # divide applicants by treatment so we can give employers only one type of treatment
        applicant_ids = {0: [], 1: [], 2: []}
        for a in applicant_data.keys():
            applicant_ids[applicant_data[a]["treatment"]].append(a)
        self.session.vars["applicant_ids"] = applicant_ids

        self.session.vars["male_idx"] = 0
        self.session.vars["female_idx"] = 0
        self.session.vars["emp_idx"] = 0

        self.session.vars["applicant_start_idxs"] = {i: 0 for i in range(3)}

        # everything else happens in pages.py, after demographic survey


class Group(BaseGroup):
    pass


understanding1_choices = [
    x.replace("~", Constants.payment) for x in qtext["understanding1"]
]

understanding3_choices = [
    x.replace("~", Constants.bonus_per_question) for x in qtext["emp_understanding3"]
]


class Player(BasePlayer):
    applicants = models.StringField()
    bids = models.StringField()
    perform_guesses = models.StringField()
    soc_approp_ratings = models.StringField()
    # captcha = models.CharField(blank=True)
    understanding1 = models.StringField(
        choices=understanding1_choices, widget=widgets.RadioSelect
    )
    understanding2 = models.StringField(
        choices=qtext["emp_understanding2"], widget=widgets.RadioSelect
    )
    understanding3 = models.StringField(
        choices=understanding3_choices, widget=widgets.RadioSelect
    )
    understanding4 = models.StringField(
        choices=qtext["emp_understanding4"], widget=widgets.RadioSelect
    )
    understanding5 = models.StringField(
        choices=qtext["emp_understanding5"], widget=widgets.RadioSelect
    )
    age = models.IntegerField(min=18, max=95)
    gender = models.StringField(choices=qtext["gender"])
    # ethnicity = models.StringField(choices=qtext['ethnicity'])
    # home_state = models.StringField(choices=qtext['home_state'])
    education = models.StringField(choices=qtext["education"])
    # married = models.StringField(choices=qtext['married'])
    # household_income = models.StringField(choices=qtext['household_income'])
    employed = models.StringField(choices=qtext["employed"])
    # religion = models.StringField(choices=qtext['religion'])
    # politics = models.StringField(choices=qtext['politics'])
    # resident = models.StringField(choices=["Yes", "No"])

    understanding1_attempts = models.IntegerField(initial=0)
    understanding2_attempts = models.IntegerField(initial=0)
    understanding3_attempts = models.IntegerField(initial=0)
    understanding4_attempts = models.IntegerField(initial=0)
    understanding5_attempts = models.IntegerField(initial=0)
    understanding6_attempts = models.IntegerField(initial=0)

    study_topic_guess = models.StringField()

    def check_q(self, value, correct):
        if value != correct:
            return "Sorry. Your answer is incorrect. Please choose the correct answer to proceed."

    def understanding1_error_message(self, value):
        return self.check_q(value, understanding1_choices[1])

    def understanding2_error_message(self, value):
        return self.check_q(value, qtext["emp_understanding2"][2])

    def understanding3_error_message(self, value):
        return self.check_q(value, understanding3_choices[2])

    def understanding4_error_message(self, value):
        return self.check_q(value, qtext["emp_understanding4"][0])

    def understanding5_error_message(self, value):
        return self.check_q(value, qtext["emp_understanding5"][0])
