import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import json

test_id = 1



def create_database():
    con = sqlite3.connect('echo.db')
    cur = con.cursor()
    con.execute("CREATE TABLE IF NOT EXISTS test (test_id integer,t_subject text,ans_id text, ans_value text, submission text)")
    con.execute("CREATE TABLE IF NOT EXISTS scantron (scantron_id integer, scantron_url text, s_name text, s_subject text,score text, result text,actual text, expected text)")
    # con.execute("CREATE TABLE IF NOT EXISTS files (f_subject text ,f_name text, id integer, answer text)")
   
    print("success")
    
    con.close
    print ("Opened database successfully")
 

    print ("Tables created successfully")


create_database()