import logging

from gensim.models import LdaModel
from gensim import corpora
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import simplejson as json

import sys
sys.path.append('/Users/ruijiang/thesis/')
from process_data.model import Review

class Predict():
    def __init__(self):
        dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/restaurant-review.dict'
        lda_model_path = '/Users/ruijiang/thesis/analysis/model/restaurant-review-lda_model_50_topics.lda'
        print "load dictionary"
        self.dictionary = corpora.Dictionary.load(dictionary_path)
        self.lda = LdaModel.load(lda_model_path)

    def load_stopwords(self):
        stopwords = {}
        with open('stopwords.txt', 'rU') as f:
            for line in f:
                stopwords[line.strip()] = 1

        return stopwords

    def extract_lemmatized_nouns(self, new_review):
        stopwords = self.load_stopwords()
        words = []

        sentences = nltk.sent_tokenize(new_review.lower())
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            text = [word for word in tokens if word not in stopwords]
            tagged_text = nltk.pos_tag(text)

            for word, tag in tagged_text:
                words.append({"word": word, "pos": tag})

        lem = WordNetLemmatizer()
        nouns = []
        for word in words:
            if word["pos"] in ["NN", "NNS"]:
                nouns.append(lem.lemmatize(word["word"]))

        return nouns

    def extract_nouns(self, new_words):
        nouns = []
        for word in new_words:
            ns = json.loads(word)
            for n in ns:
                nouns.append(n)

        return nouns

    def run(self, new_review):

        # nouns = self.extract_lemmatized_nouns(new_review)
        nouns = self.extract_nouns(new_review)
        new_review_bow = self.dictionary.doc2bow(nouns)
        new_review_lda = self.lda[new_review_bow]

        print new_review_lda

def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    session = get_session()
    file = '4bEjOyTaDG24SY5TxsaUNQ_restaurant_review_ids.txt'
    print "open file %s" % (file)
    fp = open(file)
    texts = []
    for line in fp:
        review = session.query(Review).filter(Review.review_id==line[:22]).first()
        texts.append(review.words)
    # new_review = '\n'.join(texts)

    # new_review = "It's like eating with a big Italian family. " \
    #              "Great, authentic Italian food, good advice when asked, and terrific service. " \
    #              "With a party of 9, last minute on a Saturday night, we were sat within 15 minutes. " \
    #              "The owner chatted with our kids, and made us feel at home. " \
    #              "They have meat-filled raviolis, which I can never find. " \
    #              "The Fettuccine Alfredo was delicious. We had just about every dessert on the menu. " \
    #              "The tiramisu had only a hint of coffee, the cannoli was not overly sweet, " \
    #              "and they had this custard with wine that was so strangely good. " \
    #              "It was an overall great experience!"

    predict = Predict()
    predict.run(texts)


if __name__ == '__main__':
    main()


