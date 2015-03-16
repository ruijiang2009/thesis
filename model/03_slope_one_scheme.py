import psycopg2
import numpy as np
import math
from scipy.stats import pearsonr

def get_data(number_user=3000, number_restaurant=300):
    sql = "SELECT stars, user_id, business_id \
    FROM review r  \
    WHERE user_id IN ( \
        SELECT user_id \
        FROM ( \
            SELECT COUNT(review_id) AS review_count, user_id  \
            FROM review r WHERE business_id IN \
            (SELECT business_id \
            FROM \
            (SELECT COUNT(r.review_id) c, r.business_id \
            FROM review r \
            JOIN business b ON r.business_id=b.business_id \
            JOIN business_category bc ON bc.business_id=b.id \
            WHERE bc.category_id=3 \
            GROUP BY r.business_id \
            ORDER BY c DESC) t \
            LIMIT %d) \
        GROUP BY r.user_id \
        ORDER BY review_count DESC \
        LIMIT %d) s) \
    AND business_id IN \
        (SELECT business_id \
        FROM \
        (SELECT COUNT(r.review_id) c, r.business_id \
        FROM review r \
        JOIN business b ON r.business_id=b.business_id \
        JOIN business_category bc ON bc.business_id=b.id \
        WHERE bc.category_id=3 \
        GROUP BY r.business_id \
        ORDER BY c DESC) s \
        LIMIT %d);" % (number_restaurant, number_user, number_restaurant)

    print sql

    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    data_len = len(rows)

    training_size = int(data_len * 9 / 10)
    print "training size: {}".format(training_size)
    print "test size: {}".format(data_len - training_size)
    business_index_map = {}
    user_index_map = {}
    user_item_training_matrix = np.zeros([number_user, number_restaurant])
    user_item_test_matrix = np.zeros([number_user, number_restaurant])

    recorded_user = 0
    recorded_business = 0

    for i in range(training_size):
        row = rows[i]
        business_id = row[2]
        user_id = row[1]
        stars = row[0]
        if user_id not in user_index_map:
            user_index_map[user_id] = recorded_user
            recorded_user += 1
        user_index = user_index_map[user_id]
        if business_id not in business_index_map:
            business_index_map[business_id] = recorded_business
            recorded_business += 1
        business_index = business_index_map[business_id]
        user_item_training_matrix[user_index][business_index] = stars

    for i in range(training_size, data_len):
        row = rows[i]
        business_id = row[2]
        user_id = row[1]
        stars = row[0]
        if user_id not in user_index_map:
            user_index_map[user_id] = recorded_user
            recorded_user += 1
        user_index = user_index_map[user_id]
        if business_id not in business_index_map:
            business_index_map[business_id] = recorded_business
            recorded_business += 1
        business_index = business_index_map[business_id]
        user_item_test_matrix[user_index][business_index] = stars

    cur.close()
    conn.close()

    print "finished getting training and test data"
    return user_item_training_matrix, user_item_test_matrix

def avg_deviation(user_item_matrix, item_i, item_j):
    height = len(user_item_matrix)
    width = len(user_item_matrix[0])
    counter = 0
    deviation_sum = 0
    for user in range(height):
        if user_item_matrix[user][item_i] != 0 and user_item_matrix[user][item_j] != 0:
            counter += 1
            deviation_sum += user_item_matrix[user][item_i] - user_item_matrix[user][item_j]
    if counter == 0:
        return 0, 0
    # print 'deviation_sum: {} counter: {}'.format(deviation_sum, counter)
    return deviation_sum / counter, counter

def get_item_deviation_matrix(user_item_matrix):
    width = len(user_item_matrix[0])
    print "width {}".format(width)
    deviation_matrix = np.zeros([width, width])
    card_matrix = np.zeros([width, width]) # how many common user between item i and item j

    for i in range(width):
        for j in range(width):
            if j > i:
                deviation_matrix[i][j], card_matrix[i][j] = avg_deviation(user_item_matrix, i, j)
            else:
                deviation_matrix[i][j] = deviation_matrix[j][i]
                card_matrix[i][j] = card_matrix[j][i]
    return deviation_matrix, card_matrix

def predict(user_item_matrix, item_deviation_matrix, card_matrix, user_index, item_index):
    height = len(user_item_matrix)
    width = len(user_item_matrix[0])

    # find value card(Rj)
    card_Rj = 0
    item_list = []
    for item in range(width):
        if item != item_index:
            if user_item_matrix[user_index][item] > 0 and card_matrix[item_index][item] > 0:
                card_Rj += 1
                item_list.append(item)

    if card_Rj == 0:
        return np.nan

    prediction = 0

    for item in item_list:
        prediction += item_deviation_matrix[item_index][item] + user_item_matrix[user_index][item]

    return prediction / card_Rj

def mse(prediction, test):
    height = len(prediction)
    width = len(prediction[0])
    s = 0.0
    counter = 0
    for i in range(height):
        for j in range(width):
            if prediction[i][j] > 0:
                print "actual: {} predicion: {}".format(test[i][j], prediction[i][j])
                diff = pow(prediction[i][j] - test[i][j], 2)
                s += diff
                counter += 1
    print "{} is sum".format(s)
    print "{} # prediction".format(counter)
    return math.sqrt(s / counter)


number_restaurant = 300
number_reviewer = 30000

import os.path

prefix = 'slope_one_'

user_item_training_matrix_fname = prefix + 'user_item_training_matrix.txt'
user_item_test_matrix_fname = prefix + 'user_item_test_matrix.txt'
if os.path.isfile(user_item_training_matrix_fname) and os.path.isfile(user_item_test_matrix_fname):
    user_item_training_matrix = np.loadtxt(user_item_training_matrix_fname, delimiter=',')
    user_item_test_matrix = np.loadtxt(user_item_test_matrix_fname, delimiter=',')
else:
    user_item_training_matrix, user_item_test_matrix = get_data(number_user=number_reviewer, number_restaurant=number_restaurant)
    np.savetxt(fname=user_item_training_matrix_fname, X=user_item_training_matrix, delimiter=',', header=prefix+user_item_training_matrix_fname[:-4])
    np.savetxt(fname=user_item_test_matrix_fname, X=user_item_test_matrix, delimiter=',', header=prefix+user_item_test_matrix_fname[:-4])

user_item_predict_matrix_fname = prefix +'user_item_predict_matrix.txt'
item_deviation_matrix_fname = prefix + 'item_deviation_matrix.txt'
item_card_matrix_fname = prefix + 'item_card_matrix.txt'

if os.path.isfile(item_deviation_matrix_fname) and os.path.isfile(item_card_matrix_fname):
    print "load existing {}".format(item_deviation_matrix_fname)
    print "load existing {}".format(item_card_matrix_fname)
    item_deviation_matrix = np.loadtxt(item_deviation_matrix_fname, delimiter=',')
    item_card_matrix = np.loadtxt(item_card_matrix_fname, delimiter=',')
else:
    print "{} does not exist".format(user_item_predict_matrix_fname)
    item_deviation_matrix, item_card_matrix = get_item_deviation_matrix(user_item_training_matrix)
    np.savetxt(fname=item_deviation_matrix_fname, X=item_deviation_matrix, delimiter=',', header=prefix+item_deviation_matrix_fname[:-4])
    np.savetxt(fname=item_card_matrix_fname, X=item_card_matrix, delimiter=',', header=prefix+item_card_matrix_fname[:-4])

if os.path.isfile(user_item_predict_matrix_fname):
    print "load existing {}".format(user_item_predict_matrix_fname)
    user_item_predict_matrix = np.loadtxt(user_item_predict_matrix_fname, delimiter=',')
else:
    print "{} does not exist".format(user_item_predict_matrix_fname)
    user_item_predict_matrix = np.zeros([number_reviewer, number_restaurant])
    for user in range(number_reviewer):
        for item in range(number_restaurant):
            if user_item_test_matrix[user][item] > 0:
                user_item_predict_matrix[user][item] = predict(user_item_training_matrix, item_deviation_matrix, item_card_matrix, user, item)
                if user_item_predict_matrix[user][item] != 0.0:
                    print "user: {} item: {} prediction: {} actual: {}".format(user, item, user_item_predict_matrix[user][item], user_item_test_matrix[user][item])
        np.savetxt(fname=user_item_predict_matrix_fname, X=user_item_predict_matrix, delimiter=',', header=prefix+user_item_predict_matrix_fname[:-4])

# # # calculate MSE between user_item_predict_matrix and user_item_test_matrix
m = mse(user_item_predict_matrix, user_item_test_matrix)

print m

