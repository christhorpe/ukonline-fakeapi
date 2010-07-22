#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson 
from google.appengine.api import memcache

import helpers


class MainHandler(webapp.RequestHandler):
    def get(self):
		postcode = self.request.get("postcode").replace(" ", "").lower()
		recordset = memcache.get(postcode)
		if not recordset:
			if len(postcode) > 0:
				records, query = helpers.get_nearest_centres(postcode)
				if records:
					recordset = {
						"status": "ok",
						"query": postcode,
						"results": records
						}
				else:
					recordset = {
						"status": "error",
						"message": "no records",
						}
			else:
				recordset = {
					"status": "error",
					"message": "no postcode",
					}
			memcache.add(postcode, recordset, 360)
		self.response.headers['Content-Type'] = 'application/json'
		if self.request.get("callback"):
			self.response.out.write(self.request.get("callback") + "(" + simplejson.dumps(recordset) +")")
		else:
			self.response.out.write(simplejson.dumps(recordset))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
