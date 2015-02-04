import os
import simplejson as json
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_

from model import User, UserVote

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_user.json'
fp = open( os.path.join(dir, file) )


for line in fp:
    if line is not None or line != '':
        try:
            user_line = json.loads(line)
            user = session.query(User).filter(User.user_id==user_line['user_id']).first()
            user_vote = UserVote(user_id=user_line['user_id'],
                                     vote='funny',
                                     number = user_line['votes']['funny'])
            session.add(user_vote)

            user_vote = UserVote(user_id=user_line['user_id'],
                                     vote='useful',
                                     number = user_line['votes']['useful'])
            session.add(user_vote)

            user_vote = UserVote(user_id=user_line['user_id'],
                                     vote='cool',
                                     number = user_line['votes']['cool'])
            session.add(user_vote)
            session.commit()

        except UnicodeEncodeError:
            print "UnicodeEncodeError"


