
import os
import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from model import Review

from gensim.models import LdaModel
from gensim import corpora

import sys
sys.path.append('/Users/ruijiang/thesis/')
from process_data.model import Review, ReviewTopic22, ReviewTopic50

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def get_restaurant_review_ids():
    file = 'restaurant_review_ids.txt'
    fp = open(file)
    review_ids = []
    for line in fp:
        review_ids.append(line[:22])
    return review_ids

# get noun per restaurant/business
def get_nouns(session, review_id):
    review = session.query(Review).filter(Review.review_id==review_id).first()
    nouns = []
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
review_ids = get_restaurant_review_ids()
dictionary = load_dictionary()
lda22 = load_22model()
lda50 = load_50model()

# start prediction
for review_id in review_ids:
    nouns = get_nouns(session, review_id)
    bow = dictionary.doc2bow(nouns)
    review_lda22 = lda22[bow]
    review_lda50 = lda50[bow]

    review = session.query(Review).filter(Review.review_id==review_id).first()
    review.predicted_topic_50 = json.dumps(review_lda50)
    review.predicted_topic_22 = json.dumps(review_lda22)
    session.add(review)

    for review_score in review_lda22:
        review_topic22 = ReviewTopic22(review_id=review_id,
                                       topic_id=review_score[0]+1,
                                       relationship=review_score[1],
                                       stars=review.stars)
        session.add(review_topic22)

    for review_score in review_lda50:
        review_topic50 = ReviewTopic50(review_id=review_id,
                                       topic_id=review_score[0]+1,
                                       relationship=review_score[1],
                                       stars=review.stars)
        session.add(review_topic50)
    session.commit()
