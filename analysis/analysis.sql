-- Get the city with most business 
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

SELECT review_id, user_id, business_id, text FROM review WHERE business_id = '4bEjOyTaDG24SY5TxsaUNQ'