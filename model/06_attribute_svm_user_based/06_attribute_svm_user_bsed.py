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
2 train svm model per user basis
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

def get_user_ids(number_users=1000):
    user_ids = []
    f = open('user_id_order_by_number_visited_restaurant_desc.txt')
    for i in range(number_users):
        user_ids.append(f.readline()[-23:-1])
    f.close()
    return user_ids

def get_visited_restaurant(user_id):
    """
    get all reviewed restaurants
    90% for training, 10% for testing
    """
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    sql = \
"SELECT MAX(stars), business_id \
FROM review \
WHERE user_id = '%s'\
GROUP BY business_id" % (user_id)

    cur.execute(sql)
    rows = cur.fetchall()
    data_len = len(rows)
    training_size = int(data_len * 9 / 10)

    training_restaurant_data = []
    for i in range(training_size):
        row = rows[i]
        training_restaurant_data.append({'business_id': row[1], 'stars': row[0]})

    test_restaurant_data = []
    for i in range(training_size, data_len):
        row = rows[i]
        test_restaurant_data.append({'business_id': row[1], 'stars': row[0]})

    cur.close()
    conn.close()

    return training_restaurant_data, test_restaurant_data

# use calculated stars in business_topic table
def get_business_attribute_data(business_id):
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    sql = \
"SELECT attribute_id, stars \
FROM business_detailed_attribute \
WHERE business_id = '%s'\
ORDER BY attribute_id ASC" % (business_id)

    cur.execute(sql)
    rows = cur.fetchall()
    result = np.zeros([85])

    for row in rows:
        result[row[0]-1] = row[1]

    cur.close()
    conn.close()

    return result

# unfinished piece
def load_data(fname):
    f = open(fname)
    s = f.read()
    f.close()
    return s

def write_data(fname, data):
    f = open(fname, 'w')
    f.write(data)
    f.close()

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

def multiclass_svm(user_id):
    path = './data_90'
    training_data_fname = os.path.join(path, "training_data_{}.txt".format(user_id))
    test_data_fname = os.path.join(path, "test_data_{}.txt".format(user_id))

    if os.path.isfile(training_data_fname) and os.path.isfile(test_data_fname):
        print "{!r} and {!r} already exist".format(training_data_fname, test_data_fname)
        training_restaurant_data = json.loads(load_data(training_data_fname))
        test_restaurant_data = json.loads(load_data(test_data_fname))
    else:
        print "{!r} and {!r} does not exist".format(training_data_fname, test_data_fname)
        training_restaurant_data, test_restaurant_data = get_visited_restaurant(user_id)
        write_data(training_data_fname, json.dumps(training_restaurant_data))
        write_data(test_data_fname, json.dumps(test_restaurant_data))

    X_fname = os.path.join(path, "X_{}.txt".format(user_id))
    Y_fname = os.path.join(path, "Y_{}.txt".format(user_id))
    if os.path.isfile(X_fname) and os.path.isfile(Y_fname):
        print "{!r} and {!r} already exist".format(X_fname, Y_fname)
        X = np.loadtxt(X_fname, delimiter=',')
        Y = np.loadtxt(Y_fname, delimiter=',')
    else:
        print "{!r} and {!r} does not exist".format(X_fname, Y_fname)
        number_training_data = len(training_restaurant_data)
        Y = np.zeros([number_training_data])
        X = np.zeros([number_training_data, 85])
        for i in range(number_training_data):
            business_data = training_restaurant_data[i]
            business_id = business_data['business_id']
            business_attribute = get_business_attribute_data(business_id)
            X[i] = business_attribute
            Y[i] = business_data['stars']
        np.savetxt(fname=X_fname, X=X, delimiter=',')
        np.savetxt(fname=Y_fname, X=Y, delimiter=',')
    clf = svm.SVC()
    clf.fit(X.tolist(), Y.tolist())

    # prediction
    X_test_fname = os.path.join(path, "X_test_{}.txt".format(user_id))
    Y_prediction_fname = os.path.join(path, "Y_prediction_{}.txt".format(user_id))
    Y_actual_fname = os.path.join(path, "Y_actual_{}.txt".format(user_id))
    if os.path.isfile(X_test_fname) and os.path.isfile(Y_prediction_fname) and os.path.isfile(Y_actual_fname):
        print "{!r}, {!r} and {!r} already exist.".format(X_test_fname, Y_prediction_fname, Y_actual_fname)
        Y_prediction = np.loadtxt(Y_prediction_fname, delimiter=',')
        Y_actual = np.loadtxt(Y_actual_fname, delimiter=',')
        X_test = np.loadtxt(X_test_fname, delimiter=',')
    else:
        print "{!r}, {!r} and {!r} does not exist.".format(X_test_fname, Y_prediction_fname, Y_actual_fname)
        number_test_data = len(test_restaurant_data)
        Y_prediction = np.zeros([number_test_data])
        Y_actual = np.zeros([number_test_data])
        X_test = np.zeros([number_test_data, 85])

        for i in range(number_test_data):
            business_data = training_restaurant_data[i]
            business_id = business_data['business_id']
            business_feature = get_business_attribute_data(business_id)
            X_test[i] = business_feature
            Y_actual[i] = business_data['stars']
        Y_prediction = clf.predict(X_test.tolist())

        np.savetxt(fname=X_test_fname, X=X_test, delimiter=',')
        np.savetxt(fname=Y_prediction_fname, X=Y_prediction, delimiter=',')
        np.savetxt(fname=Y_actual_fname, X=Y_actual, delimiter=',')

    return Y_actual.tolist(), Y_prediction.tolist()

number_users = 1000
user_ids = get_user_ids(number_users)

# Method 1. calculate MSE accross all the businesses
# Method 2. calculate MSE for each business, then average them
total_actual = []
total_prediction = []
total_mse = []
for user_id in user_ids:
    print "user_id {}".format(user_id)
    Y_actual, Y_prediction = multiclass_svm(user_id)
    total_actual.extend(Y_actual)
    total_prediction.extend(Y_prediction)
    total_mse.append(mse(Y_actual, Y_prediction))

# Method 1:
mse1 = mse(total_actual, total_prediction)
print "total # prediction is {}".format(len(total_actual))
print "method 1 MSE is {!r}".format(mse1)

# Method
mse2 = np.mean(total_mse)
print "method 2 MSE is {!r}".format(mse2)
