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

def get_review_from_db(session, business_id='4bEjOyTaDG24SY5TxsaUNQ'):
    reviews = session.query(Review).filter(Review.business_id==business_id)
    return reviews


def get_tokens(reviews, session, stopwords):
    lem = WordNetLemmatizer()
    corp = []
    for review in reviews:
        # tagging
        words = []
        sentences = nltk.sent_tokenize(review.text.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        review.tags = json.dumps(words)

        nouns = []
        # get NN or NNS words
        for word in words:
            if word['pos'] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word['word']))

        corp.append(nouns)
        review.words = json.dumps(nouns)

        session.add(review)
        session.commit()
        return corp
    # return corp

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
        print dictionary
        # dictionary.filter_extremes(keep_n=1000)
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


engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# preprocess reviews
reviews = get_review_from_db(session=session)
stopwords = load_stopwords()
corp = get_tokens(reviews, session, stopwords)


dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/4bEjOyTaDG24SY5TxsaUNQ.dict'
corpus_path = '/Users/ruijiang/thesis/analysis/corpus/4bEjOyTaDG24SY5TxsaUNQ-corpus.lda-c'
lda_model_path = '/Users/ruijiang/thesis/analysis/model/4bEjOyTaDG24SY5TxsaUNQ-lda_model_10_topics.lda'
lda_num_topics = 10

dictionary = Dictionary(corp, dictionary_path).build()
print dictionary
print "save dictionary"
Corpus(corp, dictionary, corpus_path).serialize()
print "save corpus"
Train.run(lda_model_path, corpus_path, lda_num_topics, dictionary)
print "finish training"

# display
lda = LdaModel.load(lda_model_path)
i = 0
for topic in lda.show_topics(num_topics=lda_num_topics):
    print '#' + str(i) + ': ' + topic
    i += 1




# # stopwords = set('for a of the and to in as . , just with an'.split())
# # get review for one restaurant 4bEjOyTaDG24SY5TxsaUNQ
# for review in reviews:
#     words = []
#     # get tag from review
#     sentences = nltk.sent_tokenize(review)

#     for sentence in sentences:
#         tokens = nltk.word_tokenize(sentence)
#         text = [word for word in tokens if word not in stopwords]
#         tagged_text = nltk.pos_tag(text)

#         for word, tag in tagged_text:
#             words.append({"word": word, "pos": tag})

#         nn_words = [for word in words if word["pos"] in ["NN", "NNS"]]



# remove common words and tokenize
# stoplist = set('for a of the and to in as . , just with an'.split())
# texts = [[word for word in document.lower().split() if word not in stoplist]
#          for document in documents]
# # remove words that appear only once
# all_tokens = sum(texts, [])
# tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
# texts = [[word for word in text if word not in tokens_once]
#          for text in texts]


# print(texts)

# dir = 'output_data'
# file = '4bEjOyTaDG24SY5TxsaUNQ_token.txt'
# fp = open(os.path.join(dir, file) , 'wb')

# for text in texts:
#     fp.write(str(text) + '\n')

# fp.close()

