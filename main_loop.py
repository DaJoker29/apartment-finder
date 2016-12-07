#!/usr/bin/env python3
from scraper import do_scrape
import settings
import time
import sys
import traceback

if __name__ == "__main__":
    print("{}: Starting scrape cycle".format(time.ctime()))
    try:
        for key in settings.SITES:
            do_scrape(key, settings.SITES[key])
    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit(1)
    except Exception as exc:
        print("Error with the scraping:", sys.exc_info()[0])
        traceback.print_exc()
    else:
        print("{}: Successfully finished scraping".format(time.ctime()))
