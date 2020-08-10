from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from random import randint

class MyPage(Page):
    form_model = 'player'
    form_fields = ['your_pick']
    


class Results(Page):
    pass


page_sequence = [MyPage]
