
DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%Z'
# HTTP Header: Date
# The date and time that the message was originated
#  (in "HTTP-date" format as defined by RFC 7231 Date/Time Formats).
#  https://tools.ietf.org/html/rfc7231#section-7.1.1.1
# e.g., Date: Sun, 06 Nov 1994 08:49:37 GMT    ; IMF-fixdate
# import locale, datetime
# locale.setlocale(locale.LC_TIME, 'en_US')
# datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
HTTP_DATE_FORMAT = ''

DEFAULT_CONFIGURATION_FILE = "./google_places_api_cacher.ini"

DEFAULT_MYSQL_HOST_NAME = "127.0.0.1"
DEFAULT_MYSQL_PORT_NUMBER = "3306"
DEFAULT_MYSQL_CHARSET = "utf8mb4"
DEFAULT_MYSQL_STORAGE_ENGINE_NAME = "InnoDB"
DEFAULT_MYSQL_CHARACTER_SET_NAME = "utf8mb4"
DEFAULT_MYSQL_COLLATION_NAME = "utf8mb4_unicode_ci"

# Protocol AKA Scheme
DEFAULT_PROTOCOL = "https"
API_URL_PREFIX = "https://"
API_BASE_URL = "maps.googleapis.com/maps/api/place/"
FIND_PLACE_ENDPOINT_URL = "/findplacefromtext/"
NEARBY_SEARCH_ENDPOINT_URL = "/nearbysearch/"
TEXT_SEARCH_ENDPOINT_URL = "/textsearch/"
DEFAULT_API_ENDPOINT_NAME = "nearby_search"
DEFAULT_OUTPUT_TYPE = "json"
# DEFAULT_OUTPUT_TYPE = "xml"
FIND_PLACE_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/findplacefromtext/output?parameters"
NEARBY_SEARCH_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/nearbysearch/output?parameters"
TEXT_SEARCH_REQUEST_URL = \
    "https://maps.googleapis.com/maps/api/place/textsearch/output?parameters"
# DEFAULT_RADIUS_METERS = "1609.34"  # 1   || 1.0   mile = 1609.34 meters
# DEFAULT_RADIUS_METERS = "804.672"  # 1/2 || 0.5   mile =  804.672 meters
# DEFAULT_RADIUS_METERS = "402.336"  # 1/4 || 0.25  mile =  402.336 meters
DEFAULT_RADIUS_METERS = "201.168"  # 1/8 || 0.125 mile =  201.168 meters
# Formula: Miles to Meters: Miles * 1609.344 = Meters
# Formula: Miles to Nautical Miles: Miles * 1.151 = Nautical Miles
DEFAULT_LATITUDE = "41.878113"  # 41.878113, -87.629799 = Center: Chicago, Illinois
DEFAULT_LONGITUDE = "-87.629799"  # 41.878113, -87.629799 = Center: Chicago, Illinois
DEFAULT_PLACE_TYPE_NAME = "bar"

TEST_HTTP_GET_URL = "http://httpbin.org/get"

