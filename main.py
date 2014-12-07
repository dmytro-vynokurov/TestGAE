#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import cgi
import urllib
from google.appengine.ext import ndb
import webapp2
import jinja2
import json
import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

coordinate_key = ndb.Key('Coordinate', 'default_coordinate')


def coordinate_to_json(coordinate):
    return {
        'longitude': coordinate.longitude,
        'latitude': coordinate.latitude,
        'date': str(coordinate.date),
    }


def coordinate_from_json(json_parameter):
    coordinate = Coordinate(parent=coordinate_key)
    coordinate.longitude = json_parameter.get('longitude')
    coordinate.latitude = json_parameter.get('latitude')
    # date_as_string = json_parameter.get('date')
    # coordinate.date = datetime.datetime.strptime(date_as_string, '%Y-%m-%d %H:%M:%S.%f')
    return coordinate


class Coordinate(ndb.Model):
    longitude = ndb.IntegerProperty(indexed=False)
    latitude = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        coordinates_query = Coordinate.query(ancestor=coordinate_key).order(-Coordinate.date)
        coordinates = coordinates_query.fetch(10)

        template_values = {
            'coordinates': coordinates
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        rendered_template = template.render(template_values)

        self.response.write(rendered_template)

    def post(self):
        coordinate = Coordinate(parent=coordinate_key)
        coordinate.latitude = int(self.request.get('latitude'))
        coordinate.longitude = int(self.request.get('longitude'))
        coordinate.put()
        self.redirect('/')


class RestHandler(webapp2.RequestHandler, json.JSONEncoder):
    def get(self):
        coordinates_query = Coordinate.query(ancestor=coordinate_key).order(-Coordinate.date)
        coordinates = coordinates_query.fetch(10)
        result = []
        for coordinate in coordinates:
            result.append(coordinate_to_json(coordinate))
        json.dump(result, self.response)

    def post(self):
        coordinate_as_text = self.request.body
        coordinate_as_json = json.loads(coordinate_as_text)
        coordinate = coordinate_from_json(coordinate_as_json)
        coordinate.put()
        self.response.set_status(200, 'OK')

    def put(self):
        pass

    def delete(self):
        pass


app = webapp2.WSGIApplication([('/', MainHandler), ('/coordinates/', RestHandler)], debug=True)
