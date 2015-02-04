import os
import sys

from gensim import corpora, models, similarities

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import simplejson as json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append('/Users/ruijiang/thesis/')
from process_data.model import Review

import nltk



def load_stopwords():
    stopwords = {}
    with open('stopwords.txt', 'rU') as f:
        for line in f:
            stopwords[line.strip()] = 1
    return stopwords

def get_review_from_db(business_id='4bEjOyTaDG24SY5TxsaUNQ'):
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    reviews = session.query(Review).filter(Review.business_id==business_id)
    return reviews

# read review from DB
reviews = get_review_from_db()
stopwords = load_stopwords()

def get_token(reviews):
    lem = WordNetLemmatizer()
    for review in reviews:
        sentences = nltk.sent_tokenize(review.text.lower())
        words = []
        nouns = []
        for sentence in sentences:

            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

            noun_tagged_words = [word for word in words if word["pos"] in ["NN", "NNS"]]
            for word in noun_tagged_words:
                nouns.append(lem.lemmatize(word["word"]))




# stopwords = set('for a of the and to in as . , just with an'.split())
# get review for one restaurant 4bEjOyTaDG24SY5TxsaUNQ
for review in reviews:
    words = []
    # get tag from review
    sentences = nltk.sent_tokenize(review)

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        text = [word for word in tokens if word not in stopwords]
        tagged_text = nltk.pos_tag(text)

        for word, tag in tagged_text:
            words.append({"word": word, "pos": tag})

        nn_words = [for word in words if word["pos"] in ["NN", "NNS"]]



# remove common words and tokenize
stoplist = set('for a of the and to in as . , just with an'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]
# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]


print(texts)

dir = 'output_data'
file = '4bEjOyTaDG24SY5TxsaUNQ_token.txt'
fp = open(os.path.join(dir, file) , 'wb')

for text in texts:
    fp.write(str(text) + '\n')

fp.close()

