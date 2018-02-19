# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 13:04:42 2018

@author: Proppick Solutions
"""

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps


app = Flask(__name__)

#config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL
mysql = MySQL(app)

Articles = Articles()

#logic for login required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('login'))
    return wrap

#User form registration form class
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=5, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create Cursor
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_entered = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()

        #get the username
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username]) 
        
        if result > 0:
            #get the first user detials
            data = cur.fetchone()
            #find password from the user details
            password = data['password']
            
            #compare passwords
            if sha256_crypt.verify(password_entered, password):
                #password verified
                session['logged_in'] = True
                session['username'] = username
                flash('You have successfully loggedin!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('You have entered a wrong password', 'danger')
        #condition if no user found
        else:
            flash('No user found with that username', 'danger')
    return render_template('login.html')

#route for logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('login'))

#Route for home
@app.route('/')
def home():
    return render_template('home.html')

#Route for about
@app.route('/about')
def about():
    return render_template('about.html')

#Class for adding/editing articles form 
class ArticlesForm(Form):
    title = StringField('Title', validators=[
        validators.DataRequired(),
        validators.Length(min=1, max=50)
    ])
    body = TextAreaField('Body', validators=[
        validators.Length(min=5)
    ])

#Route for adding article
@app.route('/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticlesForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title
        body = form.body
        #create cursor
        cur = mysql.connection.cursor()

        #Execute Query
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))

        #Commit to DB
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Article has been added!', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

#Route for articles index
@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

#Route for article show page
@app.route('/articles/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

#routes for dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)