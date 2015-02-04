import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import Business, Category, BusinessCategory

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
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
            business = session.query(Business).filter(Business.business_id==business_line['business_id']).update(dict(category=str(business_line['categories'])))
            session.commit()

        except UnicodeEncodeError:
            print "UnicodeEncodeError"


