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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

coordinate_key = ndb.Key('Coordinate', 'default_coordinate')


class Coordinate(ndb.Model):
    longitude = ndb.IntegerProperty(indexed=False)
    latitude = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        print 'recieved get request'
        coordinates_query = Coordinate.query(ancestor=coordinate_key).order(-Coordinate.date)
        coordinates = coordinates_query.fetch(10)
        print 'fetched coordinates: '+str(coordinates)

        template_values = {
            'coordinates': coordinates
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        rendered_template = template.render(template_values)

        print 'rendered template: '+str(rendered_template   )

        self.response.write(rendered_template)

    def post(self):
        coordinate = Coordinate(parent=coordinate_key)
        print self.request.params
        coordinate.latitude = int(self.request.get('latitude'))
        coordinate.longitude = int(self.request.get('longitude'))
        coordinate.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
                                  ('/', MainHandler)
                              ], debug=True)
