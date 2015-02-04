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
from model import Business

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_business.json'
fp = open( os.path.join(dir, file) )

counter = 0
for line in fp:
    if line is not None or line != '':
        try:
            business_line = json.loads(line)
            business = Business(business_id=business_line['business_id'],
                                name=business_line['name'],
                                neighborhoods=str(business_line['neighborhoods']),
                                full_address=business_line['full_address'],
                                city=business_line['city'],
                                state=business_line['state'],
                                stars=business_line['stars'],
                                review_count=business_line['review_count'],
                                hours=str(business_line['hours']),
                                attributes=str(business_line['attributes']),
                                business_type=business_line['type'])
            session.add(business)
            session.commit()
            counter += 1
        except UnicodeEncodeError:
            print "UnicodeEncodeError"

print counter
