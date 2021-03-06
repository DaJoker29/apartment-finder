#!/usr/bin/env python3
from scraper import do_scrape
from slackclient import SlackClient
import settings
import time
import sys
import traceback


if __name__ == "__main__":
    print("{}: Starting scrape cycle".format(time.ctime()))
    try:
        sc = SlackClient(settings.SLACK_TOKEN)

        for category in settings.CATEGORIES:
            for key in settings.SITES:
                do_scrape(key, settings.SITES[key], category)
    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit(1)
    except Exception as exc:
        print("Error with the scraping:", sys.exc_info()[0])
        traceback.print_exc()
    else:
        print("{}: Successfully finished scraping".format(time.ctime()))
