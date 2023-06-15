# dblabProject

Team Members (team 139) :

Αριστοτέλης Γρίβας (03119889)

Ευάγγελος Μυργιώτης (03119085)



Install Instructions :

-Clone this repository using the command git clone https://github.com/ArisGr/dblabProject in a local working directory

-Use the command pip install -r requirements.txt in said directory to download the needed libraries

-Create the database using a DBSM that supports MySQL and run the scripts schema.sql and insert.sql 

-Change fields MYSQL_USER, MY_SQLPASSWORD at the lines shown below (lines 14,15 of main.py file) :

app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'team139sql'

using the user and password you have assigned for your database server (ours were "root" for the server username and "team139sql" for the server password)

-Use the command  python main.py to run the main.py file and visit http://localhost:xxxx/ which will be printed at your output window/terminal



Username / Password for the application testing :


Director : DirectorUsername / abcdef1


client (teacher) : username6 / abcd6


client (student) : username4 / abcd4


manager : username5 / abcd5


All the information above about clients/manager belong to a specific school  (3ο Γυμνασιο Λαρισας) in our database and are provided for the sole purpose of testing the app.

