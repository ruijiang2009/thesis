import psycopg2

number_restaurant = 300

def get_data():
    """
    get 
    """
    conn = psycopg2.connect("dbname='yelp' user='ruijiang' host='localhost' password=''")
    cur = conn.cursor()

    cur.close()
    conn.close()