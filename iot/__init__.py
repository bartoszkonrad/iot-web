#!/usr/bin/python3
# coding: utf-8
# Bartosz Konrad <bartosz.konrad@talex.pl>

import sys
import datetime
import requests
# import logging
from flask import Flask, request, redirect, url_for, abort, send_file, Response, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_mysqldb import MySQL


# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler('/var/www/html/iot/iot/iot.log')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'zai1OoRo'
app.config['MYSQL_DB'] = 'iot'
app.config['MYSQL_HOST'] = 'localhost'
login_manager = LoginManager()
login_manager.init_app(app)

users = {'test': {'passwd': 'test'}, 'bartek': {'passwd': 'test'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    user.is_authenticated = request.form['passwd'] == users[username]['passwd']
    return user


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html', text='homecontrol login')
    try:
        username = request.form['username']
        if request.form['passwd'] == users[username]['passwd']:
            checked = 'remember' in request.form
            checked = True  # force remember
            user = User()
            user.id = username
            login_user(user, remember=checked)
            return redirect(url_for('dashboard'))
    except KeyError:
        return render_template('login.html', text='unauthorized')
        # return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/lighting')
@login_required
def lighting():
    return render_template('lighting.html')


@app.route('/temperature')
@login_required
def temperature():
    cur = mysql.connection.cursor()
    sql = '''select value from sensors where location = "rpi" order by ts desc limit 1'''
    cur.execute(sql)
    rpitemp = cur.fetchone()[0]
    sql = '''select value from sensors where location = "bdr" order by ts desc limit 1'''
    cur.execute(sql)
    bdrtemp = cur.fetchone()[0]
    sql = '''select value from sensors where location = "lvr" order by ts desc limit 1'''
    cur.execute(sql)
    lvrtemp = cur.fetchone()[0]
    return render_template('temperature.html', rpitemp=str(rpitemp), bdrtemp=str(bdrtemp), lvrtemp=str(lvrtemp))
    # return 'Temperature; Logged in as: ' + current_user.id


@app.route('/ws')
@login_required
def ws():
    return render_template('ws.html')

@app.route('/colorpicker')
@app.route('/colorpicker/<color>')
@login_required
def colorpicker(color=None):
    return render_template('colorpicker.html', color=color)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html', text='logged out')


@login_manager.unauthorized_handler
def unauthorized_handler():
    # return 'Unauthorized'
    return render_template('login.html', text='unauthorized')

if __name__ == "__main__":
    app.run(debug=True)
