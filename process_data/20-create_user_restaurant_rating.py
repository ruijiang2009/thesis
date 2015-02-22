# fill predicted_topic_50 column in business table
# this prediction is based on 50 topic


import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import Review

from gensim.models import LdaModel
from gensim import corpora

import sys
sys.path.append('/Users/ruijiang/thesis/')
from process_data.model import Review, UserBusiness

import psycopg2

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def get_user_business_pair():
    try:
        conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    except:
        print "unable to connect"
        return None
    pairs = dict()
    cur = conn.cursor()
    sql = "SELECT user_id, business_id, AVG(stars) AS stars FROM review GROUP BY user_id, business_id;"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        pairs[(row[0], row[1])] = row[2]
    cur.close()
    conn.close()
    return pairs

session = get_session()
pairs = get_user_business_pair()

for key in pairs:
    user_id = key[0]
    business_id = key[1]
    stars = pairs[key]
    user_business = UserBusiness(user_id=user_id, business_id=business_id, stars=stars)
    session.add(user_business)
    session.commit()

