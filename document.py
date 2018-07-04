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


'''clean()
insert(client=Client(name="OfftheGrid",type="Product"),
       developers=[Developer(name="Fercho",zohoid=338873000000170987, status=Status.PLACED.value),
                   Developer(name="Jorge", zohoid=338873000000173889, status=Status.PLACED.value),
                   Developer(name="Luis", zohoid=338873000000171007, status=Status.PLACED.value)],
       contract=Contract(fromdate=datetime.date(2018,12, 17),todate=datetime.date(2019,1, 15), description="Nov 17, extended recently to 1/15", autorenew=False),
       tech=["Angular", "Node"])

insert(client=Client(name="AnaPlan - Dev",type="Product"),
       developers=[Developer(name="Jose", zohoid=4, status=Status.PLACED.value),
                   Developer(name="Cristiano", zohoid=5, status=Status.PLACED.value),
                   Developer(name="Chistopher", zohoid=6, status=Status.PLACED.value)],
       contract=Contract(fromdate=datetime.date(2018,12, 17),todate=datetime.date(2019,1, 15), description="Nov 17, extended recently to 1/15", autorenew=False),
       tech=["Angular", "Node"])

insert(client=Client(name="Zignal Labs",type="Product"),
       developers=[Developer(name="Rodolfo", zohoid=7, status=Status.PLACED.value),
                   Developer(name="Antonio", zohoid=8, status=Status.PLACED.value),
                   Developer(name="Alvaro", zohoid=9, status=Status.PLACED.value),
                   Developer(name="Lucio", zohoid=10, status=Status.PLACED.value),
                   Developer(name="Santiago", zohoid=11, status=Status.PLACED.value)],
       contract=Contract(fromdate=datetime.date(2018, 12, 17), todate=datetime.date(2019, 1, 15),
                         description="Nov 17, extended recently to 1/15", autorenew=False),
       tech=["React"])
'''