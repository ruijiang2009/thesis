"""
This file parse the following data format.

{ 
    'type': 'business', 
    'business_id': (encrypted business id), 
    'name': (business name), 
    'neighborhoods': [(hood names)], 
    'full_address': (localized address), 
    'city': (city), 
    'state': (state), 
    'latitude': latitude, 
    'longitude': longitude, 
    'stars': (star rating, rounded to half-stars), 
    'review_count': review count, 
    'categories': [(localized category names)] 
    'open': True / False (corresponds to closed, not business hours), 
    'hours': { (day_of_week): { 'open': (HH:MM), 'close': (HH:MM) }, ... }, 
    'attributes': { (attribute_name): (attribute_value), ... }, 
}


One example is:
{
    "business_id": "vcNAWiLM4dR7D2nwwJ7nCA",
    "full_address": "4840 E Indian School Rd\nSte 101\nPhoenix, AZ 85018",
    "hours": {
        "Tuesday": {
            "close": "17:00",
            "open": "08:00"
        },
        "Friday": {
            "close": "17:00",
            "open": "08:00"
        },
        "Monday": {
            "close": "17:00",
            "open": "08:00"
        },
        "Wednesday": {
            "close": "17:00",
            "open": "08:00"
        },
        "Thursday": {
            "close": "17:00",
            "open": "08:00"
        }
    },
    "open": true,
    "categories": [
        "Doctors",
        "Health & Medical"
    ],
    "city": "Phoenix",
    "review_count": 7,
    "name": "Eric Goldberg, MD",
    "neighborhoods": [],
    "longitude": -111.98376,
    "state": "AZ",
    "stars": 3.5,
    "latitude": 33.499313,
    "attributes": {
        "By Appointment Only": true
    },
    "type": "business"
}

"""
import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Business, Category, BusinessCategory

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_business.json'
fp = open( os.path.join(dir, file) )

for line in fp:
    if line is not None or line != '':
        try:
            business_line = json.loads(line)
            business = session.query(Business).filter(Business.business_id==business_line['business_id']).first()
            category_id = -1
            for category_name in business_line['categories']:
                db_query = session.query(Category).filter(Category.name==category_name)
                if db_query.count() != 0:
                    category_id = db_query.first().id
                else:
                    category = Category(name=category_name)
                    session.add(category)
                    session.commit()
                    category_id = category.id

                business_category = BusinessCategory(business_id=business.id, category_id=category_id)
                session.add(business_category)
                session.commit()

        except UnicodeEncodeError:
            print "UnicodeEncodeError"


