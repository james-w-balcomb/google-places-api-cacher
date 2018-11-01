import datetime
import email
# import itertools
import json
# import locale
# import logging
# import logging.config
# import os
import requests
# import sys
import time

from urllib.parse import urlencode

# import ats_utilities.ats_configuration
# import ats_utilities.ats_file_system
# import ats_utilities.ats_log
# import ats_utilities.ats_mysql
# import ats_utilities.ats_url
# import ats_utilities.ats_utilities
# import constants

from ats_utilities import ats_url
# from model import create_nearby_search_response
# from model import create_nearby_search_response_result
# from google_places_api_cacher import TEST_RUN
from google_places_api_cacher import SAVE_FILE
# from google_places_api_cacher import MAXIMUM_LOOP_COUNT


PLACE_TYPE_NAMES = [
    "bar",
    "night_club"
]

LATITUDES = [
    41.902852,
    41.901037,
    41.899222,
    41.897407,
    41.895592,
    41.893777,
    41.891962,
    41.890147,
    41.888332,
    41.886517,
    41.884702,
    41.882887,
    41.881072,
    41.879257,
    41.877442,
    41.875627,
    41.873812,
    41.871997,
    41.870182,
    41.868367,
    41.866552,
    41.864737,
    41.862922,
    41.861107,
    41.859292,
    41.857477,
    41.855662,
    41.853847,
    41.852032,
    41.850217
]

LONGITUDES = [
    -87.709340,
    -87.706907,
    -87.704474,
    -87.702041,
    -87.699608,
    -87.697175,
    -87.694742,
    -87.692309,
    -87.689876,
    -87.687443,
    -87.685010,
    -87.682577,
    -87.680144,
    -87.677711,
    -87.675278,
    -87.672845,
    -87.670412,
    -87.667979,
    -87.665546,
    -87.663113,
    -87.660680,
    -87.658247,
    -87.655814,
    -87.653381,
    -87.650948,
    -87.648515,
    -87.646082,
    -87.643649,
    -87.641216,
    -87.638783,
    -87.636350,
    -87.633917,
    -87.631484,
    -87.629051,
    -87.626618,
    -87.624185,
    -87.621752,
    -87.619319,
    -87.616886,
    -87.614453,
    -87.612020,
    -87.609587,
    -87.607154,
    -87.604721,
    -87.602288,
    -87.599855,
    -87.597422
]

# Scheme AKA Protocol
DEFAULT_URI_SCHEME = "https"
# DEFAULT_URI_AUTHORITY = "maps.googleapis.com"
# DEFAULT_URI_PATH_BASE = "/maps/api/place"

GOOGLE_PLACES_API_HOSTNAME = "maps.googleapis.com"
GOOGLE_PLACES_API_BASE_PATH = "/maps/api/place"

FIND_PLACE_ENDPOINT_PATH = "/findplacefromtext"
NEARBY_SEARCH_ENDPOINT_PATH = "/nearbysearch"  # requires: location
PLACE_DETAIL_ENDPOINT_PATH = "/details"  # requires: placeid
TEXT_SEARCH_ENDPOINT_PATH = "/textsearch"

DEFAULT_OUTPUT_TYPE = "json"
# DEFAULT_OUTPUT_TYPE = "xml"

DEFAULT_FIND_PLACE_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
DEFAULT_NEARBY_SEARCH_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DEFAULT_TEXT_SEARCH_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/textsearch/json"

DEFAULT_NEARBY_SEARCH_URL = \
    "https://maps.googleapis.com/maps/api/place/nearbysearch/json?parameters"

FIND_PLACE_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/findplacefromtext/output?parameters"
NEARBY_SEARCH_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters"
TEXT_SEARCH_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/textsearch/output?parameters"

DEFAULT_PLACE_TYPE = "bar"

# DEFAULT_RADIUS_METERS = "1609.34"  # 1   || 1.0   mile = 1609.34 meters
# DEFAULT_RADIUS_METERS = "804.672"  # 1/2 || 0.5   mile =  804.672 meters
# DEFAULT_RADIUS_METERS = "402.336"  # 1/4 || 0.25  mile =  402.336 meters
DEFAULT_RADIUS_METERS = "201.168"  # 1/8 || 0.125 mile =  201.168 meters
# "The maximum allowed radius is 50 000 meters."
# - https://developers.google.com/places/web-service/search
MAXIMUM_ALLOWED_RADIUS_METERS = 50000

# Formula: Miles to Meters: Miles * 1609.344 = Meters
# Formula: Miles to Nautical Miles: Miles * 1.151 = Nautical Miles
# 41.8818616,-87.6294258 = Center: Chicago, Illinois; State & Madison
DEFAULT_LATITUDE = "41.8818616"
DEFAULT_LONGITUDE = "-87.6294258"

DEFAULT_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
              "?location=41.8818616,-87.6294258&radius=201.168&type=bar"

DEFAULT_TEST_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
                   "?location=41.8818616,-87.6294258&radius=50000&type=bar"

# "The maximum number of results that can be returned is 60."
# - https://developers.google.com/places/web-service/search
MAXIMUM_NUMBER_OF_RESULTS = 60  # 20 per page, 3 pages

SCHEMA_NAME = "google_places_api_cacher"
TABLE_NAME_NEARBY_SEARCH_RESULT = "nearby_search"
TABLE_NAME_NEARBY_SEARCH_RESULT_PHOTOS = "nearby_search_result_photos"

INSERT_INTO_NEARBY_SEARCH_REQUESTS = "INSERT INTO " \
                                     "google_places_api_cacher.nearby_search_requests (" \
                                     "api_endpoint_name," \
                                     "place_name_type," \
                                     "latitude," \
                                     "longitude," \
                                     "range_meters," \
                                     "final_url," \
                                     "record_ts" \
                                     ") VALUES (" \
                                     "%s," \
                                     "% s," \
                                     "% s," \
                                     "% s," \
                                     "% s," \
                                     "% s," \
                                     "% s" \
                                     ");"


class NearbySearchRequest(object):
    def __INIT__(self, latitude, longitude, radius_meters, place_type_name, api_key):
        self.latitude = latitude,
        self.longitude = longitude,
        self.radius_meters = radius_meters,
        self.place_type_name = place_type_name,
        self.api_key = api_key
        self.latitude_longitude_pair = "{latitude},{longitude}". \
            format(latitude = self.longitude,
                   longitude = self.longitude)
        self.uri = "{scheme}://{authority}{api_base_path}{api_endpoint_path}{output_type}". \
            format(scheme = DEFAULT_URI_SCHEME,
                   authority = GOOGLE_PLACES_API_HOSTNAME,
                   api_base_path = GOOGLE_PLACES_API_BASE_PATH,
                   api_endpoint_path = NEARBY_SEARCH_ENDPOINT_PATH,
                   output_type = DEFAULT_OUTPUT_TYPE)
        self.query_string_parameters = "?" \
                                       "type={place_type_name}" \
                                       "&" \
                                       "location={latitude_longitude_pair}" \
                                       "&" \
                                       "radius={radius_meters}" \
                                       "&" \
                                       "key={api_key}". \
            format(latitude_longitude_pair = self.latitude_longitude_pair,
                   radius_meters = self.radius_meters,
                   place_type_name = self.place_type_name,
                   api_key = self.api_key)
        self.url = "{uri}{query_string_parameters}". \
            format(uri = self.uri,
                   query_string_parameters = self.query_string_parameters)


# import requests
#
# url = 'http://maps.googleapis.com/maps/api/directions/json'
#
# params = dict(
#     origin='Chicago,IL',
#     destination='Los+Angeles,CA',
#     waypoints='Joplin,MO|Oklahoma+City,OK',
#     sensor='false'
# )
#
# resp = requests.get(url=url, params=params)
# data = resp.json() # Check the JSON Response Content documentation below
# JSON Response Content:
#  http://docs.python-requests.org/en/latest/user/quickstart/#json-response-content

# The Response object
# The result of the get method, i.e. the web server's response,
#  i.e. what's been assigned to the resp variable above, is a Response object.
# You can print out its type to verify this:
# print(type(resp))  # => <class 'requests.models.Response'>
# According to the Requests documentation, we can access the content of the response
#  (i.e. the raw HTML in this example) with the text attribute:
# txt = resp.text
# # print the size of the web-page's content:
# print(len(txt))  # => 1270
# There's other useful attributes, too:
# print(resp.ok)           # => True
# print(resp.status_code)  # => 200
# print(resp.headers['content-type'])   # => "text/html"
# The headers attribute contains the response headers as Python dictionary.
# The full object looks like this:
# {
#   "content-length": "1270",
#   "content-type": "text/html",
#   "etag": '359670651"',
#   "cache-control": "max-age=604800",
#   "server": "ECS (cpm/F9D5)",
#   "date": "Mon, 20 Apr 2015 12:16:24 GMT",
#   "x-cache": "HIT",
#   "x-ec-custom-error": "1",
#   "accept-ranges": "bytes",
#   "last-modified": "Fri, 09 Aug 2013 23:54:35 GMT",
#   "expires": "Mon, 27 Apr 2015 12:16:24 GMT"
# }

# http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects


def do_nearby_search(mysql_connection = None,
                     mysql_cursor = None,
                     output_type = None,
                     latitude = None,
                     longitude = None,
                     radius_meters = None,
                     place_type_name = None,
                     api_key = None):
    """

    :param mysql_connection: [required]
    :param mysql_cursor: [required]
    :param output_type: [optional] (Default: DEFAULT_OUTPUT_TYPE)
    :param latitude: [required]
    :param longitude: [required]
    :param radius_meters: [optional] (Default: DEFAULT_RADIUS_METERS)
    :param place_type_name: [required]
    :param api_key: [required]
    :return:
    """
    # TODO(JamesBalcomb): raise ValueError if missing required parameters
    if mysql_connection is None:
        raise ValueError("mysql_connection? Nein danke!")
    if mysql_cursor is None:
        raise ValueError("mysql_cursor? Nein danke!")
    if output_type is None:
        del output_type
    if latitude is None:
        raise ValueError("latitude? Nein danke!")
    if longitude is None:
        raise ValueError("longitude? Nein danke!")
    if radius_meters is None:
        # del radius_meters
        # UnboundLocalError: local variable 'radius_meters' referenced before assignment
        pass
    if place_type_name is None:
        raise ValueError("place_type_name? Nein danke!")
    if api_key is None:
        raise ValueError("api_key? Nein danke!")

    # output_type = DEFAULT_OUTPUT_TYPE if output_type is None else output_type
    radius_meters = DEFAULT_RADIUS_METERS if radius_meters is None else radius_meters

    # Q: How to create the request URLs before executing the requests?
    # A: Use PreparedRequests.
    #    To build the URL, you can build your own Request object and prepare it:
    #    from requests import Session, Request
    #    s = Session()
    #    p = Request('GET', 'http://someurl.com', params=request_parameters).prepare()
    #    log.append(p.url)
    #    Later, when you're ready to send, you can just do this:
    #    r = s.send(p)
    #    The relevant section of the documentation is here.
    #    \_,-> http://docs.python-requests.org/en/latest/user/advanced/#prepared-requests

    # TODO(JamesBalcomb): ?make the file_name just parse the API End-Point Path?
    # TODO(JamesBalcomb): ?make the request record just use the url_final, sans token & key?
    # TODO(JamesBalcomb): ?save the request record_id with the result?
    api_endpoint_name = "nearby_search"  # used by file name and request record

    next_page_token = None

    results_page_number = 1

    # PEP 315:
    # "Users of the language are advised to use the while-True form with an inner if-break
    #   when a do-while loop would have been appropriate."
    while True:

        # print("BEGIN: results_page_number: {}".format(str(results_page_number)))

        # print("BEGIN: next_page_token: {}".format(str(next_page_token)))

        # url_final = DEFAULT_TEST_URL
        # # url_final = url_final + "&pagetoken=" + next_page_token
        # # TypeError: must be str, not NoneType
        # # url_final = url_final + "&pagetoken=" + str(next_page_token)
        # # 'status': 'INVALID_REQUEST'
        # if next_page_token is None:
        #     url_final = url_final + "&pagetoken=" + ""
        # else:
        #     url_final = url_final + "&pagetoken=" + str(next_page_token)
        # url_final = url_final + "&key=" + api_key
        # print("url_final: {}".format(str(url_final)))

        # build_nearby_search_url_string(output_type = None,
        #                                    latitude = None,
        #                                    longitude = None,
        #                                    radius_meters = None,
        #                                    place_type = None,
        #                                    page_token = None,
        #                                    api_key = None)
        url_final = build_nearby_search_url_string(latitude = latitude,
                                                   longitude = longitude,
                                                   place_type = place_type_name,
                                                   page_token = next_page_token,
                                                   api_key = api_key)
        print("url_final: {}".format(str(url_final)))

        record_ts = datetime.datetime.now()  # <class 'str'>
        # >>> record_ts: 2018-10-25 14:15:11.508349

        # ############################### #
        # BEGIN: Get NearbySearchResponse #
        # ############################### #

        requests_response = requests.get(url_final)  # <class 'requests.models.Response'>
        # print("requests_response: {}".format(str(requests_response)))
        # requests.exceptions.MissingSchema: Invalid URL '...': No schema supplied.
        # requests_response: <Response [404]>

        # requests_response_raw = requests_response.raw
        # print("requests_response_raw: {}".format(str(requests_response_raw)))
        # requests_response.content
        # requests_response.json()
        requests_response_text = requests_response.text  # <class 'str'>
        # requests_response.encoding  # e.g., 'utf-8'
        # requests_response.encoding = 'ISO-8859-1'
        # requests_response.status_code  # e.g., 200
        # requests_response.status_code == requests.codes.ok  # e.g., True
        # requests_response.raise_for_status()  # e.g., .exceptions.HTTPError: 404 Client Error
        # requests_response.raise_for_status()  # e.g., (for status_code 200) None
        # requests_response.headers  # e.g., {..., 'content-type': 'application/json', ...}
        # requests_response.headers.get('content-type')

        http_header_date = requests_response.headers.get('date')  # <class 'str'>
        # >>> http_header_date: Thu, 25 Oct 2018 19:15:38 GMT
        # http_header_date = datetime.datetime\
        #     .strptime(http_header_date, '%a, %d %b %Y %H:%M:%S %z')\
        #     .strftime('%Y-%m-%d %H:%M:%S.%f')
        # ValueError: time data
        #  'Thu, 25 Oct 2018 22:29:55 GMT' does not match format '%a, %d %b %Y %H:%M:%S %z'
        # datetime.datetime.strptime(http_header_date, '%a, %d %b %Y %H:%M:%S GMT')
        http_header_date = email.utils.parsedate_to_datetime(http_header_date)
        http_header_date = \
            http_header_date.replace(tzinfo = datetime.timezone.utc).astimezone(tz = None)
        # print("http_header_date: {}".format(str(http_header_date)))

        nearby_search_response = json.loads(requests_response_text)  # <class 'dict'>
        # json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
        print("nearby_search_response: {}".format(str(nearby_search_response)))

        next_page_token = nearby_search_response.get('next_page_token')  # <class 'str'>
        # >>> next_page_token: CqQCHAEAAJsW3i1TuGl-A ... GML4OHYT-8DsxoUgwXQMCQC2JzcVQ60dAidR2XMLMk

        results_count = len(nearby_search_response.get("results"))
        # print("results_count: {}".format(str(results_count)))

        # nearby_search_response = get_nearby_search(latitude,
        #                                            longitude,
        #                                            radius_meters,
        #                                            api_key)

        # ############################# #
        # END: Get NearbySearchResponse #
        # ############################# #

        # ################################ #
        # BEGIN: Save NearbySearchResponse #
        # ################################ #

        if SAVE_FILE:
            save_file(nearby_search_response,
                      api_endpoint_name,
                      place_type_name,
                      latitude,
                      longitude,
                      radius_meters,
                      results_page_number)
        # END: if SAVE_FILE:

        save_nearby_search_response(mysql_connection,
                                    mysql_cursor,
                                    nearby_search_response,
                                    http_header_date)

        save_nearby_search_request(mysql_connection,
                                   mysql_cursor,
                                   api_endpoint_name,
                                   place_type_name,
                                   latitude,
                                   longitude,
                                   radius_meters,
                                   results_page_number,
                                   results_count,
                                   url_final,
                                   record_ts)

        # ############################## #
        # END: Save NearbySearchResponse #
        # ############################## #

        results_page_number = results_page_number + 1

        # print("END: results_page_number: {}".format(str(results_page_number)))

        # print("END: next_page_token: {}".format(str(next_page_token)))

        # if results_page_number >= 4:
        #     print("Exceeded Request Count: ({})".format(results_page_number))
        #     break

        if next_page_token is None:
            break

        # Give Google a little time to prepare the Results for the Next Page
        time.sleep(2)

    # while True:


def build_nearby_search_url_string(output_type = None,
                                   latitude = None,
                                   longitude = None,
                                   radius_meters = None,
                                   place_type = None,
                                   page_token = None,
                                   api_key = None):

    # TODO(JamesBalcomb): raise ValueError if missing required parameters
    if output_type is None:
        # del output_type
        # UnboundLocalError: local variable 'output_type' referenced before assignment
        pass
    if latitude is None:
        raise ValueError("latitude? Nein danke!")
    if longitude is None:
        raise ValueError("longitude? Nein danke!")
    if radius_meters is None:
        # del radius_meters
        # UnboundLocalError: local variable 'radius_meters' referenced before assignment
        pass
    if place_type is None:
        raise ValueError("place_type? Nein danke!")
    if page_token is None:
        # del page_token
        pass
    if api_key is None:
        raise ValueError("api_key? Nein danke!")

    output_type = DEFAULT_OUTPUT_TYPE if output_type is None else output_type
    radius_meters = DEFAULT_RADIUS_METERS if radius_meters is None else radius_meters
    page_token = "" if page_token is None else page_token

    latitude_longitude_pair = "{latitude},{longitude}".format(
        latitude = latitude,
        longitude = longitude
    )

    query_string_parameters = {
        'location': latitude_longitude_pair,
        'radius': radius_meters,
        'type': place_type,
        'pagetoken': page_token,
        'key': api_key
    }

    uri_authority = GOOGLE_PLACES_API_HOSTNAME
    uri_path = GOOGLE_PLACES_API_BASE_PATH + NEARBY_SEARCH_ENDPOINT_PATH + "/" + output_type
    # NOTE: urlencode does not provide the URI query separator "?"
    uri_query = urlencode(query_string_parameters)
    # if not uri_query.startswith("?"):
    #     uri_query = "?" + uri_query

    nearby_search_url_string = ats_url.build_url_string(uri_authority = uri_authority,
                                                        uri_path = uri_path,
                                                        uri_query = uri_query)

    return nearby_search_url_string


def get_nearby_search(place_type_name, latitude, longitude, radius_meters, api_key):
    url = "{scheme}://{authority}{api_base_path}{api_endpoint_path}{output_type}".format(
        scheme = DEFAULT_URI_SCHEME,
        authority = GOOGLE_PLACES_API_HOSTNAME,
        api_base_path = GOOGLE_PLACES_API_BASE_PATH,
        api_endpoint_path = NEARBY_SEARCH_ENDPOINT_PATH,
        output_type = DEFAULT_OUTPUT_TYPE)
    query_string_parameters = ""

    location_coordinates = "{latitude},{longitude}".format(latitude = latitude,
                                                           longitude = longitude)
    default_url = \
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
        "?type={place_type_name}" \
        "&location={location_coordinates}" \
        "&radius={radius_meters}" \
        "&key={api_key}".format(place_type_name = place_type_name,
                                location_coordinates = location_coordinates,
                                radius_meters = radius_meters,
                                api_key = api_key)

    print("url: {}".format(url))
    print("query_string_parameters: {}".format(query_string_parameters))
    print("default_url: {}".format(default_url))


def execute_nearby_search(url):
    print("url: {}".format(url))
    pass

# Save Nearby Search Response
# |-> Save Nearby Search Response Results
#       |-> Save Nearby Search Response Result
#             |-> Save Nearby Search Response Result Photos
#                   |-> Save Nearby Search Response Result Photo


def save_nearby_search_response(mysql_connection,
                                mysql_cursor,
                                nearby_search_response,
                                http_header_date):
    """

    :param mysql_connection: [required]
    :param mysql_cursor: [required]
    :param nearby_search_response: [required]
    :type nearby_search_response: dict
    :return:
    """

    # TODO(JamesBalcomb): raise ValueError if missing required parameters
    if mysql_connection is None:
        raise ValueError("mysql_connection? Nein danke!")
    if mysql_cursor is None:
        raise ValueError("mysql_cursor? Nein danke!")
    if nearby_search_response is None:
        raise ValueError("nearby_search_response? Nein danke!")

    # html_attributions = nearby_search_response.get("html_attributions")
    # next_page_token = nearby_search_response.get("next_page_token")
    results = nearby_search_response.get("results")
    # status = nearby_search_response.get("status")

    save_nearby_search_response_results(mysql_connection, mysql_cursor, results, http_header_date)


def save_nearby_search_response_results(mysql_connection,
                                        mysql_cursor,
                                        nearby_search_response_results,
                                        http_header_date):
    """

    :param mysql_connection:
    :param mysql_cursor:
    :param nearby_search_response_results:
    :type nearby_search_response_results: list
    :return:
    """

    for nearby_search_response_result in nearby_search_response_results:
        save_nearby_search_response_result(mysql_connection,
                                           mysql_cursor,
                                           nearby_search_response_result,
                                           http_header_date)


def save_nearby_search_response_result(mysql_connection,
                                       mysql_cursor,
                                       nearby_search_response_result,
                                       http_header_date):
    """

    :param mysql_connection:
    :param mysql_cursor:
    :param nearby_search_response_result:
    :type nearby_search_response_result: dict
    :return:
    """
    # geometry = nearby_search_response_result.get("geometry")
    icon = nearby_search_response_result.get("icon")
    result_id = nearby_search_response_result.get("id")
    name = nearby_search_response_result.get("name")
    # opening_hours = nearby_search_response_result.get("opening_hours")
    photos = nearby_search_response_result.get("photos")
    place_id = nearby_search_response_result.get("place_id")
    # plus_code = nearby_search_response_result.get("plus_code")
    price_level = nearby_search_response_result.get("price_level")
    rating = nearby_search_response_result.get("rating")
    reference = nearby_search_response_result.get("reference")
    scope = nearby_search_response_result.get("scope")
    types = nearby_search_response_result.get("types")
    vicinity = nearby_search_response_result.get("vicinity")

    geometry_location_lat = \
        nearby_search_response_result.get("geometry").get("location").get("lat")
    geometry_location_lng = \
        nearby_search_response_result.get("geometry").get("location").get("lng")
    geometry_viewport_northeast_lat = \
        nearby_search_response_result.get("geometry").get("viewport").get("northeast").get("lat")
    geometry_viewport_northeast_lng = \
        nearby_search_response_result.get("geometry").get("viewport").get("northeast").get("lng")
    geometry_viewport_southwest_lat = \
        nearby_search_response_result.get("geometry").get("viewport").get("southwest").get("lat")
    geometry_viewport_southwest_lng = \
        nearby_search_response_result.get("geometry").get("viewport").get("southwest").get("lng")

    if nearby_search_response_result.get("opening_hours"):
        opening_hours_open_now = nearby_search_response_result.get("opening_hours").get("open_now")
    else:
        opening_hours_open_now = None

    if nearby_search_response_result.get("plus_code"):
        plus_code_compound_code = \
            nearby_search_response_result.get("plus_code").get("compound_code")
        plus_code_global_code = \
            nearby_search_response_result.get("plus_code").get("global_code")
    else:
        plus_code_compound_code = None
        plus_code_global_code = None

    if photos:
        save_nearby_search_response_result_photos(mysql_connection,
                                                  mysql_cursor,
                                                  place_id,
                                                  photos)

    # columns = (
    #     "geometry_location_lat",
    #     "geometry_location_lng",
    #     "geometry_viewport_northeast_lat",
    #     "geometry_viewport_northeast_lng",
    #     "geometry_viewport_southwest_lat",
    #     "geometry_viewport_southwest_lng",
    #     "icon",
    #     "result_id",
    #     "places_name",
    #     "opening_hours_open_now",
    #     "place_id",
    #     "plus_code_compound_code",
    #     "plus_code_global_code",
    #     "price_level",
    #     "rating",
    #     "reference",
    #     "scope",
    #     "place_types",
    #     "vicinity")

    values = (
        geometry_location_lat,
        geometry_location_lng,
        geometry_viewport_northeast_lat,
        geometry_viewport_northeast_lng,
        geometry_viewport_southwest_lat,
        geometry_viewport_southwest_lng,
        icon,
        result_id,
        name,
        opening_hours_open_now,
        place_id,
        plus_code_compound_code,
        plus_code_global_code,
        price_level,
        rating,
        reference,
        scope,
        str(types),
        vicinity,
        http_header_date
    )

    # ats_utilities.ats_mysql.do_mysql_insert(mysql_cursor,
    #                                         schema_name,
    #                                         table_name,
    #                                         columns,
    #                                         values)

    schema_name = "google_places_api_cacher"
    table_name = "nearby_search_result"

    sql_insert_query = "INSERT INTO {schema_name}.{table_name} (" \
                       "geometry_location_lat," \
                       "geometry_location_lng, " \
                       "geometry_viewport_northeast_lat, " \
                       "geometry_viewport_northeast_lng, " \
                       "geometry_viewport_southwest_lat, " \
                       "geometry_viewport_southwest_lng, " \
                       "icon, " \
                       "result_id, " \
                       "place_name, " \
                       "opening_hours_open_now, " \
                       "place_id, " \
                       "plus_code_compound_code, " \
                       "plus_code_global_code, " \
                       "price_level, " \
                       "rating, " \
                       "reference, " \
                       "scope, " \
                       "place_types, " \
                       "vicinity, " \
                       "record_ts" \
                       ") VALUES (" \
                       "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" \
                       ");".format(schema_name = schema_name, table_name = table_name)

    mysql_cursor.execute(sql_insert_query, values)
    # pymysql.err.InternalError: (1292,
    # "Incorrect datetime value: 'Thu, 25 Oct 2018 22:17:21 GMT' for column 'record_ts' at row 1")
    mysql_connection.commit()


def save_nearby_search_response_result_photos(mysql_connection,
                                              mysql_cursor,
                                              place_id,
                                              nearby_search_response_result_photos):

    for nearby_search_response_result_photo in nearby_search_response_result_photos:
        save_nearby_search_response_result_photo(mysql_connection,
                                                 mysql_cursor,
                                                 place_id,
                                                 nearby_search_response_result_photo)


def save_nearby_search_response_result_photo(mysql_connection,
                                             mysql_cursor,
                                             place_id,
                                             nearby_search_response_result_photo):

    photos_photo_reference = nearby_search_response_result_photo.get("photo_reference")
    photos_html_attributions = nearby_search_response_result_photo.get("html_attributions")
    photos_height = nearby_search_response_result_photo.get("height")
    photos_width = nearby_search_response_result_photo.get("width")

    # columns = (
    #     "place_id",
    #     "photos_photo_reference",
    #     "photos_html_attributions",
    #     "photos_height",
    #     "photos_width")

    values = (
        place_id,
        photos_photo_reference,
        photos_html_attributions,
        photos_height,
        photos_width
    )

    # ats_utilities.ats_mysql.do_mysql_insert(mysql_cursor,
    #                                         schema_name,
    #                                         table_name,
    #                                         columns,
    #                                         values)

    schema_name = "google_places_api_cacher"
    table_name = "nearby_search_result_photos"

    sql_insert_query = "INSERT INTO {schema_name}.{table_name} (" \
                       "place_id, " \
                       "photos_photo_reference, " \
                       "photos_html_attributions, " \
                       "photos_height, " \
                       "photos_width" \
                       ") VALUES (" \
                       "%s,%s,%s,%s,%s" \
                       ");".format(schema_name = schema_name, table_name = table_name)

    mysql_cursor.execute(sql_insert_query, values)
    mysql_connection.commit()


def find_places(location_coordinates = ("35.701474", "51.405288"),
                radius_meters = 4000,
                pagetoken = None):
    latitude_dd, longitude_dd = location_coordinates
    place_type_name = "restaurant"
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
          "?location={latitude_dd},{longitude_dd}" \
          "&radius={radius_meters}" \
          "&type={place_type_name}" \
          "&key={API_KEY}{pagetoken}".format(latitude_dd = latitude_dd,
                                             longitude_dd = longitude_dd,
                                             radius_meters = radius_meters,
                                             place_type_name = place_type_name,
                                             API_KEY = "",
                                             pagetoken = "&pagetoken=" +
                                                         pagetoken if pagetoken else "")
    print(url)
    response = requests.get(url)
    res = json.loads(response.text)
    # print(res)
    print("here results ---->>> ", len(res["results"]))

    for result in res["results"]:
        info = ";".join(map(str, [result["name"], result["geometry"]["location"]["lat"],
                                  result["geometry"]["location"]["lng"], result.get("rating", 0),
                                  result["place_id"]]))
        print(info)
    pagetoken = res.get("next_page_token", None)

    print("here -->> ", pagetoken)

    return pagetoken


def save_nearby_search_request(mysql_connection,
                               mysql_cursor,
                               api_endpoint_name,
                               place_type_name,
                               latitude,
                               longitude,
                               radius_meters,
                               results_page_number,
                               results_count,
                               url_final,
                               record_ts):

    values = (api_endpoint_name,
              place_type_name,
              latitude,
              longitude,
              radius_meters,
              results_page_number,
              results_count,
              url_final,
              record_ts)

    # schema_name = "google_places_api_cacher"
    # table_name = "nearby_search_requests"
    # INSERT_INTO_NEARBY_SEARCH_REQUESTS

    sql_insert_query = "INSERT INTO google_places_api_cacher.nearby_search_requests (" \
                       "api_endpoint_name, " \
                       "place_type_name, " \
                       "latitude, " \
                       "longitude, " \
                       "radius_meters, " \
                       "results_page_number, " \
                       "results_count, " \
                       "url_final, " \
                       "record_ts" \
                       ") VALUES (" \
                       "%s,%s,%s,%s,%s,%s,%s,%s,%s" \
                       ");"

    mysql_cursor.execute(sql_insert_query, values)
    # pymysql.err.IntegrityError: (1062, "Duplicate entry '...' for key '...'")
    # pymysql.err.DataError: (1406, "Data too long for column 'url_final' at row 1")
    mysql_connection.commit()


def get_list_of_previous_nearby_search_requests(mysql_cursor):
    sql_select_query = "SELECT " \
                       "record_id, " \
                       "api_endpoint_name, " \
                       "place_type_name, " \
                       "latitude, " \
                       "longitude, " \
                       "radius_meters, " \
                       "results_page_number, " \
                       "results_count, " \
                       "url_final, " \
                       "record_ts " \
                       "created_ts, " \
                       "updated_ts " \
                       "FROM google_places_api_cacher.nearby_search_requests " \
                       "ORDER BY NULL;"

    mysql_cursor.execute(sql_select_query)

    records = mysql_cursor.fetchall()

    print("records: {}".format(str(records)))

    row_count = mysql_cursor.rowcount

    print("row_count: {}".format(str(row_count)))

    return records


def check_for_existing_nearby_search_record(mysql_cursor = None,
                                            api_endpoint_name = None,
                                            place_type_name = None,
                                            latitude = None,
                                            longitude = None,
                                            radius_meters = None,
                                            results_page_number = None):
    """

    :param mysql_cursor: [required]
    :param api_endpoint_name:  [optional] (Default "nearby_search")
    :param place_type_name:  [required]
    :param latitude:  [required]
    :param longitude:  [required]
    :param radius_meters:  [optional] (Default: DEFAULT_RADIUS_METERS)
    :param results_page_number:  [required]
    :return:
    """

    # TODO(JamesBalcomb): raise ValueError if missing required parameters
    if mysql_cursor is None:
        raise ValueError("mysql_cursor? Nein danke!")
    if api_endpoint_name is None:
        # raise ValueError("api_endpoint_name? Nein danke!")
        pass
    if place_type_name is None:
        raise ValueError("place_type_name? Nein danke!")
    if latitude is None:
        raise ValueError("latitude? Nein danke!")
    if longitude is None:
        raise ValueError("longitude? Nein danke!")
    if radius_meters is None:
        # raise ValueError("radius_meters? Nein danke!")
        pass
    if results_page_number is None:
        # raise ValueError("results_page_number? Nein danke!")
        pass

    api_endpoint_name = "nearby_search" if api_endpoint_name is None else api_endpoint_name
    radius_meters = DEFAULT_RADIUS_METERS if radius_meters is None else radius_meters

    have_record_already = False

    sql_select_query = "SELECT " \
                       "record_id, " \
                       "api_endpoint_name, " \
                       "place_type_name, " \
                       "latitude, " \
                       "longitude, " \
                       "radius_meters, " \
                       "results_page_number, " \
                       "url_final, " \
                       "record_ts " \
                       "created_ts, " \
                       "updated_ts " \
                       "FROM google_places_api_cacher.nearby_search_requests " \
                       "WHERE " \
                       "api_endpoint_name = %s " \
                       "AND " \
                       "place_type_name = %s " \
                       "AND " \
                       "latitude = %s " \
                       "AND " \
                       "longitude = %s " \
                       "AND " \
                       "radius_meters = %s " \
                       "ORDER BY NULL;"
    # "AND " \
    # "results_page_number = %s " \

    prepared_parameters = (api_endpoint_name,
                           place_type_name,
                           latitude,
                           longitude,
                           radius_meters)
    # , results_page_number

    query_results = mysql_cursor.execute(sql_select_query, prepared_parameters)  # <class 'int'>
    # >>> query_results: 0

    records = mysql_cursor.fetchall()  # <class 'tuple'>
    # >>> records: ()

    row_count = mysql_cursor.rowcount  # <class 'int'>
    # >>> row_count: 0

    if query_results != 0:
        have_record_already = True

    # if records >= 1:
    #     have_record_already = True
    # TypeError: '>=' not supported between instances of 'tuple' and 'int'
    if not records:
        have_record_already = False

    if row_count == 0:
        have_record_already = False

    print("have_record_already: {}".format(str(have_record_already)))

    return have_record_already


def get_latitudes_and_latitudes():
    # latitudes_and_longitudes =
    # [zip(x, longitudes) for x in itertools.permutations(latitudes, len(longitudes))]

    list_of_latitudes_and_latitudes = [(x, y) for x in LATITUDES for y in LONGITUDES]

    return list_of_latitudes_and_latitudes


def save_file(data,
              endpoint_name,
              place_type_name,
              latitude,
              longitude,
              radius_meters,
              results_page_number):

    file_name = "{file_path}" \
                "{endpoint_name}" \
                "({place_type_name})" \
                "({latitude},{longitude})" \
                "({radius_meters})" \
                "({results_page_number})" \
                ".{file_extension}".format(file_path = "./saves/",
                                           endpoint_name = endpoint_name,
                                           place_type_name = place_type_name,
                                           latitude = latitude,
                                           longitude = longitude,
                                           radius_meters = radius_meters,
                                           results_page_number = results_page_number,
                                           file_extension = "json")
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)
