#!/usr/bin/env python

import datetime
import json

from flask import Flask
from pymongo import MongoClient

app = Flask("panopticon")

client = MongoClient()
db = client.apps
panopticon = db.panopticon


@app.route('/panopticon/raw/')
def raw_find():
    from flask import request
    q = request.args.get('q', None)

    query = panopticon.find()
    if q:
        query = panopticon.find(json.loads(q))

    response = {}
    response['items'] = []
    start = datetime.datetime.now()
    for item in query:
        del(item['_id'])
        response['items'].append(item)
    response['meta'] = {}
    response['meta']['count'] = len(response['items'])
    elapsed = datetime.datetime.now() - start
    response['meta']['time_elapsed'] = float('%s.%s' % (elapsed.seconds, elapsed.microseconds))
    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
