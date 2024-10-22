﻿-- Get the city with most business 
SELECT COUNT(id) AS c, state, city
FROM business
GROUP BY city, state ORDER BY c DESC;


-- Get the city with most restaurants
SELECT COUNT(id) AS c, state, city
FROM business b
JOIN business_category bc
ON b.id=bc.business_id
WHERE bc.category_id=3 GROUP BY city, state ORDER BY c DESC;

-- SELECT category for restaurants in Las Vegas, NV
SELECT b.id, b.business_id, name, full_address, category
FROM business b
JOIN business_category bc
ON b.id=bc.business_id
WHERE bc.category_id = 3
AND state = 'NV'
AND city = 'Las Vegas'
AND name ilike '%buffet%'
ORDER BY b.id;

-- Find the most popular category
SELECT COUNT(business_id) AS b, c.name
FROM business_category bc
JOIN category c
ON bc.category_id=c.id
GROUP BY c.name
ORDER BY b DESC;

-- Find the restaurant related category and the connected times
SELECT COUNT(business_id) AS b, c.name
FROM business_category bc
JOIN category c
ON bc.category_id=c.id
WHERE bc.business_id IN (
    SELECT id
    FROM business b
    JOIN business_category bbc
    ON bbc.business_id=b.id
    WHERE bbc.category_id=3)
GROUP BY c.name
ORDER BY b DESC;

-- Find the restaurant related category and the connected times in Las Vegas, NV
SELECT COUNT(business_id) AS b, c.name
FROM business_category bc
JOIN category c
ON bc.category_id=c.id
WHERE bc.business_id IN(
    SELECT id
    FROM business b
    JOIN business_category bbc
    ON bbc.business_id=b.id
    WHERE bbc.category_id=3
    AND state='NV'
    AND city = 'Las Vegas')
GROUP BY c.name
ORDER BY b DESC;

-- Las Vegas, NV: Find the restaurant related category showed more than 30 times
SELECT COUNT(business_id) AS b, c.name
FROM business_category bc
JOIN category c
ON bc.category_id=c.id
WHERE bc.business_id IN (
    SELECT id
    FROM business b
    JOIN business_category bbc
    ON bbc.business_id=b.id
    WHERE bbc.category_id=3
    AND state='NV'
    AND city = 'Las Vegas')
    AND c.id <> 3
GROUP BY c.name
HAVING COUNT(business_id) >= 30
ORDER BY b DESC;

-- how many reviews are on restaurant
SELECT COUNT(review_id) AS rc
FROM review r
JOIN business b ON r.business_id=b.business_id
JOIN business_category bc ON bc.business_id=b.id
WHERE bc.category_id=3
ORDER BY rc DESC;

-- Las Vegas, NV: Find how many reviewers one restaurant can have
SELECT COUNT(review_id) AS rc, b.business_id, b.name, b.category
FROM review r
JOIN business b ON r.business_id=b.business_id
JOIN business_category bc ON bc.business_id=b.id
WHERE b.state = 'NV'
AND b.city = 'Las Vegas'
AND bc.category_id=3
GROUP BY b.business_id, b.name, b.category
ORDER BY rc DESC;


SELECT name, full_address, category FROM business WHERE business_id = '4bEjOyTaDG24SY5TxsaUNQ';

SELECT review_id, user_id, business_id, text FROM review WHERE business_id = '4bEjOyTaDG24SY5TxsaUNQ';


SELECT review_id, user_id, business_id, text FROM review WHERE review_id = 'xTGollxKKRh7ANzKs1OfEg';

SELECT * FROM review WHERE review_id = '15SdjuK7DmYqUAj6rjGowg';

SELECT AVG(t.stars) FROM
(SELECT r.review_id, r.stars AS stars FROM review_topic22 rt
JOIN review r ON rt.review_id=r.review_id
WHERE business_id = 'q2SZa5g85758iW1L9sSL1g'
AND rt.topic_id = 2) t;

SELECT COUNT(DISTINCT user_id) FROM review r
JOIN business b ON r.business_id = b.business_id
JOIN business_category bc ON b.id = bc.business_id
WHERE bc.category_id=3;

SELECT r.review_id FROM review r
JOIN business b ON r.business_id = b.business_id
JOIN business_category bc ON b.id = bc.business_id
WHERE bc.category_id=3 AND r.user_id = 'fEXxa3d0cjqysrQk4hmudA';

-- see the business_id with how many distinct reviewer
SELECT COUNT(r.review_id) c, r.business_id
FROM review r
JOIN business b ON r.business_id=b.business_id
JOIN business_category bc ON bc.business_id=b.id
WHERE bc.category_id=3
GROUP BY r.business_id
ORDER BY c DESC;

-- select user who has been in top # business
SELECT COUNT(review_id) as review_count, user_id 
FROM review r WHERE business_id IN
(SELECT business_id
FROM
(SELECT COUNT(r.review_id) c, r.business_id
FROM review r
JOIN business b ON r.business_id=b.business_id
JOIN business_category bc ON bc.business_id=b.id
WHERE bc.category_id=3
GROUP BY r.business_id
ORDER BY c DESC) t
LIMIT 300)
GROUP BY r.user_id
ORDER BY review_count DESC
LIMIT 3000;

SELECT stars, user_id, business_id
FROM review r
WHERE user_id IN (
    SELECT user_id
    FROM (
        SELECT COUNT(review_id) AS review_count, user_id
        FROM review r WHERE business_id IN
        (SELECT business_id
        FROM
        (SELECT COUNT(r.review_id) c, r.business_id
        FROM review r
        JOIN business b ON r.business_id=b.business_id
        JOIN business_category bc ON bc.business_id=b.id
        WHERE bc.category_id=3
        GROUP BY r.business_id
        ORDER BY c DESC) t
        LIMIT 300)
    GROUP BY r.user_id
    ORDER BY review_count DESC
    LIMIT 3000) s)
AND business_id IN
    (SELECT business_id
    FROM
    (SELECT COUNT(r.review_id) c, r.business_id
    FROM review r
    JOIN business b ON r.business_id=b.business_id
    JOIN business_category bc ON bc.business_id=b.id
    WHERE bc.category_id=3
    GROUP BY r.business_id
    ORDER BY c DESC) s
    LIMIT 300);


SELECT bt.stars, t.name
FROM business_topic50 bt 
JOIN topic50 t on bt.topic_id = t.id
WHERE business_id = '4bEjOyTaDG24SY5TxsaUNQ';

SELECT bt.stars, bt.relationship, b.name, b.stars
FROM business_topic50 bt 
JOIN business b on bt.business_id=b.business_id
WHERE bt.topic_id = 19 AND bt.stars is not NULL
ORDER BY bt.stars DESC
LIMIT 50;

-- how many people has visited restaurant in Las Vegas
SELECT COUNT(DISTINCT user_id)
FROM review r
JOIN business b ON r.business_id = b.business_id
WHERE b.city = 'Las Vegas';


-- get topic 22 from top 

SELECT business_id \
        FROM \
        (SELECT COUNT(r.review_id) c, r.business_id \
        FROM review r \
        JOIN business b ON r.business_id=b.business_id \
        JOIN business_category bc ON bc.business_id=b.id \
        WHERE bc.category_id=3 \
        GROUP BY r.business_id \
        ORDER BY c DESC) s \
        LIMIT %d
