# Databases-Semester-Project

This repository contains the completed semester project for the **Databases** course.  
The project required the design and implementation of a database-driven system for managing **School Libraries in public schools**.  

---

## Project Overview

The system was built to handle:

- **Schools:** Registration with details such as name, address, contact info, director, and library operator.  
- **Books:** Storage of book information including title, authors, publisher, ISBN, pages, summary, categories, language, keywords, and available copies.  
- **Users:**  
  - **Administrators:** Managed schools, operators, and database backup/restore.  
  - **Library Operators:** Oversaw book catalogues, loans, reservations, and user accounts.  
  - **Students and Teachers:** Registered, borrowed books within weekly limits, made reservations, and submitted reviews.  
- **Loans & Reservations:** Enforced borrowing limits, handled reservations, and tracked overdue returns.  
- **Reviews:** Allowed ratings and reviews for books (student reviews required operator approval).  
- **Search & CRUD Operations:** All users could search and manage relevant information through a user-friendly interface.  

---

## Team Members (team 139)

- Αριστοτέλης Γρίβας (03119889)  
- Ευάγγελος Μυργιώτης (03119085)  

---

## Requirements

The project asked for:

1. **Database design** (ER diagram, relational schema, DDL/DML scripts, constraints, indexes).  
2. **Implementation** with realistic sample data (schools, books, users, loans, reservations).  
3. **Application development** with a practical and accessible UI to support all user roles.  
4. **Support for SQL queries** tailored to Administrators, Operators, and Users.  
5. **User manual and installation guide.**  

---

## Technologies Used

- **Flask** (Python web framework)  
- **Python**  
- **HTML** (front-end interface)  
- **MySQL** (relational database)  

---


## Install Instructions :

- Clone this repository using the command git clone https://github.com/ArisGr/dblabProject in a local working directory

- Use the command pip install -r requirements.txt in said directory to download the needed libraries

- Create the database using a DBSM that supports MySQL and run the scripts schema.sql and insert.sql 

- Change fields MYSQL_USER, MY_SQLPASSWORD at the lines shown below (lines 14,15 of main.py file) :
  ```python
    app.config["MYSQL_USER"] = 'root'
    app.config["MYSQL_PASSWORD"] = 'team139sql'
  ```
using the user and password you have assigned for your database server (ours were "root" for the server username and "team139sql" for the server password)

- Use the command  python main.py to run the main.py file and visit http://localhost:xxxx/ which will be printed at your output window/terminal



Username / Password for the application testing :


Director : DirectorUsername / abcdef1


client (teacher) : username6 / abcd6


client (student) : username4 / abcd4


manager : username5 / abcd5


All the information above about clients/manager belong to a specific school  (3ο Γυμνασιο Λαρισας) in our database and are provided for the sole purpose of testing the app.

