import numpy as np
from sklearn import neighbors
import psycopg2
import datetime
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

business_id='4bEjOyTaDG24SY5TxsaUNQ'

n_neighbors = 15

print "start"
print datetime.datetime.now()
# create matrix for topics, using topic 50
conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
cur = conn.cursor()

# getting X
"""
training model with first 500 records
prediction with last 100 records
"""
sql = "SELECT r.user_id, COUNT(review_id) AS c  FROM review r JOIN \
(SELECT user_id FROM review WHERE business_id = '4bEjOyTaDG24SY5TxsaUNQ') t ON r.user_id=t.user_id \
GROUP BY r.user_id ORDER BY c DESC LIMIT 600;"
cur.execute(sql)
rows = cur.fetchall()

user_ids = []
for row in rows:
    user_ids.append(row[0])

print "got user_ids"
print datetime.datetime.now()

user_topic_data = [] # array [500, 50]
y_target = []

for user_id in user_ids:
    user_topics = [0] * 50
    sql = "SELECT topic_id, relationship FROM user_topic50 WHERE user_id = '%s'" % (user_id)
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        user_topics[row[0]-1] = row[1]*100

    user_topic_data.append(user_topics)

    sql = "SELECT user_id, stars FROM user_business WHERE user_id = '%s' AND business_id = '%s'" % (user_id, business_id)
    cur.execute(sql)
    row = cur.fetchall()[0]
    y_target.append(row[1])

cur.close()
conn.close()

X = np.array(user_topic_data[:500])
# X = np.array(X[:, :2])
y = np.array(y_target[:500])

print "got user data"
print datetime.datetime.now()


# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])#, '#FAAAAA', '#AAAFFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])#, '#F00000', '#00000F'])


# for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
weights = 'uniform'
clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
clf.fit(X, y)

X_predict = np.array(user_topic_data[500:])
y_actual = np.array(y_target[500:])

Z = clf.predict(X_predict)

print y_actual

print Z

print "finished"
print datetime.datetime.now()

# h = .02  # step size in the mesh
# h = 1
# for i in range (500, 599):
#     Z =

#     # Plot the decision boundary. For that, we will assign a color to each
#     # point in the mesh [x_min, m_max]x[y_min, y_max].
#     x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#     y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
#                          np.arange(y_min, y_max, h))
#     Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

#     # Put the result into a color plot
#     Z = Z.reshape(xx.shape)
#     plt.figure()
#     plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

#     # Plot also the training points
#     plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold)
#     plt.xlim(xx.min(), xx.max())
#     plt.ylim(yy.min(), yy.max())
#     plt.title("3-Class classification (k = %i, weights = '%s')"
#               % (n_neighbors, weights))

# print "finished"
# print datetime.datetime.now()

# plt.show()

