from flask import Flask, redirect, url_for, render_template , request , flash , session
from flask_mysqldb import MySQL
from forms import LoginForm,ClientForm,LoansForm, BookForm, SchoolForm, ReviewForm, GenreForm

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange


app = Flask(__name__)


app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'team139sql'
app.config["MYSQL_DB"] = 'dblab'
app.config["SECRET_KEY"] = 'dbdbdbdb' ## secret key for sessions (signed cookies). Flask uses it to protect the contents of the user session against tampering.




db = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def home():  
    form = LoginForm()
    if request.method == 'POST':
        usr = request.form['username']
        passw = request.form['password']

        try:
            cur = db.connection.cursor()
            cur.execute("SELECT client.occupation,client.s_name,client.passw,client.verified FROM client WHERE client.username=%s and client.passw=%s;", [usr,passw])
            x =   cur.fetchone() 
            occupation = x[0]
            school = x[1]
            verification = x[3]
            print(verification)
            cur.close()
            if occupation == 'director' and verification != 'no':
              return redirect(url_for("director", name = usr))
        
            elif occupation == 'manager' and verification != 'no':
             return redirect(url_for("manager", name = usr, school = school))
        
            elif (occupation == 'student' or occupation == 'teacher') and verification != 'no':
                return redirect(url_for("client", name = usr, occ = occupation, school = school))
            else:
                flash("Something went Wrong! Try typing your information again.")
                return render_template("base.html", form=form)
            
        except Exception as e:
             flash("Wrong Credentials! Try again.")
             return render_template("base.html", form=form)
    else:    
        return render_template("base.html", form=form)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register",methods=['GET', 'POST'])
def register():
    form = ClientForm()
    cur = db.connection.cursor()
    cur.execute("SELECT school.school_name FROM school;")
    schools = cur.fetchall()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['passw']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        occupation = request.form['select']
        age = request.form['age']
        school_name = request.form['s_name']
        cur = db.connection.cursor()

        try:                      
           
            cur.execute("SELECT * FROM school WHERE school_name=%s;", [school_name])
            x = cur.fetchall()
            if x != None:
                print('before')
                cur.execute("INSERT INTO client VALUES(%s,%s,%s,%s,%s,'no','DirectorUsername',%s,%s);", [username,first_name,last_name,password,occupation,age,school_name])
                print('after')
                db.connection.commit()
                cur.close()
                flash("You have applied for a registration.You will be verified shortly.")
                return redirect(url_for("home"))
          


            else:
                 flash("There is no Such school")   
                 cur.close()
                 return redirect(url_for("home"))
                 
            

        except Exception as e:
             flash("Invalid Inputs!")
             return redirect(url_for("home"))
    
    
    return  render_template("register.html" , table = schools, form = form)

    


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("occupation", None)
    session.pop("school", None)
    return render_template("logout.html")



@app.route("/<name>")
def user(name):
        return f"hello {name}!"

@app.route("/director/<name>",  methods=['GET', 'POST'])
def director(name):
            session["user"] = name
            form = GenreForm()

            cur = db.connection.cursor()
 
            cur.execute("SELECT COUNT(l.isbn), s.school_name FROM loans l JOIN client c ON (c.username = l.username) JOIN school s ON (s.school_name = c.s_name) GROUP BY s.school_name;")
            q31 =   cur.fetchall() 

            q32 = '-'

            cur.execute("SELECT client.first_name,client.last_name,COUNT(loans.isbn) FROM client   JOIN loans ON (loans.username = client.username)  WHERE client.occupation='teacher' AND client.age<40  GROUP BY client.first_name,client.last_name ORDER BY COUNT(loans.isbn) DESC;")
            q33 =   cur.fetchall() 

            cur.execute("SELECT DISTINCT author.author_name FROM author JOIN book ON(author.isbn = book.isbn) WHERE book.isbn NOT  IN ( SELECT isbn FROM loans);")
            q34 =   cur.fetchall() 

            cur.execute("SELECT NUM1.manager_id, NUM1.n1 FROM (SELECT COUNT(l1.isbn) AS n1, s1.manager_id  FROM loans l1    JOIN client c1 ON c1.username = l1.username   JOIN school s1 ON s1.school_name = c1.s_name     GROUP BY s1.school_name     HAVING n1 > 10   ) AS NUM1 JOIN (     SELECT COUNT(l2.isbn) AS n2, s2.manager_id     FROM loans l2     JOIN client c2 ON c2.username = l2.username     JOIN school s2 ON s2.school_name = c2.s_name     GROUP BY s2.school_name     HAVING n2 > 10  ) AS NUM2 ON NUM1.n1 = NUM2.n2 WHERE NUM1.manager_id <> NUM2.manager_id;")
            q35 =   cur.fetchall() 

            cur.execute("SELECT  LEAST(g1.genre_type, g2.genre_type) AS genre1, GREATEST(g1.genre_type, g2.genre_type) AS genre2, COUNT(b.isbn) div 2 AS loan_count FROM loans l JOIN book b ON l.isbn = b.isbn JOIN genre g1 ON b.isbn = g1.isbn JOIN genre g2 ON b.isbn = g2.isbn WHERE   g1.genre_type != g2.genre_type GROUP BY  genre1, genre2 ORDER BY loan_count DESC LIMIT 3;")
            q36 =   cur.fetchall() 

            cur.execute("SELECT author_name,COUNT(isbn), (SELECT COUNT(isbn)  AS book_count  FROM author GROUP BY author_name ORDER  BY book_count desc LIMIT 1) as auth FROM author GROUP BY author_name  HAVING auth - COUNT(isbn) >= 5 ;")
            q37 =   cur.fetchall() 

            cur.execute("SELECT * from client WHERE client.username=%s;", [name])
            director_info = cur.fetchall()

            if request.method == 'POST':
                genre = request.form['genre_type']
                cur.execute("SELECT a.author_name as names, ('author') FROM author a JOIN genre on (a.isbn = genre.isbn) WHERE genre.genre_type = %s UNION SELECT b.last_name, ('teacher') FROM client b JOIN loans on (b.username = loans.username) JOIN genre on (loans.isbn = genre.isbn) WHERE genre.genre_type = %s and b.occupation = 'teacher';", [genre,genre])
                q32 =   cur.fetchall() 


            cur.close()
            return render_template("director.html" , table1=q31 ,table2 = q32, table3=q33 ,table4 = q34,table5=q35 ,table6 = q36, table7=q37, info = director_info, form = form)


@app.route("/manager/<name>/<school>")
def manager(name,school):
        session["user"] = name
        session["school"] = school
        cur = db.connection.cursor()
 
        cur.execute("SELECT book.title, author.author_name,genre.genre_type,provides.copies from book JOIN provides ON (provides.school_name=%s and provides.isbn = book.isbn )  JOIN author ON(author.isbn = book.isbn) JOIN genre ON (genre.isbn = book.isbn);", [school])
        qm1 =   cur.fetchall() 

        cur.execute("SELECT  DISTINCT client.first_name,client.last_name,DATEDIFF(NOW(), loans.due_date),loans.isbn FROM client JOIN loans  ON(loans.username = client.username) JOIN school ON (client.s_name = school.school_name) WHERE loans.status = 'not returned' AND school.manager_id = %s;", [name])
        qm2 =   cur.fetchall() 


        cur.execute("SELECT AVG(reviews.likert),client.first_name,client.last_name FROM reviews JOIN client ON (reviews.username = client.username) JOIN school ON(school.school_name=%s and client.s_name = school.school_name) GROUP BY client.first_name,client.last_name,client.username;", [school])
        qm3 =   cur.fetchall() 

        cur.execute("SELECT * from client WHERE client.username=%s;", [name])
        manager_info = cur.fetchall()

        cur.execute("SELECT AVG(reviews.likert),genre.genre_type FROM reviews JOIN book ON (book.isbn = reviews.isbn) JOIN genre ON(genre.isbn = book.isbn) JOIN provides ON(provides.school_name=%s and provides.isbn = book.isbn) GROUP BY genre.genre_type;", [school])
        qm4 = cur.fetchall()

        cur.close()
        return render_template("manager.html" , table1 =qm1, table2 = qm2, table3 = qm3, table4 = qm4,info = manager_info )


@app.route("/client/<name>/<occ>/<school>", methods=['GET', 'POST'])
def client(name,occ,school):
    session["user"] = name
    session["occupation"] = occ
    session["school"] = school
    form = BookForm()

    
  
    cur = db.connection.cursor()

    cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn);", [name])    
    qc1 =   cur.fetchall() 


    cur.execute("SELECT loans.isbn,book.title FROM loans JOIN book ON (loans.isbn = book.isbn)  WHERE loans.username = %s;", [name])
    qc2 =   cur.fetchall() 

    cur.execute("SELECT * from client WHERE client.username=%s;", [name])
    client_info = cur.fetchall()


    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        author = request.form['author']    

        if title == '' and genre == '' and author=='': 
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn);", [name])
            qc1 =   cur.fetchall()  

        elif title == '' and genre == '' and author!='': 
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE author.author_name=%s;", [name,author])
            qc1 =   cur.fetchall() 
        elif title == '' and genre != '' and author=='':
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE genre.genre_type=%s;", [name,genre])
            qc1 =   cur.fetchall() 
        elif title == '' and genre != '' and author!='':
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE genre.genre_type=%s and author.author_name=%s;", [name,genre,author])
            qc1 =   cur.fetchall() 
        elif title != '' and genre == '' and author=='':
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE book.title =%s;", [name,title])
            qc1 =   cur.fetchall() 
        elif title != '' and genre == '' and author!='':
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE book.title =%s and author.author_name=%s;", [name,title,author])
            qc1 =   cur.fetchall() 
        elif title != '' and genre != '' and author=='':
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE book.title =%s and genre.genre_type=%s;", [name,title,genre])
            qc1 =   cur.fetchall() 
        elif title != '' and genre != '' and author!='':
            cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn) WHERE book.title =%s and genre.genre_type=%s and author.author_name=%s;", [name,title,genre,author])
            qc1 =   cur.fetchall() 
        
        return render_template("client.html" , table1 =qc1, table2 = qc2, info = client_info, form = form)  
        
    
    return render_template("client.html" , table1 =qc1, table2 = qc2, info = client_info, form = form)







@app.route("/changeinfo", methods=['GET', 'POST'])
def changeinfo():
    user = session["user"]
    school = session["school"]
    occupation = session["occupation"]
    form = ClientForm()

    if request.method == 'POST':
        if occupation == 'teacher':
            username = request.form['username']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = request.form['passw']

        else:
             flash("You are a student,thus cannot change your info", "info")
             return redirect(url_for("client", name = user, occ = occupation, school = school))
        
        try:    
            cur = db.connection.cursor()
            cur.execute("UPDATE client SET client.username =%s,client.passw =%s, client.first_name = %s,client.last_name = %s where client.username = %s;", [username,password,first_name,last_name,user])
            db.connection.commit()
            cur.close()

            return redirect(url_for("client", name = username, occ = occupation, school = school))
        
        except Exception as e:
            flash("Action not allowed.Try different values.")
            return redirect(url_for("client", name = username, occ = occupation, school = school))
                            
    
    return  render_template("change_client_info.html" , form = form)


@app.route("/applyloan", methods=['GET', 'POST'])
def applyloan():
    user = session["user"]
    school = session["school"]
    occupation = session["occupation"]
    form = LoansForm()
    cur = db.connection.cursor()
    
    cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn);", [user])    
    books =   cur.fetchall() 

    cur.execute("SELECT  reviews.isbn,AVG(reviews.likert) from reviews JOIN provides ON(provides.school_name =%s and provides.isbn = reviews.isbn) GROUP BY reviews.isbn;", [school])    
    reviews =   cur.fetchall()

    if request.method == 'POST':
        isbn = request.form['isbn']
        s_date = request.form['start_date']
        d_date = request.form['due_date']
        
        cur.execute("SELECT * FROM provides where (provides.isbn =%s and provides.school_name=%s);", [isbn,school])
        x = cur.fetchone()
        if x == None:
            flash("No such book in this school!")
            cur.close()
            return redirect(url_for("client", name = user, occ = occupation, school = school))
        
        else: 
            try:
                cur.execute("INSERT INTO loans VALUES(%s,%s,%s,%s,'not returned');", [isbn,user,s_date,d_date])
                db.connection.commit()
                flash("Loan Complete.")
                cur.close()
            except Exception as e:
                flash("Action not allowed.Try different values.")
                return redirect(url_for("client", name = user, occ = occupation, school = school))

        return redirect(url_for("client", name = user, occ = occupation, school = school))
    
    
    return  render_template("applyloan.html" , form = form , table = books,table1 = reviews)


@app.route("/reserve", methods=['GET', 'POST'])
def reserve():
    user = session["user"]
    school = session["school"]
    occupation = session["occupation"]
    form = LoansForm()
    cur = db.connection.cursor()
    
    cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn);", [user])    
    books =   cur.fetchall() 

    cur.execute("SELECT  reviews.isbn,AVG(reviews.likert) from reviews JOIN provides ON(provides.school_name =%s and provides.isbn = reviews.isbn) GROUP BY reviews.isbn;", [school])    
    reviews =   cur.fetchall()

    if request.method == 'POST':
        isbn = request.form['isbn']
        s_date = request.form['start_date']
        d_date = request.form['due_date']
        
        cur.execute("SELECT * FROM provides where (provides.isbn =%s and provides.school_name=%s);", [isbn,school])
        x = cur.fetchone()
        if x == None:
            flash("No such book in this school!")
            cur.close()
            return redirect(url_for("client", name = user, occ = occupation, school = school))
        
        else: 
            try:
                cur.execute("INSERT INTO reserves VALUES(%s,%s,%s,%s);", [isbn,user,s_date,d_date])
                db.connection.commit()
                flash("Reservation Complete.")
                cur.close()
            except Exception as e:
                flash("Action not allowed.Try different values.")
                cur.close()
                return redirect(url_for("client", name = user, occ = occupation, school = school))

        return redirect(url_for("client", name = user, occ = occupation, school = school))
    
    
    return  render_template("reserve.html" , form = form , table = books, table1 = reviews)



@app.route("/review", methods=['GET', 'POST'])
def review():
    user = session["user"]
    school = session["school"]
    occupation = session["occupation"]
    form = ReviewForm()
    cur = db.connection.cursor()
    cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn);", [user])    
    books =   cur.fetchall() 

    if request.method == 'POST':
        isbn = request.form['isbn']
        comment = request.form['comment']
        likert = request.form['likert']
        
 
        try:
            cur.execute("SELECT * FROM provides where(provides.school_name =%s and provides.isbn=%s);",[school,isbn] )
            y =   cur.fetchone() 
            if  y == None:
                  flash("There is no such school to delete!")
                  cur.close()
                  return redirect(url_for("director", name = user, school = school))
            else:
                cur.execute("INSERT INTO reviews VALUES(%s,%s,%s,%s);", [isbn,user,comment,likert])
                db.connection.commit()
                flash("You have rated a book")
                cur.close()
                return redirect(url_for("client", name = user, occ = occupation, school = school))
                  
        except Exception as e:
             flash("Something Went Wrong. Have you perhaps rated the book previously? If so ,you cant rate it again.")
             return redirect(url_for("client", name = user, occ = occupation, school = school))
            
    return  render_template("review.html" , form = form, table = books)


@app.route("/addbook", methods=['GET', 'POST'])
def addbook():
    user = session["user"]
    school = session["school"]
    form = BookForm()

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publisher = request.form['publisher']
        page_number = request.form['page_number']
        language = request.form['language']
        image = request.form['image']
        summary = request.form['summary']
        
        cur = db.connection.cursor()


        cur.execute("SELECT provides.copies from provides WHERE  provides.isbn=%s and provides.school_name=%s;", [isbn,school])
        x =   cur.fetchone() 
        if x != None:
             copies = x[0]
             copies = copies + 1
             cur.execute("UPDATE provides SET provides.copies =%s where provides.isbn=%s and provides.school_name=%s;", [copies,isbn,school])
             db.connection.commit()
             cur.close()
             flash("Added one more book copy!", "info")
             return redirect(url_for("manager", name = user, school = school))


        else:
            cur.execute("SELECT provides.copies from provides WHERE  provides.isbn=%s ;", [isbn])
            y =   cur.fetchone() 
            if y != None:
                 cur.execute("INSERT INTO provides VALUES(%s,%s,%s);", [isbn,school,1])
                 db.connection.commit()
                 cur.close()
                 flash("Book added!", "info")
                 return redirect(url_for("manager", name = user, school = school))

            else:
                cur.execute("INSERT INTO book VALUES(%s,%s,%s,%s,%s,%s,%s);", [isbn,title,publisher,page_number,language,image,summary])
                db.connection.commit()
                cur.execute("INSERT INTO author VALUES(%s,'NULL')", [isbn])
                db.connection.commit()
                cur.execute("INSERT INTO genre VALUES(%s,'NULL')", [isbn])
                db.connection.commit()
                cur.execute("INSERT INTO keyword VALUES(%s,'NULL')", [isbn])
                db.connection.commit()
                cur.execute("INSERT INTO provides VALUES(%s,%s,%s);", [isbn,school,1])
                db.connection.commit()
                cur.close()
                flash("Book added in the Library System!", "info")
                return redirect(url_for("manager", name = user, school = school))
    
    
    return  render_template("addbook.html" , form = form)



@app.route("/addauthor", methods=['GET', 'POST'])
def addauthor():
    user = session["user"]
    school = session["school"]
    form = BookForm()

    if request.method == 'POST':
        isbn = request.form['isbn']
        text = request.form['title']
        
        cur = db.connection.cursor()

        cur.execute("SELECT * from provides WHERE  provides.isbn=%s and provides.school_name=%s;", [isbn,school])
        x =   cur.fetchone() 
        if x != None:
             try:
                
                cur.execute("INSERT INTO author VALUES(%s,%s);", [isbn,text])
                db.connection.commit()
                cur.execute("DELETE FROM author WHERE author.author_name = 'NULL';")
                db.connection.commit()
                cur.close()
                flash("Added one author to this book!", "info")
                return redirect(url_for("manager", name = user, school = school))
             
             except Exception as e:
                flash("Something Went Wrong.")
                return redirect(url_for("manager", name = user, school = school))


        else: 
                flash("No such book in the this Library.")
                return redirect(url_for("manager", name = user, school = school))
  
    
    return  render_template("addauthor.html" , form = form)


@app.route("/addgenre", methods=['GET', 'POST'])
def addgenre():
    user = session["user"]
    school = session["school"]
    form = BookForm()

    if request.method == 'POST':
        isbn = request.form['isbn']
        text = request.form['title']
        
        cur = db.connection.cursor()

        cur.execute("SELECT * from provides WHERE  provides.isbn=%s and provides.school_name=%s;", [isbn,school])
        x =   cur.fetchall() 
        if x != None:
             try:
                cur.execute("INSERT INTO genre VALUES(%s,%s);", [isbn,text])
                db.connection.commit()
                cur.execute("DELETE FROM genre WHERE genre.genre_type = 'NULL';")
                db.connection.commit()
                cur.close()
                flash("Added a genre type to this book!", "info")
                return redirect(url_for("manager", name = user, school = school))
             
             except Exception as e:
                flash("Something Went Wrong.")
                return redirect(url_for("manager", name = user, school = school))


        else: 
                flash("No such book in the this Library.")
                return redirect(url_for("manager", name = user, school = school))
  
    
    return  render_template("addgenre.html" , form = form)


@app.route("/addkeyword", methods=['GET', 'POST'])
def addkeyword():
    user = session["user"]
    school = session["school"]
    form = BookForm()

    if request.method == 'POST':
        isbn = request.form['isbn']
        text = request.form['title']
        
        cur = db.connection.cursor()

        cur.execute("SELECT * from provides WHERE  provides.isbn=%s and provides.school_name=%s;", [isbn,school])
        x =   cur.fetchone() 
        if x != None:
             try:
                cur.execute("INSERT INTO keyword VALUES(%s,%s);", [isbn,text])
                db.connection.commit()
                cur.execute("DELETE FROM keyword WHERE keyword.kword = 'NULL';")
                db.connection.commit()
                cur.close()
                flash("Added one keyword to this book!", "info")
                return redirect(url_for("manager", name = user, school = school))
             
             except Exception as e:
                flash("Something Went Wrong.")
                return redirect(url_for("manager", name = user, school = school))


        else: 
                flash("No such book in the this Library.")
                return redirect(url_for("manager", name = user, school = school))
  
    
    return  render_template("addkeyword.html" , form = form)


@app.route("/deletebook", methods=['GET', 'POST'])
def deletebook():
    user = session["user"]
    school = session["school"]
    form = BookForm()
    cur = db.connection.cursor()
    cur.execute("SELECT  provides.isbn,book.title,book.publisher,book.page_number,book.language,book.image,genre.genre_type,author.author_name,book.summary FROM provides JOIN book ON (book.isbn = provides.isbn) JOIN client ON(client.username = %s AND client.s_name = provides.school_name) JOIN genre ON(genre.isbn = book.isbn) JOIN author ON(author.isbn = book.isbn);", [user])    
    books = cur.fetchall()

    if request.method == 'POST':
        isbn = request.form['isbn']
        
 
        try:

            cur.execute("DELETE  FROM  provides WHERE provides.isbn=%s and provides.school_name=%s;", [isbn,school])
            db.connection.commit()
            flash("Book no longer exists in this schools Library!", "info")
            cur.execute("SELECT provides.school_name FROM  provides WHERE provides.isbn=%s;", [isbn])
            y =   cur.fetchone() 
            if y == None:
                  cur.execute("DELETE FROM  book WHERE book.isbn=%s;", [isbn])
                  db.connection.commit()
                        
            cur.close()
            
        
        except Exception as e:
             flash(str(e),"danger")
        return redirect(url_for("manager", name = user, school = school))

    
    
    return  render_template("deletebook.html" , table = books, form = form)


@app.route("/verifyclient", methods=['GET', 'POST'])
def verifyclient():
    user = session["user"]
    school = session["school"]
    form = ClientForm()
    cur = db.connection.cursor()
    cur.execute("SELECT *  FROM client where (client.s_name=%s and client.verified = 'no');", [school])
    clients  = cur.fetchall()

    if request.method == 'POST':
        username = request.form['username']

        try:
 
            cur.execute("SELECT *  FROM client where client.s_name=%s and client.username=%s;", [school,username])
            x  = cur.fetchone()
            if x  != None:
                cur.execute("UPDATE client SET client.verified = 'yes' WHERE client.username=%s;", [username])
                db.connection.commit()
                flash("You verified a user")
                cur.close()
                return redirect(url_for("manager", name = user, school = school))

            else:
                flash("That user does not belong to the school you manage!")
                cur.close()
                return redirect(url_for("manager", name = user, school = school))
      
        except Exception as e:
             flash(str(e),"danger")
             return redirect(url_for("manager", name = user, school = school))

    
    return  render_template("verifyclient.html" , form = form, table = clients)



@app.route("/returned", methods=['GET', 'POST'])
def returned():
    user = session["user"]
    school = session["school"]
    form = LoansForm()
    cur = db.connection.cursor()
    cur.execute("SELECT  DISTINCT client.username,client.first_name,client.last_name,DATEDIFF(NOW(), loans.due_date),loans.isbn FROM client JOIN loans  ON(loans.username = client.username) JOIN school ON (client.s_name = school.school_name) WHERE loans.status = 'not returned' AND school.manager_id = %s;", [user])
    loans = cur.fetchall()

    if request.method == 'POST':
        username = request.form['username']
        isbn = request.form['isbn']

        try:
 
            cur.execute("SELECT *  FROM loans where loans.username=%s and loans.isbn=%s and loans.status='not returned';", [username,isbn])
            x  = cur.fetchone()
            print(x)
            if x  != None:
                cur.execute("UPDATE loans SET loans.status ='returned' WHERE loans.username=%s and loans.isbn=%s;", [username,isbn])
                db.connection.commit()
                flash("Book returned")
                cur.close()
                return redirect(url_for("manager", name = user, school = school))

            else:
                flash("That user does not have this book loaned and not returned!")
                cur.close()
                return redirect(url_for("manager", name = user, school = school))
      
        except Exception as e:
             flash(str(e),"danger")
             return redirect(url_for("manager", name = user, school = school))

    
    return  render_template("returned.html" , form = form, table = loans)



@app.route("/verifymanager", methods=['GET', 'POST'])
def verifymanager():
    user = session["user"]
    form = ClientForm()
    cur = db.connection.cursor()
    cur.execute("SELECT *  FROM client where client.occupation='manager' and client.verified = 'no';")
    managers  = cur.fetchall()

    if request.method == 'POST':
        username = request.form['username']
        print(username)

        try:
 
            cur.execute("SELECT *  FROM client where client.occupation='manager' and client.username=%s;", [username])
            x  = cur.fetchone()
            if x  != None:
                cur.execute("UPDATE client SET client.verified = 'yes' WHERE client.username=%s;", [username])
                db.connection.commit()
                cur.execute("UPDATE school s JOIN client c ON s.school_name = c.s_name SET s.manager_id = c.username WHERE c.username = %s;", [username])
                db.connection.commit()
                flash("You verified a manager")
                cur.close()
                return redirect(url_for("director", name = user))

            else:
                flash("That user does not belong to the school you manage!")
                cur.close()
                return redirect(url_for("director", name = user))
      
        except Exception as e:
             flash(str(e),"danger")
             return redirect(url_for("director", name = user))

    
    return  render_template("verifymanager.html" , form = form, table = managers)



@app.route("/deleteclient", methods=['GET', 'POST'])
def deleteclient():
    user = session["user"]
    school = session["school"]
    form = ClientForm()
    cur = db.connection.cursor()
    cur.execute("SELECT *  FROM client where (client.s_name=%s and client.verified = 'yes');", [school])
    clients  = cur.fetchall()

    if request.method == 'POST':
        username = request.form['username']
        print(username)

        try:
 
            cur.execute("SELECT *  FROM client where client.s_name=%s and client.username=%s;", [school,username])
            x  = cur.fetchone()
            if x  != None:
                cur.execute("DELETE FROM client WHERE client.username=%s;", [username])
                db.connection.commit()
                flash("You deleted a user")
                cur.close()
                return redirect(url_for("manager", name = user, school = school))

            else:
                flash("That user does not belong to the school you manage!")
                cur.close()
                return redirect(url_for("manager", name = user, school = school))
      
        except Exception as e:
             flash(str(e),"danger")
             return redirect(url_for("manager", name = user, school = school))

    
    return  render_template("deleteclient.html" , form = form, table = clients)





@app.route("/addschool", methods=['GET', 'POST'])
def addschool():
    user = session["user"]
    form = SchoolForm()

    if request.method == 'POST':
        school_name = request.form['school_name']
        street_name = request.form['street_name']
        street_number = request.form['street_number']
        postal_code = request.form['postal_code']
        city = request.form['city']
        email_address = request.form['email_address']
        phone_number = request.form['phone_number']
        principal_name = request.form['principal_name']

        try:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO school(school_name,street_name,street_number,postal_code,city,email_address,phone_number,principal_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);", [school_name,street_name,street_number,postal_code,city,email_address,phone_number,principal_name])
            db.connection.commit()
            flash("Added new school library to the System,you will need someone to manage it!", "info")
            cur.close()

        except Exception as e:
             flash(str(e),"danger")
        return redirect(url_for("director", name = user))


    
    
    return  render_template("addschool.html" , form = form)




@app.route("/deleteschool", methods=['GET', 'POST'])
def deleteschool():
    user = session["user"]
    form = SchoolForm()
    cur = db.connection.cursor()
    cur.execute("SELECT * from school;")
    schools = cur.fetchall()

    if request.method == 'POST':
        school = request.form['school_name']
        
 
        try:
            cur.execute("SELECT * FROM school where school.school_name=%s;", [school] )
            y =   cur.fetchone() 
            if y == None:
                  flash("There is no such school to delete!")
                  return redirect(url_for("director", name = user, school = school))
            else:
                cur.execute("DELETE  FROM  provides WHERE  provides.school_name=%s;", [school])
                db.connection.commit()
                cur.execute("DELETE FROM  school WHERE school.school_name=%s;", [school])
                db.connection.commit()
                flash("School no longer exists in this System!", "info")
                cur.close()
                  
        except Exception as e:
             flash(str(e),"danger")
        return redirect(url_for("director", name = user, school = school))

    
    
    return  render_template("deleteschool.html" , table = schools,form = form)




    

if __name__ == "__main__":  
    app.run(debug=True)