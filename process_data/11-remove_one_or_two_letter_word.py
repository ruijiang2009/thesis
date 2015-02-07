import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import Review

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

file = 'review_ids.txt'
fp = open(file)

i = 0
for review_id in fp:
    if review_id is not None or line != '':
        try:
            review_id = review_id[:22]
            review = session.query(Review).filter(Review.review_id==review_id).first()
            words = json.loads(review.words)
            filtered_words = [word for word in words if len(word) > 2]
            review.words = json.dumps(filtered_words)
            session.add(review)
            session.commit()
            i += 1
            # print "index %d review_id %s " % (i, review_id)

        except UnicodeEncodeError:
            print "UnicodeEncodeError"