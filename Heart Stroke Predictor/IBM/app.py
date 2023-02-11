# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 13:39:41 2020

@author: DELL
"""

from flask import Flask, render_template, request# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.

import numpy as np #used for numerical analysis
import requests
import pickle

#model = pickle.load(open("F:/notebook/heart_stroke/Model Building/cardiac_arrest_model.pkl", "rb"))
app = Flask(__name__) #our flask app
API_KEY = "B5kSmOXG37q7eziVgOOX7fuTRILBd46FRUtsMkJx-iwA"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


@app.route('/') #default route
def hello_world():
  return render_template("index.html")
  
@app.route('/login', methods = ['POST']) #Main page route
def admin():

  q = request.form['age']
  r = 1 if request.form['anaemia'] == "yes" else 0
  s = request.form['cpl']
  t = 1 if request.form['diabetes'] == "yes" else 0
  u = request.form['efl']
  v = request.form['hbpl']
  p = request.form['p']
  w = request.form['scl']
  x = request.form['ss']
  y = 1 if request.form['gender'] == "male" else 0
  z = 1 if request.form['smoking'] == "yes" else 0

  sample = [[q, r, s, t, u, v, p, w, x, y, z]]
  payload_scoring = {"input_data": [{"fields": ["gender","age","hypertension","heart_disease","ever_married","work_type","Residence_type","avg_glucose_level","bmi","smoking_status","stroke"], "values": sample}]}

  response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/02b82cc5-dfe3-49e3-93ef-328c0612912f/predictions?version=2023-02-11', json=payload_scoring,
  headers={'Authorization': 'Bearer ' + mltoken})
  print("Scoring response")
  predictions=response_scoring.json()
  test = predictions['predictions'][0]['values'][0][0][0]
  if test == 0:
     test = "The Risk of Heart Stroke is Low. "
  elif test == 1:
    test = "The Risk of Heart Stroke is High. "

  return render_template("index.html", test = test)


# age,anaemia,creatinine_phosphokinase,diabetes,ejection_fraction,
# high_blood_pressure,platelets,serum_creatinine,serum_sodium,
# sex,smoking,time,DEATH_EVENT


@app.route('/user')
def user():
  return "Hye User"



if __name__ == '__main__':
  #app.run(host='0.0.0.0', port=8000,debug=False)
  app.run(debug = True) #running our flask app