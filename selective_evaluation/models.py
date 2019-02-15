from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
import csv
from utils import cp

author = 'Philipp Chapkovski'

doc = """
Pre-selecting choise of items for the subsequent evaluation
"""


class Constants(BaseConstants):
    name_in_url = 'selective_evaluation'
    players_per_group = None
    num_rounds = 1
    with open('selective_evaluation/items.csv', 'r') as f:
        data = [line.rstrip('\n') for line in f]


class Subsession(BaseSubsession):
    def creating_session(self):
        items_to_create = []
        for i in Constants.data:
            for p in self.get_players():
                items_to_create.append(
                    Item(
                        player=p,
                        item=i
                    )
                )
        Item.objects.bulk_create(items_to_create)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Item(djmodels.Model):
    player = djmodels.ForeignKey(to=Player, related_name='items')
    item = models.StringField()
    selected = models.BooleanField()
    evaluation = models.IntegerField()
