#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from flask import Flask, request
from config import config
from db import Cluster, Config


app = Flask(__name__)


@app.route('/')
def ok():
  r = {
    "ok": True,
    "port": os.environ['PORT'],
    "env": [ [key, os.environ[key]] for key in os.environ ]
  }
  return json.dumps(r)

def get_cluster(name):
  result = [ i for i in Cluster.select() if i.name == name ]
  if not result:
    cl = Cluster(name=name)
    cl.save()
    return cl
  return result[0]


@app.route('/<name>/', methods=['GET'])
def get_state(name):
  cl = get_cluster(name)
  it = Config.select().join(Cluster).where(Cluster.name == name).order_by(Config.date_create.desc())
  r = [ i for i in it ]
  if not r:
    return ''
  return r[0].data


@app.route('/<name>/', methods=['POST'])
def write_state(name):
  st = Config(
    data=request.get_data(),
    cluster=get_cluster(name)
  )
  if st.save():
    return st.data


if __name__ == '__main__':
  app.run(
    host='0.0.0.0',
    port=config['port'],
    debug=True
  )
