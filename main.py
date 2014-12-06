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
import cgi
import urllib
from google.appengine.ext import ndb
import webapp2

coordinate_key = ndb.Key('Coordinate', 'default_coordinate')


class Coordinate(ndb.Model):
    longitude = ndb.IntegerProperty(indexed=False)
    latitude = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        coordinates_query = Coordinate.query(ancestor=coordinate_key).order(-Coordinate.date)
        coordinates = coordinates_query.fetch(10)

        for coordinate in coordinates:
            self.response.write(coordinate)


        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello world! I am testing GAE')

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
