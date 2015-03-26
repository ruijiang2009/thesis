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

def 


def get_data(number_items = 300):
    """
    1. get top 300 restaurant from Las Vegas
    2. for each restaurant get its total reviewers, pick 90% for training, 10% for testing
    3. get 
    """

    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    cur.execute(sql)
    rows = cur.fetchall()
    data_len = len(rows)

    business_ids = []
    f = open('restaurant_id_order_by_number_reviewers_desc.txt', 'r')
    for i in range(number_items):
        
