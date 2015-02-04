import os
import simplejson as json
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import Tip

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_tip.json'
fp = open( os.path.join(dir, file) )

counter = 0
for line in fp:
    if line is not None or line != '':
        try:
            tip_line = json.loads(line)
            tip = Tip(user_id=tip_line['user_id'],
                        business_id=tip_line['business_id'],
                        tip_type=str(tip_line['type']),
                        likes=tip_line['likes'],
                        date=datetime.datetime.strptime(tip_line['date'] , '%Y-%m-%d'),
                        text=tip_line['text'])
            # print user
            session.add(tip)
            counter += 1
        except UnicodeEncodeError:
            print "UnicodeEncodeError"

session.commit()

print counter


