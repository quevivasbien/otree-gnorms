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
import random


# load question text
with open("_static/global/question_text.json", "r", encoding="utf-8") as fh:
    qtext = json.load(fh)
# load constants
with open("_static/global/constants.json", "r", encoding="utf-8") as fh:
    constants = json.load(fh)


author = "Mckay D Jensen"

doc = """
Gender norms of self-promotion
"""

perform_pdf = constants["perform_cdf"][:1] + [
    constants["perform_cdf"][i] - constants["perform_cdf"][i - 1]
    for i in range(1, len(constants["perform_cdf"]))
]


class Constants(BaseConstants):
    name_in_url = "applicant"
    players_per_group = None
    num_rounds = 1
    estimated_time = constants["applicant_estimated_time"]
    payment = "{:.2f}".format(constants["applicant_payment"])
    max_bonus = "{:.2f}".format(constants["applicant_max_bonus"])
    perform_cdf = "-".join(map(str, constants["perform_cdf"]))
    mean_performance = "{:.1f}".format(sum([x * i for i, x in enumerate(perform_pdf)]))
    num_wg = constants["num_wg1"] + constants["num_wg2"] + constants["num_wg3"]
    bonus_per_part = "{:.2f}".format(constants["bonus_per_part"])
    bonus_per_question = str(constants["bonus_per_question"])
    close_guess_proximity = str(constants["close_guess_proximity"])


class Subsession(BaseSubsession):
    def creating_session(self):
        # gender_idx session vars are used for assigning treatment
        # treatment assignment actually takes place in pages.py, after demographic survey
        self.session.vars["male_idx"] = 0
        self.session.vars["female_idx"] = 0
        for i, p in enumerate(self.get_players()):
            p.show_perf_guess = i % 2
            # assign question order
            question_order = random.sample(range(1, 32 + 1), 20)
            p.question_order = "-".join([str(x) for x in question_order])
            # assign evaluation and non-application questions
            eval_qs = random.sample(question_order, 10)
            noneval_qs = [j for j in question_order if j not in eval_qs]
            p.participant.vars["eval_qs"] = eval_qs
            p.participant.vars["noneval_qs"] = noneval_qs
            # assign wage guess orderings
            num_wg = Constants.num_wg
            wg_gender = random.choices(["Male", "Female"], k=num_wg)
            p.wage_guess_gender = "-".join(map(str, wg_gender))
            wg_image = random.choices(list(range(4)), k=num_wg)
            p.wage_guess_image = "-".join(map(str, wg_image))
            wg_perform = random.choices(list(range(11)), k=num_wg)
            p.wage_guess_perform = "-".join(map(str, wg_perform))
            wg_promote_type = (
                [0] * constants["num_wg1"]
                + [1] * constants["num_wg2"]
                + [2] * constants["num_wg3"]
            )
            random.shuffle(wg_promote_type)
            p.wage_guess_promote_type = "-".join(map(str, wg_promote_type))
            wg_promote1 = random.choices(list(range(6)), k=num_wg)
            p.wage_guess_promote1 = "-".join(map(str, wg_promote1))
            wg_promote2 = random.choices(list(range(101)), k=num_wg)
            p.wage_guess_promote2 = "-".join(map(str, wg_promote2))
            wg_promote3 = random.choices(list(range(3)), k=num_wg)
            p.wage_guess_promote3 = "-".join(map(str, wg_promote3))


class Group(BaseGroup):
    pass


understanding1_choices = [
    x.replace("~", Constants.payment) for x in qtext["understanding1"]
]

understanding3_choices = [
    x.replace("~", Constants.bonus_per_question) for x in qtext["understanding3"]
]

understanding4_choices = [
    x.replace("~", Constants.close_guess_proximity) for x in qtext["understanding4"]
]


class Player(BasePlayer):
    # vars set at session setup
    treatment = models.IntegerField()
    show_perf_guess = models.IntegerField()
    question_order = models.StringField()
    wage_guess_treatment = models.StringField()
    wage_guess_gender = models.StringField()
    wage_guess_image = models.StringField()
    wage_guess_perform = models.StringField()
    wage_guess_promote_type = models.StringField()
    wage_guess_promote1 = models.StringField()
    wage_guess_promote2 = models.StringField()
    wage_guess_promote3 = models.StringField()
    captcha = models.CharField(blank=True)
    # demographic survey questions
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
    # understanding questions
    understanding1 = models.StringField(
        choices=understanding1_choices, widget=widgets.RadioSelect
    )
    understanding2 = models.StringField(
        choices=qtext["understanding2"], widget=widgets.RadioSelect
    )
    understanding3 = models.StringField(
        choices=understanding3_choices, widget=widgets.RadioSelect,
    )
    understanding4 = models.StringField(
        choices=understanding4_choices, widget=widgets.RadioSelect
    )
    # ASVAB questions
    q1 = models.StringField(choices=qtext["q1"], widget=widgets.RadioSelect)
    q2 = models.StringField(choices=qtext["q2"], widget=widgets.RadioSelect)
    q3 = models.StringField(choices=qtext["q3"], widget=widgets.RadioSelect)
    q4 = models.StringField(choices=qtext["q4"], widget=widgets.RadioSelect)
    q5 = models.StringField(choices=qtext["q5"], widget=widgets.RadioSelect)
    q6 = models.StringField(choices=qtext["q6"], widget=widgets.RadioSelect)
    q7 = models.StringField(choices=qtext["q7"], widget=widgets.RadioSelect)
    q8 = models.StringField(choices=qtext["q8"], widget=widgets.RadioSelect)
    q9 = models.StringField(choices=qtext["q9"], widget=widgets.RadioSelect)
    q10 = models.StringField(choices=qtext["q10"], widget=widgets.RadioSelect)
    q11 = models.StringField(choices=qtext["q11"], widget=widgets.RadioSelect)
    q12 = models.StringField(choices=qtext["q12"], widget=widgets.RadioSelect)
    q13 = models.StringField(choices=qtext["q13"], widget=widgets.RadioSelect)
    q14 = models.StringField(choices=qtext["q14"], widget=widgets.RadioSelect)
    q15 = models.StringField(choices=qtext["q15"], widget=widgets.RadioSelect)
    q16 = models.StringField(choices=qtext["q16"], widget=widgets.RadioSelect)
    q17 = models.StringField(choices=qtext["q17"], widget=widgets.RadioSelect)
    q18 = models.StringField(choices=qtext["q18"], widget=widgets.RadioSelect)
    q19 = models.StringField(choices=qtext["q19"], widget=widgets.RadioSelect)
    q20 = models.StringField(choices=qtext["q20"], widget=widgets.RadioSelect)
    q21 = models.StringField(choices=qtext["q21"], widget=widgets.RadioSelect)
    q22 = models.StringField(choices=qtext["q22"], widget=widgets.RadioSelect)
    q23 = models.StringField(choices=qtext["q23"], widget=widgets.RadioSelect)
    q24 = models.StringField(choices=qtext["q24"], widget=widgets.RadioSelect)
    q25 = models.StringField(choices=qtext["q25"], widget=widgets.RadioSelect)
    q26 = models.StringField(choices=qtext["q26"], widget=widgets.RadioSelect)
    q27 = models.StringField(choices=qtext["q27"], widget=widgets.RadioSelect)
    q28 = models.StringField(choices=qtext["q28"], widget=widgets.RadioSelect)
    q29 = models.StringField(choices=qtext["q29"], widget=widgets.RadioSelect)
    q30 = models.StringField(choices=qtext["q30"], widget=widgets.RadioSelect)
    q31 = models.StringField(choices=qtext["q31"], widget=widgets.RadioSelect)
    q32 = models.StringField(choices=qtext["q32"], widget=widgets.RadioSelect)
    eval_correct = models.IntegerField()
    noneval_correct = models.IntegerField()
    # application questions
    avatar = models.StringField()
    self_eval = models.StringField(
        choices=qtext["self_eval"], widget=widgets.RadioSelect
    )
    self_eval_agree = models.IntegerField()
    self_eval_statement = models.StringField(
        choices=qtext["self_eval_statement"], widget=widgets.RadioSelect
    )
    # guessing questions
    wage_guess1 = models.FloatField()
    wage_guess2 = models.FloatField()
    wage_guess3 = models.FloatField()
    wage_guess_other = models.StringField()
    perform_guess1 = models.IntegerField()
    perform_guess2 = models.IntegerField()
    perform_guess3 = models.IntegerField()
    perform_guess_other = models.StringField()
    approp_guess1 = (
        models.IntegerField()
    )  # goes from 0 to 5, from v. soc. inappropriate to v. soc. appropriate
    approp_guess2 = models.IntegerField()
    approp_guess3 = models.IntegerField()
    approp_guess_other = models.StringField()

    study_topic_guess = models.StringField()

    def check_q(self, value, correct):
        if value != correct:
            return "Sorry. Your answer is incorrect. Please choose the correct answer to proceed."

    def understanding1_error_message(self, value):
        return self.check_q(value, understanding1_choices[1])

    def understanding2_error_message(self, value):
        return self.check_q(value, qtext["understanding2"][1])

    def understanding3_error_message(self, value):
        return self.check_q(value, understanding3_choices[0])

    def understanding4_error_message(self, value):
        return self.check_q(value, understanding4_choices[0])
