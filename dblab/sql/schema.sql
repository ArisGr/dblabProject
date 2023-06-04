CREATE TABLE book (
    isbn DECIMAL(13,0) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    publisher VARCHAR(30) NOT NULL,
    page_number INT NOT NULL,
    language VARCHAR(15) NOT NULL,
    image VARCHAR(150) NOT NULL,
    summary VARCHAR(3000) DEFAULT ' '
);


CREATE TABLE client (
    username  VARCHAR(30) PRIMARY KEY,
    first_name  VARCHAR(30) NOT NULL,
    last_name  VARCHAR(30) NOT NULL,
    passw VARCHAR(30) UNIQUE NOT NULL,
    occupation VARCHAR(30) NOT NULL check(occupation = 'teacher' or occupation='manager' or occupation='director' or occupation ='student'),
    verified VARCHAR(10) NOT NULL check (verified = 'yes' or verified = 'no'),
    director_username VARCHAR(30) NOT NULL,
    age INT NOT NULL
);


CREATE TABLE school (
    school_name  VARCHAR(40) PRIMARY KEY,
    street_name VARCHAR(30) NOT NULL,
    street_number INT NOT NULL,
    postal_code INT NOT NULL,
    city VARCHAR(30) NOT NULL,
    email_address VARCHAR(30) UNIQUE,
    phone_number VARCHAR(10) UNIQUE,
    principal_name VARCHAR(40) NOT NULL,
    manager_id VARCHAR(30) DEFAULT NULL,
    FOREIGN KEY(manager_id) REFERENCES client(username) ON DELETE  CASCADE ON UPDATE CASCADE

);

CREATE TABLE reserves (
    isbn  DECIMAL(13,0) ,
    username VARCHAR(30),
    start_date DATE NOT NULL,
    due_date DATE  NOT NULL,
    PRIMARY KEY(isbn,username),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE  CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(username) REFERENCES client(username) ON DELETE  CASCADE ON UPDATE CASCADE,  
    constraint valid_dates check(start_date<due_date),
    constraint duration check(timestampdiff(day, start_date, due_date) = 7)
);


CREATE TABLE loans (
    isbn  DECIMAL(13,0) ,
    username VARCHAR(30),
    start_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL check(status = 'returned' or status = 'not returned'),
    PRIMARY KEY(isbn,username),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE  CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(username) REFERENCES client(username) ON DELETE  CASCADE ON UPDATE CASCADE,
    constraint loan_date check(start_date<due_date),
    constraint loan_duration check(timestampdiff(day, start_date, due_date) = 7)
);

CREATE TABLE reviews (
    isbn  DECIMAL(13,0) ,
    username VARCHAR(30),
    comment VARCHAR(1000),
    likert INT NOT NULL check(likert >= 0 and likert <= 5),
    PRIMARY KEY(isbn,username),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE  CASCADE,
    FOREIGN KEY(username) REFERENCES client(username) ON DELETE  CASCADE ON UPDATE CASCADE
);

CREATE TABLE provides (
    isbn  DECIMAL(13,0) ,
    school_name VARCHAR(40),
    copies INT NOT NULL,
    PRIMARY KEY(isbn,school_name),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE  CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(school_name) REFERENCES school(school_name) ON DELETE  CASCADE ON UPDATE CASCADE
);


ALTER TABLE client
ADD FOREIGN KEY(director_username)
REFERENCES client(username) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE client
ADD s_name VARCHAR(40) DEFAULT NULL;


ALTER TABLE client
ADD FOREIGN KEY(s_name)
REFERENCES school(school_name) ON DELETE CASCADE ON UPDATE CASCADE;



CREATE TABLE author (
    isbn DECIMAL(13,0),
    author_name VARCHAR(50),
    PRIMARY KEY(author_name,isbn),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE genre (
    isbn DECIMAL(13,0),
    genre_type VARCHAR(50),
    PRIMARY KEY(genre_type,isbn),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE keyword (
    isbn DECIMAL(13,0) ,
    kword VARCHAR(50),
    PRIMARY KEY(kword,isbn),
    FOREIGN KEY(isbn) REFERENCES book(isbn) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE INDEX likert_idx ON reviews(likert);
CREATE INDEX copies_idx ON provides(copies);
CREATE INDEX title_idx ON book(title);
CREATE INDEX occupation_idx ON client(occupation);
CREATE INDEX loans_date_idx ON loans(start_date,due_date);
CREATE INDEX loans_status_idx ON loans(status);
CREATE INDEX reserves_date_idx ON reserves(start_date,due_date);