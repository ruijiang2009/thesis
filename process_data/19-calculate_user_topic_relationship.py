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
from process_data.model import Review, User, UserTopic22, UserTopic50

import psycopg2

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

# get the user who has comment on restaurant
def get_user_ids():
    file = 'user_ids.txt'
    fp = open(file)
    user_ids = []
    for line in fp:
        user_ids.append(line[:22])
    return user_ids

def get_review_ids(user_id):
    try:
        conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    except:
        print "unable to connect"
        return None
    review_ids = []
    cur = conn.cursor()
    sql = "SELECT r.review_id FROM review r \
           JOIN business b ON r.business_id = b.business_id \
           JOIN business_category bc ON b.id = bc.business_id \
           WHERE bc.category_id=3 AND r.user_id = '%s'" % (user_id)
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        review_ids.append(row[0])
    cur.close()
    conn.close()
    return review_ids

def get_nouns(review_ids):
    nouns = []
    for review_id in review_ids:
        review = session.query(Review).filter(Review.review_id==review_id).first()
        words = json.loads(review.words)
        for word in words:
            nouns.append(word)
    return nouns

def load_50model():
    lda_model_path = '/Users/ruijiang/thesis/analysis/model/restaurant-review-lda_model_50_topics.lda'
    lda = LdaModel.load(lda_model_path)
    return lda

def load_22model():
    lda_model_path = '/Users/ruijiang/thesis/analysis/model/restaurant-review-lda_model_22_topics.lda'
    lda = LdaModel.load(lda_model_path)
    return lda


def load_dictionary():
    dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/restaurant-review.dict'
    dictionary = corpora.Dictionary.load(dictionary_path)
    return dictionary


session = get_session()
user_ids = get_user_ids()
dictionary = load_dictionary()
lda22 = load_22model()
lda50 = load_50model()

# start prediction
for user_id in user_ids:
    review_ids = get_review_ids(user_id)
    nouns = get_nouns(review_ids)
    bow = dictionary.doc2bow(nouns)
    review_lda22 = lda22[bow]
    review_lda50 = lda50[bow]
    user = session.query(User).filter(User.user_id==user_id).first()
    user.predicted_topic_50 = json.dumps(review_lda50)
    user.predicted_topic_22 = json.dumps(review_lda22)
    session.add(user)
    for topic in review_lda22:
        user_topic22 = UserTopic22(user_id=user_id, topic_id=(topic[0]+1), relationship=topic[1])
        session.add(user_topic22)

    for topic in review_lda50:
        user_topic50 = UserTopic50(user_id=user_id, topic_id=(topic[0]+1), relationship=topic[1])
        session.add(user_topic50)

    session.commit()
