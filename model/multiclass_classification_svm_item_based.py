# user based multiclass SVM method
# based on the following link
# http://scikit-learn.org/stable/modules/svm.html
# will train a model per user basis.
# then given a 
import psycopg2
import numpy as np
import math
import os
import json
from sklearn import svm
"""
1 get data from db
2 train svm model per item basis
3 save it in database
4 prediction
"""

"""
-- how many reviewer per restaurants
SELECT COUNT(DISTINCT r.user_id) as c, r.business_id
FROM review r
JOIN business b ON r.business_id=b.business_id
JOIN business_category bc ON bc.business_id=b.id
WHERE bc.category_id=3
GROUP BY r.business_id
ORDER BY c DESC;
The result is saved in 'restaurant_id_order_by_number_reviewers_desc.txt'

-- how many restaurants have been reviewed per user.
SELECT COUNT(DISTINCT r.business_id) as c, user_id
FROM review r
JOIN business b ON r.business_id=b.business_id
JOIN business_category bc ON bc.business_id=b.id
WHERE bc.category_id=3
GROUP BY user_id
ORDER BY c DESC
LIMIT 2000;
The result is saved in 'user_id_order_by_number_visited_restaurant_desc.txt'
"""

def get_business_ids(number_items=300):
    business_ids = []
    f = open('restaurant_id_order_by_number_reviewers_desc.txt', 'r')
    for i in range(number_items):
        business_ids.append(f.readline())
    f.close()
    return business_ids

def get_reviewers_for_one_restaurant(business_id):
    """
    get all the reviewers from one restaurant
    90% for training, 10% for testing
    """
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    sql = \
"SELECT MAX(stars), user_id \
FROM review \
WHERE business_id = '%s'\
GROUP BY user_id" % (business_id)

    cur.execute(sql)
    rows = cur.fetchall()
    data_len = len(rows)
    training_size = int(data_len * 9 / 10)

    training_user_data = []
    for i in range(training_size):
        row = rows[i]
        training_user_data.append({'user_id': row[1], 'stars': row[0]})

    test_user_data = []
    for i in range(training_size, data_len):
        row = rows[i]
        test_user_data.append({'user_id': row[1], 'stars': row[0]})

    cur.close()
    conn.close()

    return training_user_data, test_user_data

# take topic 22 as example
def get_user_feature_data(user_id):
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    sql = \
"SELECT topic_id, relationship \
FROM user_topic22 \
WHERE user_id = '%s'\
ORDER BY topic_id ASC" % (user_id)

    cur.execute(sql)
    rows = cur.fetchall()
    result = np.zeros([22])

    for row in rows:
        result[row[0]-1] = row[1]

    cur.close()
    conn.close()

    return result

def load_data(fname):
    f = open(fname)
    s = f.read()
    f.close()
    return s

def mse(prediction, actual):
    n = len(prediction)
    print "{} # prediction".format(n)
    s = 0.0
    for i in range(n):
        diff = prediction[i] - actual[i]
        s += pow(diff, 2)
    m = math.sqrt(s / n)
    print "mse is {}".format(m)
    return m

def multiclass_svm(business_id):
    training_data_fname = "training_data_{}.txt".format(business_id)
    test_data_fname = "test_data_{}.txt".format(business_id)

    if os.path.isfile(training_data_fname) and os.path.isfile(test_data_fname):
        training_user_data = json.loads(load_data(training_data_fname))
        test_user_data = json.loads(load_data(test_data_fname))
    else:
        training_user_data, test_user_data = get_reviewers_for_one_restaurant(business_id)

    number_training_data = len(training_user_data)
    Y = np.zeros([number_training_data])
    X = np.zeros([number_training_data, 22])
    for i in range(number_training_data):
        user_data = training_user_data[i]
        user_id = user_data['user_id']
        user_feature = get_user_feature_data(user_id)
        X[i] = user_feature
        Y[i] = user_data['stars']
    cls = svm.SVC()
    clf.fit(X.tolist(), Y.toList())

    # prediction
    number_test_data = len(test_user_data)
    Y_prediction = np.zeros([number_test_data])
    Y_actual = np.zeros([number_test_data])
    X_test = np.zeros([number_test_data, 22])

    for i in range(number_test_data):
        user_data = test_user_data[i]
        user_id = user_data['user_id']
        user_feature = get_user_feature_data(user_id)
        X_test[i] = user_feature
        Y_actual[i] = user_data['stars']
    prediction = cls.predict(X_test.tolist())
    Y_prediction = prediction.tolist()

    prediction_fname = "prediction_{}.txt".format(business_id)
    actual_fname = "actual_{}.txt".format(business_id)
    np.savetxt(fname=prediction_fname, X=prediction, delimiter=',')
    np.savetxt(fname=actual_fname, X=Y_actual, delimiter=',')
    mse(Y_actual.tolist(), Y_prediction)


business_id = '4bEjOyTaDG24SY5TxsaUNQ'
multiclass_svm(business_id)