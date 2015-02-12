from gensim import corpora, models, similarities, matutils
from gensim.corpora import BleiCorpus, Dictionary
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from datetime import datetime

# Use Kullback-Leibler divergence function from scipy.stats to
# create a symmetric KL divergence measure
# Define KL function
def sym_kl(p,q):
    return np.sum([stats.entropy(p,q),stats.entropy(q,p)])


def arun(corpus, dictionary, min_topics=1, max_topics=10, step=1):
    kl = []
    for i in range(min_topics,max_topics,step):
        print "round #%d" % (i)
        print datetime.now()
        lda = models.ldamodel.LdaModel(corpus=corpus,
            id2word=dictionary,num_topics=i)
        for topic in lda.show_topics(num_topics=i):
            print '#' + str(i) + ': ' + topic
        m1 = lda.expElogbeta
        U,cm1,V = np.linalg.svd(m1)
        #Document-topic matrix
        lda_topics = lda[corpus]
        m2 = matutils.corpus2dense(lda_topics, lda.num_topics).transpose()
        cm2 = l.dot(m2)
        cm2 = cm2 + 0.0001
        cm2norm = np.linalg.norm(l)
        cm2 = cm2/cm2norm
        kl.append(sym_kl(cm1,cm2))
    return kl

dictionary_path = '/Users/ruijiang/thesis/analysis/dictionary/restaurant-review.dict'
corpus_path = '/Users/ruijiang/thesis/analysis/corpus/restaurant-review-corpus.lda-c'

print "start loading dictionary %s" % (datetime.now())
dictionary = Dictionary.load(dictionary_path)
print "start loading corpus %s" % (datetime.now())
corpus = BleiCorpus(corpus_path)
print "finish loading corpus %s" % (datetime.now())

l = np.array([sum(cnt for _, cnt in doc) for doc in corpus])
print "finish generating np array %s" % (datetime.now())

kl = arun(corpus,dictionary,max_topics=100)
print kl

# Plot kl divergence against number of topics
plt.plot(kl)
plt.ylabel('Symmetric KL Divergence')
plt.xlabel('Number of Topics')
plt.savefig('kldiv.png', bbox_inches='tight')
