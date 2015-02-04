import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_

from model import Attribute, Business, BusinessAttribute

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_business.json'
fp = open( os.path.join(dir, file) )

counter = 1
for line in fp:
    if line is not None or line != '':
        try:
            business_line = json.loads(line)
            business = session.query(Business).filter(Business.business_id==business_line['business_id']).first()
            attribute_id = -1
            attributes = business_line['attributes']
            for key in attributes:
                value = attributes[key]
                db_query = session.query(Attribute).filter(
                        and_(Attribute.name==key,
                            Attribute.value==str(value)))
                if db_query.count() != 0:
                    attribute_id = db_query.first().id
                else:
                    attribute = Attribute(id=counter, name=key, value=str(value))
                    session.add(attribute)
                    session.commit()
                    counter += 1
                    attribute_id = attribute.id

                business_attribute = BusinessAttribute(business_id=business.id,
                                                       business_bid=business.business_id,
                                                       attribute_id=attribute_id)
                session.add(business_attribute)
                session.commit()

        except UnicodeEncodeError:
            print "UnicodeEncodeError"


