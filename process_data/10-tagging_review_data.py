import os
import simplejson
import json
import nltk

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from nltk.stem.wordnet import WordNetLemmatizer

from model import Review

def load_stopwords():
    stopwords = {}
    with open('stopwords.txt', 'rU') as f:
        for line in f:
            stopwords[line.strip()] = 1
    return stopwords

engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

dir = 'data'
file = 'yelp_academic_dataset_review.json'
fp = open( os.path.join(dir, file) )

stopwords = load_stopwords()
lem = WordNetLemmatizer()

for line in fp:
    if line is not None or line != '':
        try:
            review_line = simplejson.loads(line)
            review_id = review_line['review_id']
            print review_id
            review = session.query(Review).filter(Review.review_id==review_id).first()
            text = review.text

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

            review.words = json.dumps(nouns)

            session.add(review)
            session.commit()
            break

        except UnicodeEncodeError:
            print "UnicodeEncodeError"



