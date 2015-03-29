"""
yelp=# select count(distinct value) as c, name from attribute group by name order by c desc;
  c  |           name
-----+---------------------------
 153 | Ambience
 115 | Music
 100 | Good For
  75 | Hair Types Specialized In
  44 | Parking
  16 | Dietary Restrictions
   8 | Payment Types
   4 | Price Range
   4 | Noise Level
   3 | Accepts Credit Cards
   3 | Ages Allowed
   3 | Alcohol
   3 | Attire
   3 | BYOB/Corkage
   3 | Smoking
   3 | Wi-Fi
   2 | Delivery
   2 | Good For Dancing
   2 | Good For Groups
   2 | Good For Kids
   2 | Good for Kids
   2 | Corkage
   2 | Happy Hour
   2 | Has TV
   2 | Coat Check
   2 | Caters
   2 | Open 24 Hours
   2 | Order at Counter
   2 | Outdoor Seating
   2 | By Appointment Only
   2 | BYOB
   2 | Accepts Insurance
   2 | Wheelchair Accessible
   2 | Take-out
   2 | Takes Reservations
   2 | Waiter Service
   2 | Dogs Allowed
   2 | Drive-Thru
(38 rows)
Here is the general attribute from "attribute" table.
Several of them have children attribute, in order to extract those children information,
I need to import these data into new "detailed_attribute" table.
"""

import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Business, DetailedAttribute, BusinessDetailedAttribute

"""
This parsing has nothing to do with the existing attribute table.
1 get business attribute
2 json parse
3 store attribute
"""

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

session = get_session()

businesses = session.query(Business).all()
number_business = len(businesses)
counter = 1

for i in range(number_business):
    business = businesses[i]
    d = json.loads(business.attributes)
    
    if d.keys() == []:
        continue
    else:
        for key in d.keys():
            parent_attribute_name = key
            value = d[key]

            # get parent attribute id
            parent_detailed_attribute = session.query(DetailedAttribute).filter(Attribute.name==key)

            if parent_detailed_attribute.count() != 0:
                parent_attribute_id = parent_detailed_attribute.first().id
            else:
                parent_attribute = DetailedAttribute(id=counter, name=key)
                session.add(parent_attribute)
                session.commit()
                counter += 1
                parent_attribute_id = parent_attribute.id

            try:
                children = json.loads()

            except ValueError:
                print "There is no children attributes for {}".format(d[key])
                if value:
                    # save the relationship between busines sand detailed attribute
                    business_detailed_attribute = BusinessDetailedAttribute)
                
                # directly save the attribute business relationship into db
                detailed_attribute = session.query(DetailedAttribute).filter(Attribute.name==key)
                if detailed_attribute.count() != 0:
                    attribute_id = detailed_attribute.first().id
                else:
                    attribute = DetailedAttribute(id=counter, name=key)
                    session.add(attribute)
                    session.commit()
                    counter += 1
                    attribute_id = attribute.id








