from itertools import count
from tkinter.messagebox import RETRY
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

class Urls(db.Model):
    id_ = db.Column("id_",db.Integer,primary_key = True)
    long = db.Column("long",db.String())
    short = db.Column("short",db.String())
    def __init__(self,long,short,id):
        self.long = long
        self.short = short
        self.id_ = id

def idToShortURL(id):
    map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    shortURL = ""
     
    # for each digit find the base 62
    while(id > 0):
        shortURL += map[id % 62]
        id //= 62
 
    # reversing the shortURL
    return shortURL[len(shortURL): : -1]
 
def shortURLToId(shortURL):
    id = 0
    for i in shortURL:
        val_i = ord(i)
        if(val_i >= ord('a') and val_i <= ord('z')):
            id = id*62 + val_i - ord('a')
        elif(val_i >= ord('A') and val_i <= ord('Z')):
            id = id*62 + val_i - ord('Z') + 26
        else:
            id = id*62 + val_i - ord('0') + 52
    return id

@app.route('/display/<url>',methods=['POST','GET'])
def display_shorten_url(url):
    return render_template('shorturl.html',short_url_display = url)

@app.route('/shorty/<short_url>',methods=['POST','GET']) 
def redirection(short_url) :
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return f'<h1>Url doesnt exist</h1>'

@app.route('/',methods=['POST','GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        #check if the url already existed in the database
        found_url = Urls.query.filter_by(long = url_received).first()
        if found_url:
            #return short url
            return redirect(url_for("display_shorten_url",url = found_url.short))
        else:
            #create short URL 
            counter = Urls.query.count()
            short_url = idToShortURL(counter+100)
            new_url = Urls(url_received,short_url,counter)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_shorten_url",url =short_url))
    else:
        return render_template('url_page.html')



if __name__ == "__main__" :
    app.run(debug = True)

