import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import User

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_user.json'
fp = open( os.path.join(dir, file) )

counter = 0
for line in fp:
    if line is not None or line != '':
        try:
            user_line = json.loads(line)
            user = User(user_id=user_line['user_id'],
                        name=user_line['name'],
                        user_type=str(user_line['type']),
                        review_count=user_line['review_count'],
                        average_stars=user_line['average_stars'],
                        yelping_since=user_line['yelping_since'],
                        compliments=str(user_line['compliments']),
                        elite=str(user_line['elite']),
                        votes=str(user_line['votes']))
            # print user
            session.add(user)
            session.commit()
            counter += 1
        except UnicodeEncodeError:
            print "UnicodeEncodeError"

print counter


