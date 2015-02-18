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
from process_data.model import Review, Business, BusinessTopic22, BusinessTopic50

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def get_business_ids():
    file = 'restaurant_business_ids.txt'
    fp = open(file)
    business_ids = []
    for line in fp:
        business_ids.append(line[:22])
    return business_ids

def get_topic22_ids(session, business_id):
    business_topics = session.query(BusinessTopic22).filter(BusinessTopic22.business_id==business_id)
    topic_ids = []
    for business_topic in business_topics:
        topic_ids.append(business_topic.topic_id)
    return topic_ids

def get_topic50_ids(session, business_id):
    business_topics = session.query(BusinessTopic50).filter(BusinessTopic50.business_id==business_id)
    topic_ids = []
    for business_topic in business_topics:
        topic_ids.append(business_topic.topic_id)
    return topic_ids

# def get_topic22_stars(session, business_id, topic_id):
#     business = session.query(Business).filter(business_id==business_id).first()
#     if business.predicted_topic_22 is not None:
#         print business_id
#         scores = json.loads(business.predicted_topic_22)
#     relationship = {}
#     for score in scores:
#         relationship[score[0]] = score[1]
#     return relationship

# def get_topic50_stars(session, business_id, topic_id):
#     business = session.query(Business).filter(business_id==business_id).first()
#     scores = json.loads(business.predicted_topic_50)
#     relationship = {}
#     for score in scores:
#         relationship[score[0]] = score[1]
#     return relationship

import psycopg2
def get_topic22_star(business_id, topic_id):
    try:
        conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    except:
        print "unable to connect"
        return None
    cur = conn.cursor()
    sql = "SELECT AVG(t.stars) FROM \
           (SELECT r.review_id, r.stars AS stars \
           FROM review_topic22 rt \
           JOIN review r ON rt.review_id=r.review_id \
           WHERE business_id = '%s' AND rt.topic_id = %d) t;" % (business_id, topic_id)
    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows[0][0]

def get_topic50_star(business_id, topic_id):
    try:
        conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    except:
        print "unable to connect"
        return None
    cur = conn.cursor()
    sql = "SELECT AVG(t.stars) FROM \
           (SELECT r.review_id, r.stars AS stars \
           FROM review_topic50 rt \
           JOIN review r ON rt.review_id=r.review_id \
           WHERE business_id = '%s' AND rt.topic_id = %d) t;" % (business_id, topic_id)
    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows[0][0]

session = get_session()
business_ids = get_business_ids()

# start prediction
for business_id in business_ids:
    topic_ids = get_topic22_ids(session, business_id)
    for topic_id in topic_ids:
        business_topic = session.query(BusinessTopic22).filter(BusinessTopic22.business_id==business_id, BusinessTopic22.topic_id==topic_id).first()
        stars = get_topic22_star(business_id, topic_id)
        business_topic.stars = stars
        session.add(business_topic)

    topic_ids = get_topic50_ids(session, business_id)
    for topic_id in topic_ids:
        business_topic = session.query(BusinessTopic50).filter(BusinessTopic50.business_id==business_id, BusinessTopic50.topic_id==topic_id).first()
        stars = get_topic50_star(business_id, topic_id)
        business_topic.stars = stars
        session.add(business_topic)

    session.commit()

