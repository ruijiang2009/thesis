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

def get_topic22_relationship(session, business_id):
    business = session.query(Business).filter(business_id==business_id).first()
    if business.predicted_topic_22 is not None:
        print business_id
        scores = json.loads(business.predicted_topic_22)
    relationship = {}
    for score in scores:
        relationship[score[0]] = score[1]
    return relationship

def get_topic50_relationship(session, business_id):
    business = session.query(Business).filter(business_id==business_id).first()
    scores = json.loads(business.predicted_topic_50)
    relationship = {}
    for score in scores:
        relationship[score[0]] = score[1]
    return relationship

import psycopg2
def get_topic22(business_id):
    try:
        conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    except:
        print "unable to connect"
        return None
    cur = conn.cursor()
    sql = "SELECT predicted_topic_22 FROM business WHERE business_id = '%s'" % (business_id)
    cur.execute(sql)
    rows = cur.fetchall()
    scores = json.loads(rows[0][0])
    relationship = {}
    for score in scores:
        relationship[score[0]] = score[1]
    return relationship

def get_topic50(business_id):
    try:
        conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    except:
        print "unable to connect"
        return None
    cur = conn.cursor()
    sql = "SELECT predicted_topic_50 FROM business WHERE business_id = '%s'" % (business_id)
    cur.execute(sql)
    rows = cur.fetchall()
    scores = json.loads(rows[0][0])
    relationship = {}
    for score in scores:
        relationship[score[0]] = score[1]
    return relationship

session = get_session()
business_ids = get_business_ids()

# start prediction
for business_id in business_ids:
    relationship22 = get_topic22(business_id)
    for key in relationship22:
        business_topic = BusinessTopic22(business_id=business_id, topic_id=(key+1), relationship=relationship22[key])
        session.add(business_topic)

    relationship50 = get_topic50(business_id)
    for key in relationship50:
        business_topic = BusinessTopic50(business_id=business_id, topic_id=(key+1), relationship=relationship50[key])
        session.add(business_topic)
    session.commit()

