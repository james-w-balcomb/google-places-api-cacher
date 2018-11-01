import json
import logging
import os
import sys

import google_places_api

from ats_utilities import ats_configuration
from ats_utilities import ats_mysql
from constants import DEFAULT_LATITUDE
from constants import DEFAULT_LONGITUDE
from constants import DEFAULT_PLACE_TYPE_NAME
from constants import DEFAULT_RADIUS_METERS

TEST_RUN = False
SAVE_FILE = True
# MAXIMUM_LOOP_COUNT = 3


def test_google_places_api_cacher(sys_argv):

    # logger = logging.getLogger(__name__)
    logger = logging.getLogger('default_logger')

    # ################# #
    # Get Configuration #
    # ################# #

    configuration = ats_configuration.get_configuration(sys_argv)

    # ############# #
    # Connect MySQL #
    # ############# #

    mysql_connection = ats_mysql.get_mysql_connection(configuration)

    mysql_cursor = ats_mysql.get_mysql_cursor(mysql_connection)

    # ############################### #
    # BEGIN: Get NearbySearchResponse #
    # ############################### #

    # with open("nearby_search_response (41.878113,-87.629799)(201.168).json", "r") as file_handle:
    with open("google-places-api-nearby-search-sample.json", "r") as file_handle:
        nearby_search_response = json.load(file_handle)
    # END: with open("google-places-api-nearby-search-sample.json", "r") as file_handle:
    logger.debug("nearby_search_response: {}".format(nearby_search_response))

    # ############################# #
    # END: Get NearbySearchResponse #
    # ############################# #

    # ################################ #
    # BEGIN: Save NearbySearchResponse #
    # ################################ #

    if SAVE_FILE:
        endpoint_name = "nearby_search"
        place_type_name = DEFAULT_PLACE_TYPE_NAME
        latitude = DEFAULT_LATITUDE
        longitude = DEFAULT_LONGITUDE
        radius_meters = DEFAULT_RADIUS_METERS
        google_places_api.save_file(nearby_search_response,
                                    endpoint_name,
                                    place_type_name,
                                    latitude,
                                    longitude,
                                    radius_meters)
    # END: if SAVE_FILE:

    google_places_api.save_nearby_search_response(mysql_connection,
                                                  mysql_cursor,
                                                  nearby_search_response)

    # ############################## #
    # END: Save NearbySearchResponse #
    # ############################## #


def google_places_api_cacher(sys_argv):

    # logger = logging.getLogger(__name__)
    logger = logging.getLogger('default_logger')

    # ################# #
    # Get Configuration #
    # ################# #

    configuration = ats_configuration.get_configuration(sys_argv)

    # ############# #
    # Connect MySQL #
    # ############# #

    mysql_connection = ats_mysql.get_mysql_connection(configuration)

    mysql_cursor = ats_mysql.get_mysql_cursor(mysql_connection)

    # ######################$$# #
    # Get Google Places API Key #
    # ######################$$# #

    api_key = os.getenv('GOOGLE_PLACES_API_KEY')

    # ####################### #
    # Get List of Place Types #
    # ####################### #

    place_type_names = google_places_api.PLACE_TYPE_NAMES

    # ####################### #
    # Get List of Coordinates #
    # ####################### #

    latitudes_and_latitudes = google_places_api.get_latitudes_and_latitudes()  # <class 'list'>

    # ############################ #
    # BEGIN: Process Nearby Search #
    # ############################ #

    current_loop_count = 1

    have_record_already = False

    for place_type_name in place_type_names:  # <class 'str'>

        for latitude_and_longitude_pair in latitudes_and_latitudes:  # <class 'tuple'>

            latitude = latitude_and_longitude_pair[0]  # <class 'float'>
            longitude = latitude_and_longitude_pair[1]  # <class 'float'>

            # check_for_existing_nearby_search_record(mysql_cursor,
            #                                         api_endpoint_name,
            #                                         place_type_name,
            #                                         latitude,
            #                                         longitude,
            #                                         radius_meters,
            #                                         results_page_number)
            have_record_already = google_places_api\
                .check_for_existing_nearby_search_record(mysql_cursor,
                                                         None,
                                                         place_type_name,
                                                         latitude,
                                                         longitude,
                                                         None,
                                                         None)

            # skip to the next latitude_and_longitude_pair
            if have_record_already:
                have_record_already = False
                continue
            # END: if have_record_already:

            google_places_api.do_nearby_search(mysql_connection,
                                               mysql_cursor,
                                               latitude = latitude,
                                               longitude = longitude,
                                               place_type_name = place_type_name,
                                               api_key = api_key)

            # current_loop_count = current_loop_count + 1
            # if current_loop_count >= MAXIMUM_LOOP_COUNT:
            #     sys.exit("Mistakes were made.")

        # END: for latitude_and_longitude_pair in latitudes_and_longitudes:

    # END: for place_type_name in google_places_api.PLACE_TYPE_NAMES:

    # ########################## #
    # END: Process Nearby Search #
    # ########################## #


def main(sys_argv):

    if TEST_RUN:
        test_google_places_api_cacher(sys_argv)
    else:
        google_places_api_cacher(sys_argv)


if __name__ == '__main__':
    main(sys.argv)
