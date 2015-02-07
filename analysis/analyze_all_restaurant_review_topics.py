import os
import sys
import gensim

from gensim import corpora, models, similarities

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from nltk.stem.wordnet import WordNetLemmatizer
from gensim.corpora import BleiCorpus
from gensim.models import LdaModel

sys.path.append('/Users/ruijiang/thesis/')
from process_data.model import Review

import nltk

def load_stopwords():
    stopwords = {}
    with open('stopwords.txt', 'rU') as f:
        for line in f:
            stopwords[line.strip()] = 1
    return stopwords

def get_nouns(session):
    file = 'restaurant_review_ids.txt'
    fp = open(file)
    words = []
    for line in fp:
        review = session.query(Review).filter(Review.review_id==line[:22]).first()
        words.append(json.loads(review.words))
    return words

class Corpus(object):
    def __init__(self, cursor, reviews_dictionary, corpus_path):
        self.cursor = cursor
        self.reviews_dictionary = reviews_dictionary
        self.corpus_path = corpus_path

    def __iter__(self):
        for corp in self.cursor:
            yield self.reviews_dictionary.doc2bow(corp)

    def serialize(self):
        BleiCorpus.serialize(self.corpus_path, self, id2word=self.reviews_dictionary)

        return self


class Dictionary(object):
    def __init__(self, cursor, dictionary_path):
        self.cursor = cursor
        self.dictionary_path = dictionary_path

    def build(self):
        dictionary = corpora.Dictionary(self.cursor)
        dictionary.filter_extremes(keep_n=10000)
        print dictionary
        dictionary.compactify()
        corpora.Dictionary.save(dictionary, self.dictionary_path)

        return dictionary

class Train:
    def __init__(self):
        pass

    @staticmethod
    def run(lda_model_path, corpus_path, num_topics, id2word):
        corpus = corpora.BleiCorpus(corpus_path)
        lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=id2word)
        lda.save(lda_model_path)

        return lda

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

session = get_session()
corp = get_nouns(session=session)

dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/review.dict'
corpus_path = '/Users/ruijiang/thesis/analysis/corpus/review-corpus.lda-c'
lda_model_path = '/Users/ruijiang/thesis/analysis/model/review-lda_model_50_topics.lda'
lda_num_topics = 50

dictionary = Dictionary(corp, dictionary_path).build()
print dictionary
print "saved dictionary"
Corpus(corp, dictionary, corpus_path).serialize()
print "saved corpus"
Train.run(lda_model_path, corpus_path, lda_num_topics, dictionary)
print "finish training"

print "# %d topics:" % (lda_num_topics)

# display
lda = LdaModel.load(lda_model_path)
i = 0
for topic in lda.show_topics(num_topics=lda_num_topics):
    print '#' + str(i) + ': ' + topic
    i += 1
