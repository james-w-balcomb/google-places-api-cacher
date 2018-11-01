# Copyright 2018 James William Balcomb. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Model objects for requests and responses.

Each API may support one or more serializations, such
as JSON, Atom, etc. The model classes are responsible
for converting between the wire format and the Python
object representation.
"""
from __future__ import absolute_import

# import json
import logging

# import constants

__author__ = 'james.w.balcomb@google.com (James William Balcomb)'

LOGGER = logging.getLogger(__name__)


def create_nearby_search_response(dictionary_from_json):
    return NearbySearchResponse(
        dictionary_from_json.get("html_attributions"),
        dictionary_from_json.get("results"),
        dictionary_from_json.get("status")
    )


def create_nearby_search_response_result(dictionary_from_json):
    return NearbySearchResponseResult(
        dictionary_from_json.get("geometry"),
        dictionary_from_json.get("icon"),
        dictionary_from_json.get("id"),
        dictionary_from_json.get("name"),
        dictionary_from_json.get("opening_hours"),
        dictionary_from_json.get("photos"),
        dictionary_from_json.get("place_id"),
        dictionary_from_json.get("plus_code"),
        dictionary_from_json.get("price_level"),
        dictionary_from_json.get("rating"),
        dictionary_from_json.get("reference"),
        dictionary_from_json.get("scope"),
        dictionary_from_json.get("types"),
        dictionary_from_json.get("vicinity")
    )


class RequestsResponse(object):
    # http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
    # Whenever a call is made to requests.get() and friends, you are doing two major things.
    # First, you are constructing a Request object
    #  which will be sent off to a server to request or query some resource.
    # Second, a Response object is generated once Requests gets a response back from the server.
    #  The Response object contains all of the information returned by the server and
    #  also contains the Request object you created originally.
    #
    # import requests.Request
    # import requests.Session
    # requests_session = requests.Session
    # requests_request = requests.Request('GET', url, data = data, headers = headers)
    # requests_prepared_request = requests_request.prepare()
    # requests_session_send_response = requests_session.send(
    #       requests_prepared_request,
    #       stream = stream,
    #       verify = verify,
    #       proxies = proxies,
    #       cert = cert,
    #       timeout = timeout
    # )
    # the above code will lose some of the advantages of having a Requests Session object.
    # In particular, Session-level state such as cookies will not get applied to your request.
    # To get a PreparedRequest with that state applied,
    #  replace the call to Request.prepare() with a call to Session.prepare_request()
    # requests_session = requests.Session()
    # requests_request = requests.Request('GET',  url, data = data, headers = headers)
    # requests_session_prepare_request = requests_session.prepare_request(requests_request)
    # requests_session_send_response = requests_session.send(
    #       requests_session_prepare_request,
    #       stream = stream,
    #       verify = verify,
    #       proxies = proxies,
    #       cert = cert,
    #       timeout = timeout
    # )
    # Body Content Workflow
    # By default, when you make a request, the body of the response is downloaded immediately.
    # You can override this behaviour and defer downloading the response body
    #  until you access the Response.content attribute with the stream parameter:
    # tarball_url = 'https://github.com/requests/requests/tarball/master'
    # r = requests.get(tarball_url, stream=True)
    # You can further control the workflow by use of the Response.iter_content()
    #  and Response.iter_lines() methods.
    # Alternatively, you can read the undecoded body
    #  from the underlying urllib3 urllib3.HTTPResponse at Response.raw.
    # If you set stream to True when making a request,
    #  Requests cannot release the connection back to the pool
    #  unless you consume all the data or call Response.close.
    # Keep-Alive
    # Excellent news — thanks to urllib3, keep-alive is 100% automatic within a session!
    # Any requests that you make within a session
    #  will automatically reuse the appropriate connection!
    # Streaming Requests
    # With Response.iter_lines() you can easily iterate over streaming APIs
    #  such as the Twitter Streaming API.
    # Simply set stream to True and iterate over the response with iter_lines:
    # import json
    # import requests
    # r = requests.get('https://httpbin.org/stream/20', stream=True)
    # for line in r.iter_lines():
    #     # filter out keep-alive new lines
    #     if line:
    #         decoded_line = line.decode('utf-8')
    #         print(json.loads(decoded_line))
    # When using decode_unicode=True with Response.iter_lines() or Response.iter_content(),
    #  you’ll want to provide a fallback encoding in the event the server doesn’t provide one:
    # r = requests.get('https://httpbin.org/stream/20', stream=True)
    # if r.encoding is None:
    #     r.encoding = 'utf-8'
    # for line in r.iter_lines(decode_unicode=True):
    #     if line:
    #         print(json.loads(line))
    # Encodings
    # When you receive a response, Requests makes a guess at the encoding to use for decoding
    #  the response when you access the Response.text attribute.
    # Requests will first check for an encoding in the HTTP header, and
    #  if none is present, will use chardet to attempt to guess the encoding.
    # The only time Requests will not do this is if no explicit charset is present
    #  in the HTTP headers and the Content-Type header contains text.
    # In this situation, RFC 2616 specifies that the default charset must be ISO-8859-1.
    # Requests follows the specification in this case. If you require a different encoding,
    #  you can manually set the Response.encoding property, or use the raw Response.content.
    #
    # HTTP GET is an idempotent method that returns a resource from a given URL.
    #
    # if r.status_code == requests.codes.ok:
    #   print(r.headers['content-type'])
    #
    # Timeouts
    # The connect timeout is the number of seconds Requests will wait for your client to establish a
    #  connection to a remote machine (corresponding to the connect()) call on the socket.
    # It’s a good practice to set connect timeouts to slightly larger than a multiple of 3,
    #  which is the default TCP packet retransmission window.
    # Once your client has connected to the server and sent the HTTP request, the read timeout is
    #  the number of seconds the client will wait for the server to send a response.
    # (Specifically, it’s the number of seconds that the client will wait between bytes sent from
    # the server. In 99.9% of cases, this is the time before the server sends the first byte).
    # If you specify a single value for the timeout, like this:
    # r = requests.get('https://github.com', timeout=5)
    # The timeout value will be applied to both the connect and the read timeouts.
    # Specify a tuple if you would like to set the values separately:
    # r = requests.get('https://github.com', timeout=(3.05, 27))
    # If the remote server is very slow, you can tell Requests to wait forever for a response,
    #  by passing None as a timeout value and then retrieving a cup of coffee.
    # r = requests.get('https://github.com', timeout=None)

    pass


class GooglePlacesApiCall(object):

    http_request_string = str()
    http_response_string = str()
    http_response_json = str()


class GooglePlacesApiCallNearbySearch(object):
    pass


class NearbySearchResponse(object):
    # html_attributions: a list (JSON Array?); as yet, always empty
    # results: a list of objects (JSON Array of JSON Object?)
    # status a string (e.g., "status" : "OK")
    def __init__(self, html_attributions, results, status):
        self.html_attributions = html_attributions
        # self.results = results
        # self.results = list()
        # self.results = list(NearbySearchResponseResult)
        # Expected type 'Iterable' (matched generic type 'Iterable[_T]'),
        #  got 'Type[NearbySearchResponseResult]' instead
        self.results = self.parse_results(results)
        self.status = status

    @staticmethod
    def parse_results(results):
        results_list = results
        results_object_list = list()
        for element in results_list:
            results_object_instance = create_nearby_search_response_result(element)
            results_object_list.append(results_object_instance)
        return results_object_list

    def __repr__(self):
        return '{{"html_attributions" = "{html_attributions}",' \
               '"results" = "{results}", ' \
               '"status" = {status}}}'.format(html_attributions = self.html_attributions,
                                              results = str(self.results),
                                              status = self.status)

    def __str__(self):
        return '{{"html_attributions" = "{html_attributions}",' \
               '"results" = "{results}", ' \
               '"status" = {status}}}'.format(html_attributions = self.html_attributions,
                                              results = str(self.results),
                                              status = self.status)


class NearbySearchResponseHtmlAttributes(object):
    pass


class NearbySearchResponseResult(object):
    def __init__(self,
                 geometry,
                 icon,
                 result_id,
                 name,
                 opening_hours,
                 photos,
                 place_id,
                 plus_code,
                 price_level,
                 rating,
                 reference,
                 scope,
                 types,
                 vicinity):
        self.geometry = geometry
        self.icon = icon
        self.result_id = result_id
        self.name = name
        self.opening_hours = opening_hours
        self.photos = photos
        self.place_id = place_id
        self.plus_code = plus_code
        self.price_level = price_level
        self.rating = rating
        self.reference = reference
        self.scope = scope
        self.types = types
        self.vicinity = vicinity

    def to_sql_insert_values(self):
        return "{geometry}, " \
               "{icon}, " \
               "{result_id}," \
               "{name}, " \
               "{opening_hours}, " \
               "{photos}, " \
               "{place_id}, " \
               "{plus_code}, " \
               "{price_level}, " \
               "{rating}, " \
               "{reference}, " \
               "{scope}, " \
               "{types}, " \
               "{vicinity}, " \
               '}}'.format(geometry = self.geometry,
                           icon = self.icon,
                           result_id = self.result_id,
                           name = self.name,
                           opening_hours = self.opening_hours,
                           photos = self.photos,
                           place_id = self.place_id,
                           plus_code = self.plus_code,
                           price_level = self.price_level,
                           rating = self.rating,
                           reference = self.reference,
                           scope = self.scope,
                           types = self.types,
                           vicinity = self.vicinity)

    def __repr__(self):
        return '{{' \
               '"geometry" = "{geometry}",' \
               '"icon" = "{icon}",' \
               '"result_id" = "{result_id}",' \
               '"name" = "{name}",' \
               '"opening_hours" = "{opening_hours}",' \
               '"photos" = "{photos}",' \
               '"place_id" = "{place_id}",' \
               '"plus_code" = "{plus_code}",' \
               '"price_level" = "{price_level}",' \
               '"rating" = "{rating}",' \
               '"reference" = "{reference}",' \
               '"scope" = "{scope}",' \
               '"types" = "{types}",' \
               '"vicinity" = "{vicinity}",' \
               '}}'.format(geometry = self.geometry,
                           icon = self.icon,
                           result_id = self.result_id,
                           name = self.name,
                           opening_hours = self.opening_hours,
                           photos = self.photos,
                           place_id = self.place_id,
                           plus_code = self.plus_code,
                           price_level = self.price_level,
                           rating = self.rating,
                           reference = self.reference,
                           scope = self.scope,
                           types = self.types,
                           vicinity = self.vicinity)

    def __str__(self):
        return '{{' \
               '"geometry" = "{geometry}",' \
               '"icon" = "{icon}",' \
               '"result_id" = "{result_id}",' \
               '"name" = "{name}",' \
               '"opening_hours" = "{opening_hours}",' \
               '"photos" = "{photos}",' \
               '"place_id" = "{place_id}",' \
               '"plus_code" = "{plus_code}",' \
               '"price_level" = "{price_level}",' \
               '"rating" = "{rating}",' \
               '"reference" = "{reference}",' \
               '"scope" = "{scope}",' \
               '"types" = "{types}",' \
               '"vicinity" = "{vicinity}",' \
               '}}'.format(geometry = self.geometry,
                           icon = self.icon,
                           result_id = self.result_id,
                           name = self.name,
                           opening_hours = self.opening_hours,
                           photos = self.photos,
                           place_id = self.place_id,
                           plus_code = self.plus_code,
                           price_level = self.price_level,
                           rating = self.rating,
                           reference = self.reference,
                           scope = self.scope,
                           types = self.types,
                           vicinity = self.vicinity)


class NearbySearchResponseResultGeometry(object):
    def __init__(self, location, viewport):
        self.location = location
        self.viewport = viewport

    def __str__(self):
        return '{{' \
               '"location" = "{location}",' \
               '"viewport" = "{viewport}",' \
               '}}'.format(location = self.location,
                           viewport = self.viewport)

    def to_sql_insert_values(self):
        return "{location}, " \
               "{viewport}, " \
               '}}'.format(location = self.location,
                           viewport = self.viewport)


class NearbySearchResponseResultGeometryLocation(object):
    pass


class NearbySearchResponseResultGeometryViewport(object):
    pass


class NearbySearchResponseResultGeometryViewportNortheast(object):
    pass


class NearbySearchResponseResultGeometryViewportSouthwest(object):
    pass


class NearbySearchResponseStatus(object):
    pass
