from flask import Flask, render_template, request, session,redirect, escape, url_for

import re

from datetime import datetime

from flask_bcrypt import Bcrypt

from users import adduser, validateLogin

from bankaccount import BankAccount

import sqlite3

from htmltest import convert

from dateutil import tz

import secret_key
app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = secret_key

error = ''
@app.route('/')
def greet():

    if 'username' in session:

        return redirect(url_for('index'))

    return render_template('login.html',error='')

@app.route('/login',methods=['POST'])
def login():
    post = request.form
    try:  
        pw_hash = bcrypt.generate_password_hash(post['pwd'],10).decode('utf-8')

        if bcrypt.check_password_hash((validateLogin(post['userid'])),post['pwd']):
            
            session['username'] = post['userid']
            
            error = ''

            return redirect(url_for('index'))

        else:
            return render_template('login.html',error='incorrect username/password')
    except ValueError:
        error = "please enter a username and password"

        return render_template('login.html',error=error)
    except TypeError:

        error = "please enter a valid username and password"

        return render_template('login.html',error=error)

@app.route('/index',methods=['GET'])
def index():

    user = BankAccount(session['username'],0)
    
    rec_trans = []

    for x in user.recents():
        a,b,c = x
        
        fromz = tz.tzutc()
        
        toz = tz.tzlocal()

        utc = datetime.strptime(b,'%Y-%m-%d %H:%M:%S.%f')

        utc = utc.replace(tzinfo=fromz)

        b = utc.astimezone(toz)

        rec_trans.append([str(b.date())+' '+str(b.hour)+':'+str(b.minute)+':'+str(b.second),str(c)])

    rec_trans = list(reversed(rec_trans))[0:9]
    return render_template('index.html',amount=str(user.getBalance()),username=session['username'],recents=convert(rec_trans))

    #return "{} : {}".format(escape(session['username']),escape(str(user.getBalance())))

@app.route('/logout')
def logout():

    session.pop('username',None)
    return redirect('/')

@app.route('/create',methods=['POST'])
def create():

    post = request.form

    try:    
        pw_hash = bcrypt.generate_password_hash(post['pwd']).decode('utf-8')
        adduser(post['userid'],pw_hash)
        error = "success"
        return render_template('login.html',error=error)
    except sqlite3.IntegrityError:
        error = "username already taken"
        return render_template('login.html',error=error)
    except ValueError:
        error = "please enter a username and password"

        return render_template('login.html',error=error)
@app.route('/deposit',methods=['POST'])
def deposit():

    if re.match(r'\d+',request.form['amount']):

        user = BankAccount(session['username'],0)

        user.deposit(float(request.form['amount']))

        return redirect(url_for('index'))
    else:
        
        return redirect(url_for('index'))


@app.route('/withdraw',methods=['POST'])
def withdraw():
    if re.match(r'\d+',request.form['amount']):

        user = BankAccount(session['username'],0)

        user.withdraw(float(request.form['amount']))

        return redirect(url_for('index'))

    else:
        
        return redirect(url_for('index'))

@app.route('/transfer',methods=['POST'])
def transfer():

    if re.match(r'\d+',request.form['amount']):

        user = BankAccount(session['username'])

        user.transfer(float(request.form['amount']),request.form['target'])

        return redirect(url_for('index'))

    else:
        
        return redirect(url_for('index'))


