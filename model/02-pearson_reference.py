import psycopg2
import numpy as np

from scipy.stats import pearsonr

def get_data(number_user = 3000, number_restaurant = 300):
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
        LIMIT %d); \"" % (number_restaurant, number_user, number_restaurant)

    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    data_len = len(rows)

    training_size = int(data_len * 9 / 10)
    business_index_map = {}
    user_index_map = {}
    user_item_training_matrix = np.empty(number_user, number_restaurant)
    user_item_training_matrix.fill(0)
    user_item_test_matrix = np.empty(number_user, number_restaurant)
    user_item_test_matrix.fill(0)

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



# vi-mean(v)
def bias_from_mean():
    pass

# u and v are two lists
def similarity_measure(u, v):
    corr = pearsonr(u, v)
    rho = 2.5 # based in paper
    r = corr * power(abs(corr), rho)
    return r

def get_similarity_matrix(training_matrix):
    similarity_matrix = []
    number_user = len(user_item_matrix)
    for i in range(number_user):
        user_similarity = [0] * number_user
        for j in range(number_user):
            if j > i:
                user_similarity[j] = similarity_measure(user_item_matrix[i], user_item_matrix[i])
            else:
                user_similarity[j] = similarity_matrix[j][i]
        similarity_matrix.append(user_similarity)
    return similarity_matrix


def prediction(matrix, user_index, item_index, business_index, user_index):
    if matrix[user_index][item_index] == 0:
        return
    number_reviewer = len(matrix)
    number_restaurant = len(matrix[0])
    for 






number_restaurant = 300
number_reviewer = 3000 

business_ids, business_index = get_business_ids(number_restaurant)
user_ids, user_index = get_user_ids(number_restaurant, number_reviewer)
user_item_matrix = get_matrix(business_index_map, user_ids)
user_similarity_matrix = get_similarity_matrix(matrix)






