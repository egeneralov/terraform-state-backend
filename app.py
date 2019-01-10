#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from flask import Flask, request
from config import config

app = Flask(__name__)

@app.route('/')
def ok(cluster):
  return '{"ok": true}'

@app.route('/<cluster>/', methods=['GET'])
def get_state(cluster):
  url = config[cluster]
  return requests.get(url).text


@app.route('/<cluster>/', methods=['POST'])
def upload_new_file(cluster):
  url = config[cluster]
  data = request.get_data()
  files = {'file': data}
  r = requests.post(url=url, files=files)
  if r.ok:
    return data

@app.route('/config/', methods=['POST'])
def save_config():
  data = request.get_json(force=True)
  with open('config.py', "w+") as f:
    f.write('config = ' + str(data))
  return str(data)

if __name__ == '__main__':
  app.run(
    host='0.0.0.0',
    port=os.environ['PORT'],
    debug=True
  )
