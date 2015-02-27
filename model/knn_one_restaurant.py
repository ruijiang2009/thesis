import numpy as np
from sklearn import neighbors
import psycopg2
import datetime
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

# mean of squared error
def mse(x, y):
    n = len(x)
    sum = 0
    for i in range(n):
        sum += (x[i] - y[i]) * (x[i] - y[i])
    return sum / n

business_id='4bEjOyTaDG24SY5TxsaUNQ'

n_neighbors = 15

# return X and y
def get_data():
    print "%s start get_data" % (datetime.datetime.now())
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

    print "%s got user_ids" % (datetime.datetime.now())

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

    print "%s got data" % (datetime.datetime.now())
    return (X, y, y_target, user_topic_data)


X, y, y_target, user_topic_data = get_data()
# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])#, '#FAAAAA', '#AAAFFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])#, '#F00000', '#00000F'])


# for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
weights = 'uniform'
y_actual = np.array(y_target[500:])
mse_array = []

max_n_neighbors = 51

for n_neighbors in range(1, max_n_neighbors):
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    X_predict = np.array(user_topic_data[500:])
    Z = clf.predict(X_predict)
    mse_array.append(mse(Z, y_actual))

print "finished"
print datetime.datetime.now()

print mse_array

y_axe = [e for e in range (1, max_n_neighbors)]
plt.plot(y_axe, mse_array)
plt.xlabel('# neighbors')
plt.ylabel('mse=mean squared error')
plt.title('knn mse relationship')
plt.show()
