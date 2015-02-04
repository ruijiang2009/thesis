import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import User, Friendship

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
            for user2 in user_line['friends']:
                friendship = Friendship(user1=user_line['user_id'], user2=user2)
                session.add(friendship)
            # user1 = session.query(User).filter(User.user_id==user_line['user_id']).first()
            # for user2 in user_line['friends']:
            #     db_user2 = session.query(User).filter(User.user_id==user2)
            #     if db_user2.count() != 0:
            #         friendship = Friendship(user1=user1.user_id, user2=user2)
            #         session.add(friendship)
            
        except UnicodeEncodeError:
            print "UnicodeEncodeError"

session.commit()