import urllib.parse
import requests
import numpy  as np
from enum import Enum
import datetime
import pandas as pd
import json
from mongoengine import *
connect('pymongo_test_v1')


class Status(Enum):
    PLACED = "PLACED"
    BENCH = "BENCH"
    LIMIT = "LIMIT"
    AVAILABLE = "AVAILABLE"
    UNBILLABLE = "UNBILLABLE"


class Client(EmbeddedDocument):
    name = StringField(required=True)
    type = StringField(required=True)


class Contract(EmbeddedDocument):
    fromdate = DateTimeField(required=True)
    todate = DateTimeField(required=True)
    description = StringField(required=True)
    autorenew = BooleanField(default=False)


class Person(EmbeddedDocument):
    meta = {'allow_inheritance': True}
    zohoid = IntField(required=True)
    name = StringField(required=True)


class Developer(Person):
    status = StringField(required=True)


class Team(Document):
    client = EmbeddedDocumentField(Client)
    tech = ListField(StringField(max_length=30, required=True))
    contract = EmbeddedDocumentField(Contract)
    developers = ListField(EmbeddedDocumentField(Developer))


class Service:
    def save(self, team):
        my_team = Team(client=team['client'], developers=team['developers'], contract=team['contract'], tech=team['tech'])
        my_team.save()
        return my_team

    def get(self, id):
        return Team.objects().get(id=id)

    def update(self, team, id):
        my_team = self.get(id)
        my_team.modify(client = team['client'], developers=team['developers'], contract=team['contract'], tech=team['tech'])
        return my_team

    def delete(self, id):
        my_team = self.get(id)
        my_team.delete()

    def list(self):
        return Team.objects().to_json()



def get_teams():
    teams = []
    for team_db in Team.objects():
        customteam = {}
        team =  json.loads(team_db.to_json())
        customteam["id"] = team["_id"]["$oid"]
        customteam["contract"] = team["contract"]
        customteam["developers"] = team["developers"]
        customteam["tech"] = team["tech"]
        teams.append(team)
        print(customteam["contract"])
    return teams


def clean():

    for team_db in Team.objects():
        team_db.delete()


def insert(client, developers, contract, tech):
    # id="5b2a689f32fd944e08fda5b0"
    my_team = Team(client=client, developers=developers, contract=contract, tech=tech)
    my_team.save()