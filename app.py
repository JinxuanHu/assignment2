from flask import Flask, escape, request
import json
import sqlite3
from sqlite3 import Error
app = Flask(__name__)
test_id = 0
scantron_id = 0;
score = 0
ss_result = {}
ans_keys = {}

@app.route('/api/tests', methods=['POST'])
def create_test():
   global test_id
   global t_answers
   con = sqlite3.connect('echo.db')
   cur = con.cursor()
   test_id += 1
   t_subject = request.get_json()['subject']
   t_answers = request.get_json()['answer_keys']
   for item in t_answers:
      ans_id = item
      ans_value = t_answers[item]
      cur.execute("INSERT INTO test(test_id, t_subject, ans_id, ans_value,submission) VALUES(?,?,?,?,?)",(test_id, t_subject, ans_id, ans_value,""))
      con.commit()
   cur.execute("SELECT ans_value FROM test")
   result = cur.fetchall()
   con.close()
   return{
      "test_id" : test_id,
      "subject" : t_subject,
      "answer_keys": t_answers, 
      "submission" :[]
   },201

@app.route('/api/tests/<test_id>/scantrons', methods = ["POST"])
def create_scantron(test_id):
   global scantron_id
   global score
   global file
   con = sqlite3.connect('echo.db')
   cur = con.cursor()
   scantron_id += 1
   scantron_url = "http://localhost:5000/files/scantron-1.json"
   name = request.get_json()['name']
   s_subject = request.get_json()['subject']
   s_answers = request.get_json()['answers']
   
   for item in s_answers:
      result = item
      actual = s_answers[item]
      expected = t_answers[item]
      if actual == expected:
         score += 1
      cur.execute("INSERT INTO scantron(scantron_id, scantron_url, s_name, s_subject,score, result,actual, expected) VALUES(?,?,?,?,?,?,?,?)",(scantron_id,scantron_url,name,s_subject,score,result,actual,expected))
      con.commit()
      # cur.execute("INSERT INTO files(f_subject,f_name, id, answer) VALUES(?,?,?,?)",(s_subject,name,result,actual))
      # con.commit()  
   cur.execute("SELECT result, actual, expected FROM scantron")
   s_result = cur.fetchall()
   for item in range(0,50):
      ss_result.update({s_result[item][0]:{"actual":s_result[item][1], "expected" :s_result[item][2]}})
   # print(ss_result)  
   con.close()
   return{
      "scantron_id": scantron_id,
      "scantron_url": scantron_url,
      "name": name,
      "subject": s_subject,
      "score": score,
      "result": ss_result
   },201

@app.route('/api/tests/<t_id>', methods = ["GET"]) 
def check_submissions(t_id):
   con = sqlite3.connect('echo.db')
   cur = con.cursor()
   cur.execute(f"SELECT t_subject FROM test WHERE test_id = {t_id}")
   tt_subject = cur.fetchone()
   t_subject = tt_subject[0]
   cur.execute(f"SELECT ans_id,ans_value FROM test WHERE test_id = {t_id} ORDER BY test_id")
   keys = cur.fetchall()
   for item in range(0,50):
      ans_keys.update({keys[item][0]:keys[item][1]})
   cur.execute(f"SELECT scantron_id FROM scantron")
   s_id = cur.fetchone()
   scantron_id = s_id[0]
   cur.execute(f"SELECT scantron_url FROM scantron")
   s_url = cur.fetchone()
   scantron_url = s_url[0]
   cur.execute(f"SELECT s_name FROM scantron")
   s_name = cur.fetchone()
   name = s_name[0]
   cur.execute(f"SELECT s_subject FROM scantron")
   ss_subject = cur.fetchone()
   s_subject = ss_subject[0]
   cur.execute(f"SELECT score FROM scantron where  result = 50")
   s_score = cur.fetchone()
   score = s_score[0]
   cur.execute("SELECT result, actual, expected FROM scantron")
   s_result = cur.fetchall()
   for item in range(0,50):
      ss_result.update({s_result[item][0]:{"actual":s_result[item][1], "expected" :s_result[item][2]}})
   
   return{
      "test_id": t_id,
      "subject": t_subject,
      "answer_keys": ans_keys,
      "submission": [{
         "scantron_id": scantron_id,
         "scantron_url": scantron_url,
         "name":name,
         "score":score,
         "result":ss_result

      }
      ]
   }

@app.route('/files/<f_name>', methods = ["GET"]) 
def get_files(f_name):
   con = sqlite3.connect('echo.db')
   cur = con.cursor()
   name = cur.execute(f"SELECT s_name FROM scantron")
   s_name = cur.fetchone()
   name = s_name[0]
   cur.execute(f"SELECT s_subject FROM scantron")
   ss_subject = cur.fetchone()
   s_subject = ss_subject[0]
   cur.execute("SELECT result, actual FROM scantron")
   s_result = cur.fetchall()
   for item in range(0,50):
      ss_result.update({s_result[item][0]:s_result[item][1]})
   return{
      "name":name,
      "subject":s_subject,
      "answers":ss_result
   }
   
       
      

   

   