# user based multiclass SVM method
# based on the following link
# http://scikit-learn.org/stable/modules/svm.html
# will train a model per user basis.
# then given a 
import psycopg2
import numpy as np
import math


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

    sql = 
"SELECT MAX(stars), user_id \
FROM reviewer \
WHERE business_id = '%s'\
GROUP BY user_id" % (business_id)

    cur.execute(sql)
    rows = cur.fetchall()
    data_len = len(rows)
    training_size = int(data_len * 9 / 10)

    training_user_data = []
    for i in range(training_size):
        training_user_data.append({'user_id': row[1], 'stars': row[0]}})
    return user_ids

    test_user_data = []
    for i in range(training_size, data_len):
        test_user_data.append({'user_id': row[1], 'stars': row[0]}})

    cur.close()
    conn.close()

    return training_user_data, test_user_data

# take topic 22 as example
def get_user_feature_data(user_id):
    
