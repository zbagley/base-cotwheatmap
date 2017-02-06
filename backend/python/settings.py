TERMS_SKI = ["CUSTOM_TERMS"]
TERMS_NED = ["CUSTOM_TERMS"]
GEOBOX = [-105.531921, 39.914345, -105.03891, 40.235247]
CO_GEOBOX = [-109.06, 36.99, -102.04, 41.0]
CONNECTION_STRING = "sqlite:///tweets.db"
JSON_NAME = "tweets.json"

TABLE1 = "coski"
TABLE2 = "geocoords"
TABLE3 = "coned"
TABLE4 = "heatmap"

try:
    from private import *
except Exception:
    pass