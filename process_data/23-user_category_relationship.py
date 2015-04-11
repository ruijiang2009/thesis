import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import UserCategory,User
import psycopg2

"""
For user, get the avg(stars) for category of visited restaurant

-- find the avg score for category for paricular user
SELECT AVG(T.stars), bc.category_id
FROM (SELECT r.business_id AS business_id , AVG(r.stars) AS stars
FROM review r
JOIN business b on r.business_id=b.business_id
JOIN business_category bc on b.id=bc.business_id
WHERE r.user_id='WmAyExqSWoiYZ5XEqpk_Uw'
AND bc.category_id=3
GROUP BY r.business_id) T
JOIN business b on T.business_id=b.business_id
JOIN business_category bc on b.id=bc.business_id
WHERE bc.category_id <> 3
GROUP BY bc.category_id
ORDER BY bc.category_id ASC; 
"""


def get_session():
    engine = create_engine('postgresql://ruijiang:@localhost/yelp', echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

session = get_session()

def get_user_ids(number_users=1000):
    user_ids = []
    f = open('user_id_order_by_number_visited_restaurant_desc.txt')
    for i in range(number_users):
        user_ids.append(f.readline()[-23:-1])
    f.close()
    return user_ids

# users = session.query(User).all()
user_ids = get_user_ids(10000)

conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
cur = conn.cursor()

for user_id in user_ids:
    sql = \
"SELECT AVG(T.stars), bc.category_id \
FROM (SELECT r.business_id AS business_id , AVG(r.stars) AS stars \
FROM review r \
JOIN business b on r.business_id=b.business_id \
JOIN business_category bc on b.id=bc.business_id \
WHERE r.user_id='%s' \
AND bc.category_id=3 \
GROUP BY r.business_id) T \
JOIN business b on T.business_id=b.business_id \
JOIN business_category bc on b.id=bc.business_id \
WHERE bc.category_id <> 3 \
GROUP BY bc.category_id \
ORDER BY bc.category_id ASC;  " % (user_id)
    cur.execute(sql)
    rows = cur.fetchall()
    try:
        for row in rows:
            if 0 == session.query(UserCategory).filter(UserCategory.user_id==user_id, UserCategory.category_id==row[1]).count():
                user_category = UserCategory(user_id=user_id, category_id=row[1], stars=row[0])
                session.add(user_category)
        session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print e.message

cur.close()
conn.close()
