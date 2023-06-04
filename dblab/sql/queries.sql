#3.1.1
SELECT COUNT(l.isbn), s.school_name 
FROM loans l
JOIN client c ON (c.username = l.username)
JOIN school s ON (s.school_name = c.s_name)
GROUP BY s.school_name;

#3.1.2(Μυθιστορημα)
SELECT a.author_name as names, ('author')
FROM author a
JOIN genre on (a.isbn = genre.isbn)
WHERE genre.genre_type = 'Μυθιστόρημα'
UNION
SELECT b.last_name, ('teacher')
FROM client b
JOIN loans on (b.username = loans.username)
JOIN genre on (loans.isbn = genre.isbn)
WHERE genre.genre_type = 'Μυθιστόρημα' and b.occupation = 'teacher';

#3.1.3
SELECT client.first_name,client.last_name,COUNT(loans.isbn) 
FROM client 
JOIN loans ON (loans.username = client.username)
WHERE client.occupation='teacher' AND client.age<40  
GROUP BY client.first_name,client.last_name 
ORDER BY COUNT(loans.isbn) DESC;



#3.1.4
SELECT DISTINCT author.author_name 
FROM author 
WHERE author.isbn NOT in(
    SELECT loans.isbn 
    FROM loans
); 

#3.1.5
SELECT NUM1.manager_id, NUM1.n1
FROM
  (
    SELECT COUNT(l1.isbn) AS n1, s1.manager_id
    FROM loans l1
    JOIN client c1 ON c1.username = l1.username
    JOIN school s1 ON s1.school_name = c1.s_name
    GROUP BY s1.school_name
    HAVING n1 > 10
  ) AS NUM1
JOIN
  (
    SELECT COUNT(l2.isbn) AS n2, s2.manager_id
    FROM loans l2
    JOIN client c2 ON c2.username = l2.username
    JOIN school s2 ON s2.school_name = c2.s_name
    GROUP BY s2.school_name
    HAVING n2 > 10
  ) AS NUM2 ON NUM1.n1 = NUM2.n2
WHERE NUM1.manager_id <> NUM2.manager_id;

#3.1.6
SELECT  LEAST(g1.genre_type, g2.genre_type) AS genre1, GREATEST(g1.genre_type, g2.genre_type) AS genre2, COUNT(b.isbn) div 2 AS loan_count
FROM loans l
JOIN book b ON l.isbn = b.isbn
JOIN genre g1 ON b.isbn = g1.isbn
JOIN genre g2 ON b.isbn = g2.isbn
WHERE   g1.genre_type != g2.genre_type
GROUP BY  genre1, genre2
ORDER BY loan_count DESC
LIMIT 3;

#3.1.7
SELECT author_name,COUNT(isbn), (SELECT COUNT(isbn)  AS book_count 
FROM author
GROUP BY author_name
ORDER  BY book_count desc
LIMIT 1) as auth
FROM author
GROUP BY author_name 
HAVING auth - COUNT(isbn) >= 5 ;

#3.2.1
SELECT book.title, author.author_name,genre.genre_type,provides.copies 
FROM book 
JOIN provides ON (provides.school_name=%s and provides.isbn = book.isbn )  
JOIN author ON(author.isbn = book.isbn) 
JOIN genre ON (genre.isbn = book.isbn);

#3.2.2
SELECT  DISTINCT client.first_name,client.last_name,DATEDIFF(NOW(), loans.due_date),loans.isbn 
FROM client 
JOIN loans  ON(loans.username = client.username) 
JOIN school ON (client.s_name = school.school_name) 
WHERE loans.status = 'not returned' AND school.manager_id = %s;

#3.2.3
SELECT AVG(reviews.likert),client.first_name,client.last_name 
FROM reviews 
JOIN client ON (reviews.username = client.username) 
JOIN school ON(school.school_name=%s and client.s_name = school.school_name) 
GROUP BY client.first_name,client.last_name,client.username;


SELECT AVG(reviews.likert),genre.genre_type 
FROM reviews 
JOIN book ON (book.isbn = reviews.isbn) 
JOIN genre ON(genre.isbn = book.isbn) 
JOIN provides ON(provides.school_name=%s and provides.isbn = book.isbn) 
GROUP BY genre.genre_type;

#3.3.1
SELECT  provides.isbn,book.title,book.publisher,book.page_number,
book.language,book.image,genre.genre_type,author.author_name,book.summary 
FROM provides
JOIN book ON (book.isbn = provides.isbn) 
JOIN client ON(client.username = %s AND client.s_name = provides.school_name)
JOIN genre ON(genre.isbn = book.isbn) 
JOIN author ON(author.isbn = book.isbn);

#3.3.2
SELECT loans.isbn,book.title 
FROM loans 
JOIN book ON (loans.isbn = book.isbn)  
WHERE loans.username = %s;