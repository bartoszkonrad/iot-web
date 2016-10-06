#!/usr/bin/python3
# coding: utf-8
# Bartosz Konrad <bartosz.konrad@gmail.com>

import datetime
from flask import Flask
from flask_mysqldb import MySQL
from flask import render_template

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'zai1OoRo'
app.config['MYSQL_DB'] = 'iot'
app.config['MYSQL_HOST'] = 'localhost'

@app.route("/")
def hello():
    sql = '''select * from sensors order by ts desc limit 1'''
    cur = mysql.connection.cursor()
    cur.execute(sql)
    rv = cur.fetchall()
    return str(rv)

@app.route('/rgb')
@app.route('/rgb/<room>')
def rgb(room=None):
    return render_template('rgb.html', room=room)

@app.route('/colorpicker')
@app.route('/colorpicker/<color>')
def colorpicker(color=None):
    return render_template('colorpicker.html', color=color)

@app.route('/ws')
def ws():
    return render_template('ws.html')


if __name__ == "__main__":
    app.run(debug=True)

