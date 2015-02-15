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
from process_data.model import Review, Business

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

# get noun per restaurant/business
def get_nouns(session, business_id):
    reviews = session.query(Review).filter(Review.business_id==business_id)
    nouns = []
    for review in reviews:
        words = json.loads(review.words)
        for word in words:
            nouns.append(word)
    return nouns

def load_model():
    lda_model_path = '/Users/ruijiang/thesis/analysis/model/restaurant-review-lda_model_22_topics.lda'
    lda = LdaModel.load(lda_model_path)
    return lda

def load_dictionary():
    dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/restaurant-review.dict'
    dictionary = corpora.Dictionary.load(dictionary_path)
    return dictionary


session = get_session()
business_ids = get_business_ids()
dictionary = load_dictionary()
lda = load_model()

# start prediction
for business_id in business_ids:
    nouns = get_nouns(session, business_id)
    bow = dictionary.doc2bow(nouns)
    review_lda = lda[bow]
    business = session.query(Business).filter(Business.business_id==business_id).first()
    business.predicted_topic_22 = json.dumps(review_lda)
    session.add(business)
    session.commit()
