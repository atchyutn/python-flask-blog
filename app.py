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


app = Flask(__name__)
Articles = Articles()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/articles/<string:id>/')
def article(id):
    return render_template('article.html', id=id)

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=5, max=50)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='passwords do not match')
        ])
    confirm = PasswordField('confirm password', [
        validators.input_required
    ])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('register.html')
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)