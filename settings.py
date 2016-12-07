import os

SITES = {
  'sfbay': ["eby", "sfc", "sby", "nby", "pen", "scz"],
  'losangeles': ["wst", "sfv", "lac", "sgv", "lgb", "ant"],
  'sandiego': ["csd", "nsd", "esd", "ssd"],
  'newyork': ["mnh", "brk", "que", "brx", "stn", "jsy", "lgi", "wch", "fct"]
}

# The Craigslist section underneath housing that you want to search in.
# For instance, https://sfbay.craigslist.org/search/apa find apartments for rent.
# https://sfbay.craigslist.org/search/sub finds sublets.
# You only need the last 3 letters of the URLs.
CRAIGSLIST_CATEGORY = 'cpg'

## System settings

# How long we should sleep between scrapes of Craigslist.
# Too fast may get rate limited.
# Too slow may miss listings.
SLEEP_INTERVAL = 20 * 60 # 20 minutes

# Which slack channel to post the listings into.
SLACK_CHANNEL = "#craigslist"

# The token that allows us to connect to slack.
# Should be put in private.py, or set as an environment variable.
SLACK_TOKEN = os.getenv('SLACK_TOKEN', "")

# Any private settings are imported here.
try:
    from private import *
except Exception:
    pass

# Any external private settings are imported from here.
try:
    from config.private import *
except Exception:
    pass