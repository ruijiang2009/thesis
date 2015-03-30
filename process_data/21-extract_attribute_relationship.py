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

dir = 'data'
file = 'yelp_academic_dataset_business.json'
fp = open( os.path.join(dir, file) )

session = get_session()

number_business = 1
counter = 1

for line in fp:
    if line is not None or line != '':
        try:
            business_line = json.loads(line)
        except UnicodeEncodeError:
            print "UnicodeEncodeError"
        business_id = business_line['business_id']

        business = session.query(Business).filter(Business.business_id==business_id).first()
        d = business_line['attributes']
        business.attributes = json.dumps(business_line['attributes'])
        session.add(business)
        session.commit()

        for key in d.keys():
            parent_attribute_name = key
            value = d[key]

            # get parent attribute id
            parent_detailed_attribute = session.query(DetailedAttribute).filter(DetailedAttribute.name==key)

            # get parent attribute
            if parent_detailed_attribute.count() != 0:
                parent_attribute = parent_detailed_attribute.first()
            else:
                parent_attribute = DetailedAttribute(id=counter, name=key)
                session.add(parent_attribute)
                session.commit()
                counter += 1

            # see whether there is children attribute
            # if yes, then save the inforation
            # otherwise pass
            if isinstance(d[key], dict):
                c_dict = d[key]
                for c_key in c_dict.keys():
                    c_attribute_name = '.'.join([parent_attribute.name, c_key])
                    attribute = session.query(DetailedAttribute).filter(DetailedAttribute.name==c_attribute_name)
                    if attribute.count() != 0:
                        # this attribute existed already
                        da = attribute.first()
                    else:
                        # this attribute not exist
                        da = DetailedAttribute(id=counter, parent_id=parent_attribute.id, name=c_attribute_name)
                        session.add(da)
                        session.commit()
                        counter += 1
                    # store busines and attribute relationship
                    if c_dict[c_key] != False:
                        c_value = None
                        if c_dict[c_key] == True:
                            c_value = 1
                        elif isinstance(c_dict[c_key], int):
                            c_value = c_dict[c_key]
                        business_attribute = BusinessDetailedAttribute(
                                attribute_id=da.id,
                                business_id=business.business_id,
                                stars=business.stars,
                                raw_value=c_dict[c_key],
                                value=c_value
                               )

                        session.add(business_attribute)
                session.commit()
            else:
                print "There is no children attributes for {}".format(d[key])
                # save the relationship between busines sand detailed attribute
                if value != False:
                    p_value = None
                    if value == True:
                        p_value = 1
                    elif isinstance(value, int):
                        p_value = value
                    business_attribute = BusinessDetailedAttribute(
                            attribute_id=parent_attribute.id,
                            business_id=business.business_id,
                            stars=business.stars,
                            raw_value=value,
                            value=p_value)
                    session.add(business_attribute)
                    session.commit()



fp.close()

