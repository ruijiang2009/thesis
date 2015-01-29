import os
import simplejson as json
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_

from model import Review, ReviewVote

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_review.json'
fp = open( os.path.join(dir, file) )


for line in fp:
    if line is not None or line != '':
        try:
            review_line = json.loads(line)
            review = Review(review_id=review_line['review_id'],
                            user_id=review_line['user_id']
                            business_id=review_line['business_id']
                            stars=review_line['stars']
                            text=review_line['text']
                            review_type=review_line['review_type']
                            date=datetime.datetime.strptime(review_line['date'] , '%Y-%m-%d'),)
            session.add(review)

            review_vote = ReviewVote(review_id=review_line['review_id'],
                                     vote='funny',
                                     number = review_line['votes']['funny'])
            session.add(review_vote)

            review_vote = ReviewVote(review_id=review_line['review_id'],
                                     vote='useful',
                                     number = review_line['votes']['useful'])
            session.add(review_vote)

            review_vote = ReviewVote(review_id=review_line['review_id'],
                                     vote='cool',
                                     number = review_line['votes']['cool'])
            session.add(review_vote)
            session.commit()

        except UnicodeEncodeError:
            print "UnicodeEncodeError"


