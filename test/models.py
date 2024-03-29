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


class Constants(BaseConstants):
    name_in_url = "test"
    players_per_group = None
    num_rounds = 1
    estimated_time = constants["test_estimated_time"]
    payment = "{:.2f}".format(constants["test_payment"])
    max_bonus = "{:.2f}".format(constants["test_max_bonus"])
    bonus_per_question = str(constants["bonus_per_question"])


class Subsession(BaseSubsession):
    def creating_session(self):
        i = 0
        for p in self.get_players():
            i = (i + 1) % 3
            # assign question order
            question_order = random.sample(range(1, 32 + 1), 20)
            p.question_order = "-".join([str(x) for x in question_order])
            # assign evaluation and non-application questions
            eval_qs = random.sample(question_order, 10)
            noneval_qs = [j for j in question_order if j not in eval_qs]
            p.participant.vars["eval_qs"] = eval_qs
            p.participant.vars["noneval_qs"] = noneval_qs


class Group(BaseGroup):
    pass


u2_choices = [x.replace("<em>application</em> ", "") for x in qtext["understanding2"]]
u2_choices[1] = u2_choices[1].replace("will be", "will likely be")


class Player(BasePlayer):
    question_order = models.StringField()
    captcha = models.CharField(blank=True)
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
    understanding2 = models.StringField(choices=u2_choices, widget=widgets.RadioSelect)
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

    understanding2_attempts = models.IntegerField(initial=0)

    study_topic_guess = models.StringField()
    male_avg_answers_guess = models.FloatField(min=0, max=10)
    female_avg_answers_guess = models.FloatField(min=0, max=10)

    def understanding2_error_message(self, value):
        if value != u2_choices[1]:
            return "Sorry. Your answer is incorrect. Please choose the correct answer to proceed."
