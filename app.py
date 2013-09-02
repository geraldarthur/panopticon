#!/usr/bin/env python

import datetime
import json

from flask import Flask, render_template
from pymongo import MongoClient

app = Flask("panopticon")

client = MongoClient()
db = client.apps
panopticon = db.panopticon


@app.route('/panopticon/<int:date>/')
def index(date=20130901):
    from flask import request
    context = {}
    context['date'] = date
    return render_template('map.html', **context)


@app.route('/panopticon/<format>/')
def raw_find(format="raw"):
    from flask import request
    q = request.args.get('q', None)

    query = panopticon.find()
    if q:
        query = panopticon.find(json.loads(q))

    response = {}

    if format == "raw":
        response['items'] = []
        start = datetime.datetime.now()
        for item in query:
            del(item['_id'])
            response['items'].append(item)
        response['meta'] = {}
        response['meta']['count'] = len(response['items'])
        elapsed = datetime.datetime.now() - start
        response['meta']['time_elapsed'] = float('%s.%s' % (elapsed.seconds, elapsed.microseconds))

    if format == "geojson":
        response['type'] = "FeatureCollection"
        response['features'] = []
        if query.count() > 0:
            for day in query:
                segments = day.get('segments', None)
                if segments:
                    for segment in segments:
                        place = segment.get('place', None)
                        if place:
                            place_dict = {}
                            place_dict['properties'] = {}
                            place_dict['geometry'] = {}
                            place_dict['type'] = "Feature"
                            place_dict['geometry']['type'] = "Point"
                            place_dict['geometry']['coordinates'] = [place['location']['lon'], place['location']['lat']]
                            place_dict['properties'] = {
                                "marker-shape": "pin",
                                "marker-size": "small",
                                "marker-symbol": "circle-stroked",
                                "marker-color": "#ace",
                                "title": place['name'],
                                "description": place['type']
                            }
                            place_dict['properties']['name'] = place['name']
                            place_dict['properties']['type'] = place['type']
                            response['features'].append(place_dict)
                        activities = segment.get('activities', None)
                        if activities:
                            for activity in activities:
                                track_points = activity.get('trackPoints', None)
                                if track_points:
                                    line_dict = {}
                                    line_dict['properties'] = {}
                                    line_dict['geometry'] = {}
                                    line_dict['type'] = "Feature"
                                    line_dict['geometry']['type'] = "LineString"
                                    line_dict['geometry']['coordinates'] = []
                                    for point in track_points:
                                        line_dict['geometry']['coordinates'].append([point['lon'], point['lat']])
                                        response['features'].append(line_dict)
                                    line_dict['properties']['type'] = activity['activity']

    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
