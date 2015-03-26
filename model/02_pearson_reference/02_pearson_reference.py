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

def get_business_ids(number_restaurant=300):
    business_ids = []
    business_index = {}
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    # get top 300 reviewed restaurants
    sql = "SELECT COUNT(r.review_id) c, r.business_id \
        FROM review r \
        JOIN business b ON r.business_id=b.business_id \
        JOIN business_category bc ON bc.business_id=b.id \
        WHERE bc.category_id=3 \
        GROUP BY r.business_id \
        ORDER BY c DESC) t \
        LIMIT %d" % (number_restaurant)
    cur.execute(sql)
    rows = cur.fetchall()
    index = 0
    for row in rows:
        business_ids.append(row[1])
        business_index[row[1]] = index
        index += 1
    cur.close()
    conn.close()
    return business_ids, business_index

def get_user_ids(number_restaurant=300, number_reviewer=3000):
    user_ids = []
    user_index = {}
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    # get top 300 reviewed restaurants
    sql = "SELECT COUNT(review_id) as review_count, user_id \
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
    ORDER BY review_count DESC\
    LIMIT %d;" % (number_restaurant, number_reviewer)
    cur.execute(sql)
    rows = cur.fetchall()
    index = 0
    for row in rows:
        user_ids.append(row[1])
        user_index[row[1]] = index
        index += 1
    cur.close()
    conn.close()
    return user_ids

def get_matrix(business_index_map, user_ids):
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()
    number_items = len(business_index_map)
    number_users = len(user_ids)
    user_item_matrix = []

    for user_id in user_ids:
        user_evaluation =[0] * number_items
        for key in business_index_map:
            index = business_index_map[key]
            # find the review star for user and business
            sql = "SELECT AVG(stars) FROM review WHERE user_id = '%s' AND business_id = '%s'" % (user_id, key)
            cur.execute(sql)
            rows = cur.fetchall
            user_evaluation[index] = rows[0][0]
        user_item_matrix.append(user_evaluation)

    cur.close()
    conn.close()

    return user_item_matrix

# u and v are two lists
# the calculation is based on the following link
# http://grouplens.org/similarity-functions-for-user-user-collaborative-filtering/
def similarity_measure(u, v):
    # fine the intersection between u and v

    intersection = []
    for i in range(len(u)):
        if u[i] != 0 and v[i] != 0:
            intersection.append(i)
    if len(intersection) == 0:
        return 0

    usum = .0
    vsum = .0
    for i in intersection:
        usum += u[i]
        vsum += v[i]

    umean = usum / len(intersection)
    vmean = vsum / len(intersection)

    numerator = .0
    for i in intersection:
        numerator += (u[i] - umean) * (v[i] - vmean)

    udenominator = .0
    vdenominator = .0
    for i in intersection:
        udenominator += pow((u[i] - umean), 2)
        vdenominator += pow((v[i] - vmean), 2)

    denominator = math.sqrt(udenominator) * math.sqrt(vdenominator)

    if denominator == 0:
        return 0
    corr = number_restaurant / denominator
    rho = 2.5 # case amplication
    return corr * pow(abs(corr), rho)
    # old way or wrong way to calculate
    # try:
    #     corr = pearsonr(u, v)
    #     rho = 2.5 # based in paper
    #     if np.isnan(corr[0]):
    #         return 0
    #     r = corr[0] * pow(abs(corr[0]), rho)
    #     return r
    # except np.seterr as e:
    #     print "np.seterr {}".format(e)
    #     return None
    # except:
    #     print "Unexpected Error"
    #     return None

def similarity_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    smatrix = np.zeros([rows, rows])

    for i in range(rows):
        for j in range(rows):
            if i != j and i < j:
                smatrix[i][j] = similarity_measure(matrix[i], matrix[j])
            else:
                smatrix[i][j] = smatrix[j][i]
    return smatrix

# def get_similarity_matrix(training_matrix):
#     similarity_matrix = []
#     number_user = len(user_item_matrix)
#     for i in range(number_user):
#         user_similarity = [0] * number_user
#         for j in range(number_user):
#             if j > i:
#                 user_similarity[j] = similarity_measure(user_item_matrix[i], user_item_matrix[i])
#             else:
#                 user_similarity[j] = similarity_matrix[j][i]
#         similarity_matrix.append(user_similarity)
#     return similarity_matrix

# only take average of rated item, u is a list of rating
def mean(u):
    counter = .0
    sum = .0
    for i in range(len(u)):
        if u[i] != 0:
            counter += 1
            sum += u[i]
    if counter == 0:
        return 0
    return sum / counter

# bias from mean = vector[index] - main(vector)
def bias_from_mean(vector, index):
    # vector should be numpy array []
    return vector[index] - mean(vector)

def predict(user_item_matrix, user_similarity, user_index, item_index):
    # user_mean = np.average(user_item_matrix[user_index])
    user_mean = mean(user_item_matrix[user_index])
    # print "user_index: {} user_mean: {}".format(user_index, user_mean)
    height = len(user_item_matrix)
    width = len(user_item_matrix[0])

    sum_bias_to_mean = 0.0
    for vuser in range(height):
        if user_item_matrix[vuser][item_index] > 0:
            sum_bias_to_mean += user_similarity[user_index][vuser] * bias_from_mean(user_item_matrix[vuser], item_index)

    sum_similarity = 0.0
    for vuser in range(height):
        if user_item_matrix[vuser][item_index] > 0:
            sum_similarity += abs(user_similarity[user_index][vuser])

    if sum_similarity == 0.0:
        return 0

    return user_mean + (sum_bias_to_mean / sum_similarity)


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
number_reviewer = 3000

# business_ids, business_index = get_business_ids(number_restaurant)
# user_ids, user_index = get_user_ids(number_restaurant, number_reviewer)
# user_item_matrix = get_matrix(business_index_map, user_ids)
# user_similarity_matrix = get_similarity_matrix(matrix)

import os.path

user_item_training_matrix_fname = 'las_vegas_user_item_training_matrix.txt'
user_item_test_matrix_fname = 'las_vegas_user_item_test_matrix.txt'
if os.path.isfile(user_item_training_matrix_fname) and os.path.isfile(user_item_test_matrix_fname):
    user_item_training_matrix = np.loadtxt(user_item_training_matrix_fname, delimiter=',')
    user_item_test_matrix = np.loadtxt(user_item_test_matrix_fname, delimiter=',')
else:
    user_item_training_matrix, user_item_test_matrix = get_data(number_user=number_reviewer, number_restaurant=number_restaurant)
    np.savetxt(fname=user_item_training_matrix_fname, X=user_item_training_matrix, delimiter=',', header='las_vegas_user_item_training_matrix')
    np.savetxt(fname=user_item_test_matrix_fname, X=user_item_test_matrix, delimiter=',', header='las_vegas_user_item_test_matrix')

user_similarity_fname = 'las_vegas_user_similarity2.txt'
user_item_predict_matrix_fname='las_vegas_user_item_predict_matrix2.txt'
if os.path.isfile(user_similarity_fname):
    print "load existing las_vegas_user_similarity_matrix"
    if not os.path.isfile(user_item_predict_matrix_fname):
        user_similarity = np.loadtxt(user_similarity_fname, delimiter=',')
    else:
        print "prediction is already there, no need to get similarity."
else:
    print "las_vegas_user_similarity_matrix does not exist"
    user_similarity = similarity_matrix(user_item_training_matrix)
    np.savetxt(fname=user_similarity_fname, X=user_similarity, delimiter=',', header='user_similarity')

if os.path.isfile(user_item_predict_matrix_fname):
    print "load existing user_item_predict_matrix_fname"
    user_item_predict_matrix = np.loadtxt(las_vegas_user_item_predict_matrix_fname, delimiter=',')
else:
    print "user_item_predict_matrix_fname does not exist"
    user_item_predict_matrix = np.zeros([number_reviewer, number_restaurant])
    for user in range(number_reviewer):
        for item in range(number_restaurant):
            if user_item_test_matrix[user][item] > 0:
                user_item_predict_matrix[user][item] = predict(las_vegas_user_item_training_matrix, user_similarity, user, item)
                if user_item_predict_matrix[user][item] != 0.0:
                    print "user: {} item: {} prediction: {} actual: {}".format(user, item, user_item_predict_matrix[user][item], user_item_test_matrix[user][item])
    np.savetxt(fname=user_item_predict_matrix_fname, X=user_item_predict_matrix, delimiter=',', header='user_item_predict_matrix')

# # # calculate MSE between user_item_predict_matrix and user_item_test_matrix
m = mse(user_item_predict_matrix, user_item_test_matrix)

print m

# the result is 16.3921997271
