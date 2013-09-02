#!/usr/bin/env python
from glob import glob
import json
import time

from pymongo import MongoClient, DESCENDING

DATA_FILES = glob('data/*.json')

client = MongoClient()
db = client.apps
panopticon = db.panopticon


def load_data():
    for file_name in DATA_FILES:
        with open(file_name, 'rb') as jsonfile:
            days = json.loads(jsonfile.read())

        for day in days:
            unique_dict = {'date': day['date']}
            panopticon.update(unique_dict, day, upsert=True, multi=False)
            print day
