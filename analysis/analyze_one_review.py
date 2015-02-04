import nltk
from nltk.stem.wordnet import WordNetLemmatizer

import gensim
from gensim.corpora import BleiCorpus
from gensim import corpora
from gensim.models import LdaModel

class Corpus(object):
    def __init__(self, cursor, reviews_dictionary, corpus_path):
        self.cursor = cursor
        self.reviews_dictionary = reviews_dictionary
        self.corpus_path = corpus_path

    def __iter__(self):
        for review in self.cursor:
            yield self.reviews_dictionary.doc2bow(review)

    def serialize(self):
        BleiCorpus.serialize(self.corpus_path, self, id2word=self.reviews_dictionary)

        return self


class Dictionary(object):
    def __init__(self, nouns, dictionary_path):
    self.nouns = nouns
        self.dictionary_path = dictionary_path

    def build(self):
        dictionary = corpora.Dictionary(nouns)
        dictionary.filter_extremes(no_below=2,keep_n=30)
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

review = "Based on oour extensive prior extremely positive experiences, my wife and I, plus three other couples, made sure to visit MAG for a nice dinner on our final night in Vegas earlier this week.  We could have been seated immediately inside, but it was a beautiful November night and we opted to wait--heck, rolling some dice, plus free table drinks for 40 minutes, no problem. \
We finally get seated and they squeeze us into a four-top.  That's OK, we like each other and expected to be squeezed.  If you're new, be warned that they put about 250 diners in a space that any other restaurant would put 100.  For us, not a great big deal because of the anticipation of excellent food and the great view of the strip and the Bellagio water shows. \
And the aniticipation grew and grew until about an hour after ordering we finally got our meals.  The waitress explained that she had waited to talk to the chef about an allergy issue one of us had before putting any of the orders in.  I'm sorry, but when you are sitting at an uncomfortable table and will end up paying about $150/person, you shouldn't have to wait an hour to get served. "

sentences = nltk.sent_tokenize(review)

stopwords = set('for a of the and to in as . , just with an'.split())

words = []
noun_words = []

for sentence in sentences:

    tokens = nltk.word_tokenize(sentence)
    text = [word for word in tokens if word not in stopwords]
    tagged_text = nltk.pos_tag(text)

    for word, tag in tagged_text:
        words.append({"word": word, "pos": tag})

    noun_words.append([word for word in words if word["pos"] in ["NN", "NNS"]])

# print noun_words
# print len(noun_words)

lem = WordNetLemmatizer()
nouns = []
for row in noun_words:
    nouns.append([lem.lemmatize(word["word"]) for word in row])

print nouns
print len(nouns)

dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/one.dict'
corpus_path = '/Users/ruijiang/thesis/analysis/corpus/corpus.lda-c'
lda_model_path = '/Users/ruijiang/thesis/analysis/model/lda_model_10_topics.lda'
lda_num_topics = 5

dictionary = Dictionary(nouns, dictionary_path).build()
print dictionary
print "save dictionary"
Corpus(nouns, dictionary, corpus_path).serialize()
print "save corpus"
Train.run(lda_model_path, corpus_path, lda_num_topics, dictionary)
print "finish training"

# display
lda = LdaModel.load(lda_model_path)
i = 0
for topic in lda.show_topics(num_topics=lda_num_topics):
    print '#' + str(i) + ': ' + topic
    i += 1


#prediction