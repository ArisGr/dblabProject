from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DecimalField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, NumberRange

class BookForm(FlaskForm):
    isbn = StringField(label = "ISBN", validators = [DataRequired(message = "Isbn is a required field.")])

    title = StringField(label = "Title")

    publisher = StringField(label = "Publisher", validators = [DataRequired(message = "Publisher is a required field.")])

    page_number = IntegerField(label = "Page Number", validators = [DataRequired(message = "Page number is a required field.")])

    language = StringField(label = "Language", validators = [DataRequired(message = "Language is a required field.")])

    image = StringField(label = "Image", validators = [DataRequired(message = "image is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "summary is a required field.")])

    genre = StringField(label = "genre")

    author = StringField(label = "author")

    submit = SubmitField("Submit")



class ClientForm(FlaskForm):
    username = StringField(label = "Username", validators = [DataRequired(message = "username name is a required field.")])

    first_name = StringField(label = "First Name", validators = [DataRequired(message = "first name name is a required field.")])

    last_name = StringField(label = "Last Name", validators = [DataRequired(message = "last name is a required field.")])

    passw = StringField(label = "Password", validators = [DataRequired(message = "password is a required field.")])

    occupation = StringField(label = "Occupation", validators = [DataRequired(message = "occupation is a required field." )])

    verified = StringField(label = "Verified", validators = [DataRequired(message = "verified is a required field.")])

    director_username = StringField(label = "Director Username", validators = [DataRequired(message = "director usename is a required field.")])

    age = IntegerField(label = "Age", validators = [DataRequired(message = "age is a required field.")])
    
    s_name = StringField(label = "School Name", validators = [DataRequired(message = "school name is a required field.")]) 

    select = SelectField(label = "SELECT", choices= ["manager", "teacher", "student"])
    
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    
    username = StringField(label = "Username", validators = [DataRequired(message = "username is a required field.")])

    password = StringField(label = "Password", validators = [DataRequired(message = "password is a required field.")])
    
    submit = SubmitField("Submit")


class LoansForm(FlaskForm):

    isbn = DecimalField(label = "ISBN", validators = [DataRequired(message = "isbn is a required field.")])

    username = StringField(label = "Username", validators = [DataRequired(message = "username is a required field.")])

    start_date = DateField(label = "Start Date", validators = [DataRequired(message = "start date is a required field.")])

    due_date = DateField(label = "Due Date", validators = [DataRequired(message = "due date is a required field.")])

    status = StringField(label = "status", validators = [DataRequired(message = "status is a required field.")])

    submit = SubmitField("Submit")


class SchoolForm(FlaskForm):

    school_name = StringField(label = "school_name", validators = [DataRequired(message = "school name is a required field.")])

    street_name = StringField(label = "street_name", validators = [DataRequired(message = "street name is a required field.")])

    street_number = IntegerField(label = "street_number", validators = [DataRequired(message = "street number is a required field.")])

    postal_code = IntegerField(label = "postal_code", validators = [DataRequired(message = "postal code  is a required field.")])

    city = StringField(label = "city", validators = [DataRequired(message = "city is a required field.")])

    email_address = StringField(label = "email_address", validators = [DataRequired(message = "email address is a required field.")])

    phone_number = IntegerField(label = "phone_number", validators = [DataRequired(message = "phone number  is a required field.")])

    principal_name = StringField(label = "principal_name", validators = [DataRequired(message = "principal name is a required field.")])

    manager_id = StringField(label = "manager_id")

    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):

    isbn = DecimalField(label = "isbn", validators = [DataRequired(message = "isbn is a required field.")])

    username = StringField(label = "username", validators = [DataRequired(message = "username is a required field.")])

    comment = TextAreaField(label = "comment", validators = [DataRequired(message = "comment is a required field.")])

    likert = IntegerField(label = "likert", validators = [DataRequired(message = "likert is a required field.")])

    submit = SubmitField("Submit")


class GenreForm(FlaskForm):

    genre_type = StringField(label = "genre_type", validators = [DataRequired(message = "genre type is a required field.")])

    submit = SubmitField("Submit")


class SearchForm(FlaskForm):

    Title = StringField(label = "genre_type", validators = [DataRequired(message = "genre type is a required field.")])

    submit = SubmitField("Submit")






