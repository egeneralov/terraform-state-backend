#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
from base64 import b64decode

import requests
from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth

from config import config
from db import Cluster, Config, Auth

def jsonify(data):
  return Response(json.dumps(data, default=str), mimetype='application/json')

app = Flask(__name__)
# auth = HTTPBasicAuth()



# KEY = uuid.uuid4()
# @app.route('/{}/<username>/<password>/'.format(KEY))
# def create_user(username, password):
#     "Create user, secured by random key, check runtime output"
#     u = Auth(
#         username=username,
#         password=password
#     )
#     return str(u.save())


# @auth.get_password
# def get_pw(username):
#   if username in [ i.username for i in Auth.select() ]:
#     return Auth.select().where(Auth.username == username).get().password
#   return None


@app.route('/')
def ok():
  r = {
    "ok": True
  }
  # print(KEY)
  return jsonify(r)


@app.route('/debug/')
# @auth.login_required
def debug():
  # if not auth.username() in ['egeneralov']:
  #   return '{}'
  r = {
    "ok": True,
    "port": os.environ['PORT'],
    "env": [ [key, os.environ[key]] for key in os.environ ]
  }
  return jsonify(r)


@app.route('/dump/')
# @auth.login_required
def dump():
  # if not auth.username() in ['egeneralov']:
  #   return '{}', 401
  r = {}
  for i in Cluster.select():
    try:
      data = Config.select().join(Cluster).where(Cluster.name == i.name).order_by(Config.date_create.desc()).limit(1).get().data
      r[i.name] = json.loads(data)
    except:
      if i.name != 'favicon.ico':
        r[i.name] = ''
  return jsonify(r)




@app.route('/favicon.ico')
def favicon():
    data =  b64decode('AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEREDwAAAAAAAAAAAAAAAAAAAABAREQPAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAQEREDwAAAAAAAAAAAAAAAAAAAABAREQPAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAQEREDwAAAABAREQPAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAQEREDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEBP8AAAD/AAAA/wAAAAAAAAAAQEREDwAAAAAAAAAAAAAAAAAAAP8EBAT/AAAA/wAAAAAAAAAAAAAAZ83NzZ4AAAAAQEREDwAAAAAAAAD/AAAARgAAAABAREQPAAAAAAAAAP8AAAAAAAAAAEBERA/Kysr2AAAAFgAAAP8AAAAAAAAAAAAAAABAREQPzMzM/wAAAAC5ubmBAAAAAEBERA+qqqr/AAAAAAAAAAAAAAAAQEREDwAAAP+kpKT/AAAAAAAAAACxbDr/sWg0ta98V+ixaDS1zMzM/wAAAAAAAAAAoqKi1AAAAAAAAAAAAAAAAAAAAADExMT/AAAA/0BERA8AAAAAAAAAALFoNP+ZmZn/QERED8zMzP+xaDT/AAAAAIODg/9AREQPsWg0/wAAAAAAAAAAAAAA/wAAAAAAAAD/QEREDwAAAACqqqr/sWg0/7FoNP9AREQPAAAAALFoNP8AAAAAqqqq/0BERA8AAAAAAAAA/wAAAAAAAAAAAAAAAAAAAABAREQPAAAAAAAAAACxaDT/sWg0/0BERA8AAAAAsWg0/7FoNP8AAAAAQEREDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAqmY1/7FoNP8AAAAAAAAAAAAAAABAREQPAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAhISE/wAAAAAAAAAAAAAAAAAAAACqZjX/AAAAnAAAAAAAAAAAAAAAAEBERA8AAAAAQEREDwAAAAAAAAAAAAAAFAAAABQqLCwiAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAREQPAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAQEREDwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAAAAAAAAAAAAAAAAAAQEREDwAAAAAAAAAAAAAAAAAAAABAREQPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQEREDwAAAAAAAAAAAAAAAAAAAABAREQPAAAAAAAAAAAAAAAAAAAAAEBERA8AAAAA//8AAP//AAD//wAAx+MAALvdAAB63gAAYN4AAHJWAACxrQAA/M8AAP+fAAD7zwAA//8AAP//AAD//wAA//8AAA==')

    return Response(data, mimetype='image/x-icon')



def get_cluster(name):
  result = [ i for i in Cluster.select() if i.name == name ]
  if not result:
    cl = Cluster(name=name)
    cl.save()
    return cl
  return result[0]


@app.route('/<name>/', methods=['GET'])
# @auth.login_required
def get_state(name):
  # if not auth.username() != name:
  #   print(auth.username(), name)
  #   return '', 401
  cl = get_cluster(name)
  it = Config.select().join(Cluster).where(Cluster.name == name).order_by(Config.date_create.desc())
  r = [ i for i in it ]
  if not r:
    return ''
  return jsonify(json.loads(r[0].data))


@app.route('/<name>/', methods=['POST'])
# @auth.login_required
def write_state(name):
  # if not auth.username() != name:
  #   print(auth.username(), name)
  #   return '', 401
  st = Config(
    data=request.get_data(),
    cluster=get_cluster(name)
  )
  if st.save():
    return jsonify(json.loads(st.data))


if __name__ == '__main__':
  app.run(
    host='0.0.0.0',
    port=config['port'],
    debug=True
  )
