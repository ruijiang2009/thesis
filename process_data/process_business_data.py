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
import simplejson

from sqlalchemy import Column, Integer, String


class Business(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

dir = 'process_data/data'
file = 'yelp_academic_dataset_business'
fp = open( os.path.join(dir, file) )
for line in fp:
    business = json.loads(line)





