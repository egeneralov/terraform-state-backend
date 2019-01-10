import datetime

import peewee
from playhouse.db_url import connect

from config import config


class BaseModel(peewee.Model):
  class Meta:
    database = connect(config['database'])


class Cluster(BaseModel):
  name = peewee.CharField(unique=True, null=False)
  date_create = peewee.DateTimeField(unique=False, null=False, default = datetime.datetime.now)


class Config(BaseModel):
  data = peewee.TextField(unique=False, null=True)
  cluster = peewee.ForeignKeyField(Cluster, null=False)
  date_create = peewee.DateTimeField(unique=False, null=False, default = datetime.datetime.now)


db = connect(config['database'])
db.create_tables([
  Cluster, Config
])
