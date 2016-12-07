from craigslist import CraigslistGigs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse
from util import post_listing_to_slack
from slackclient import SlackClient
import time
import settings

engine = create_engine('sqlite:///gigs.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'gigs'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    name = Column(String)
    location = Column(String)
    cl_id = Column(Integer, unique=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def scrape_area(site, area):
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_h = CraigslistGigs(site=site, area=area, category=settings.CRAIGSLIST_CATEGORY,
                             filters={'is_paid': 'yes', 'query': 'website'})

    results = []
    gen = cl_h.get_results(sort_by='newest', limit=20)
    while True:
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            if result["where"] is None:
                # If there is no string identifying which neighborhood the result is from, skip it.
                result["where"] = "N/A"

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                created=parse(result["datetime"]),
                name=result["name"],
                location=result["where"],
                cl_id=result["id"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()

            # Return the results
            results.append(result)

    return results

def do_scrape(site, areas):
    """
    Runs the craigslist scraper, and posts data to slack.
    """

    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = []
    for area in areas:
        all_results += scrape_area(site, area)

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post each result to slack.
    for result in all_results:
        post_listing_to_slack(sc, result)
