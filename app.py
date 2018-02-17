# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 13:04:42 2018

@author: Proppick Solutions
"""

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from  data import Articles
from flask-mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, Validators
from passlib import sha256_crypt


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


if __name__ == "__main__":
    app.run(debug=True)