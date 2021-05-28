# -*- coding: utf-8 -*-
"""
Created on Mon May  3 20:44:43 2021

@author: Lenovo
"""
from flask import Flask, jsonify
from flask import render_template, request, make_response, g
# from flask import redirect, url_for
from flask_cors import CORS
from jinja2 import TemplateNotFound
# from datetime import datetime
from config.Settings import Settings
from model.User import User
from model.Prediction import Prediction
from validation.Validator import *
import numpy as np
import os, pickle

labels = ['Iris Setosa', 'Iris Versicolour', 'Iris Virginica']

app = Flask(__name__, template_folder='templates')
# CORS(app) # to enable CORS middleware for all origins

model = None
# if os.path.isfile(Settings.modelFile):
#     print('Model file found. Loading model .....')
#     model = pickle.load(open(Settings.modelFile, 'rb'))
# else:
#     print('Model file not found. Model not loaded.')

#@app.route('/', methods=['GET','POST'])
@app.route('/')
def homepage():
    return render_template('login.html',
                            loggingIn=False, # user needs login screen
                            registering=False, # user needs register screen
                            forgotpass=False, # forgot password screen
                            displayMesg=False, # display message on login screen
                            displayMesgr=False, # display message on register screen
                            displayMesgf=False),200 # display message on forgot password screen

@app.route('/loggingIn', methods=['GET','POST'])
def loginpage():
    return render_template('login.html',
                            loggingIn=True,
                            registering=False,
                            forgotpass=False,
                            displayMesg=False,
                            displayMesgr=False,
                            displayMesgf=False),200

@app.route('/registering', methods=['GET','POST'])
def registeringpage():
    return render_template('login.html',
                            loggingIn=False,
                            registering=True,
                            forgotpass=False,
                            displayMesg=False,
                            displayMesgr=False,
                            displayMesgf=False),200

@app.route('/changepass', methods=['GET','POST'])
def changingpage():
    return render_template('login.html',
                            loggingIn=False,
                            registering=False,
                            forgotpass=True,
                            displayMesg=False,
                            displayMesgr=False,
                            displayMesgf=False),200

# @app.route('/shortcut', methods=['GET','POST'])
# @require_login
# def shortcut():
#     info = Prediction.initPredInfo()
#     return render_template('prediction.html', info=info),200

@app.route('/predict', methods=['POST'])
@require_login
def predict():
    # print('Predicting for userid: ', g.userid)
    info = Prediction.loadPredInfo(g.userid,
                                   float(request.form['sepallengthinput']),
                                   float(request.form['sepalwidthinput']),
                                   float(request.form['petallengthinput']),
                                   float(request.form['petalwidthinput']),
                                   '')
    data = np.zeros((1, 4))
    data[0,0] = info['sepalLength']
    data[0,1] = info['sepalWidth']
    data[0,2] = info['petalLength']
    data[0,3] = info['petalWidth']
    output = model.predict(data)[0]
    # output = 0

    if output >= 0 and output < 3:
        info['prediction'] = labels[output]
    else:
        info['prediction'] = 'Unknown'
    pid = Prediction.insert(info)
    fromdb = Prediction.get(pid)
    return render_template('prediction.html', info=fromdb),200

@app.route('/deletePredInfo',methods=['POST'])
def delete():
    try:
        predictionId = request.form['predictionId']
        output = Prediction.delete(predictionId)
        info = Prediction.initPredInfo()
        return render_template('prediction.html', info=info),200

    except Exception as err:
        print(err)
        return {'Rows Affected': 0},500


@app.route('/logoutUser', methods=['GET','POST'])
def logout():
    resp = make_response(render_template("login.html",
                                         loggingIn=False,
                                         registering=False,
                                         forgotpass=False,
                                         displayMesg=False,
                                         displayMesgr=False,
                                         displayMesgf=False))
    resp.delete_cookie('jwt')
    return resp
    
@app.route('/user', methods=['POST'])
@validateRegister
def insertUser():
    username = request.form['usernamer']
    email = request.form['emailr']
    role = request.form['roler']
    password = request.form['passwordr']
    password1 = request.form['passwordr1']

    if (password == password1):
        try:        
            output = User.insertUser(username, email, role, password)
            jsonOutput = {'Rows Affected' : output}
            return render_template('login.html',
                                    loggingIn=False,
                                    registering=False,
                                    forgotpass=False,
                                    displayMesg=False,
                                    displayMesgr=False,
                                    displayMesgf=False),201

        except Exception as err:
            print(err)
            return render_template('login.html',
                                    loggingIn=False,
                                    registering=True,
                                    forgotpass=False,
                                    displayMesg=False,
                                    displayMesgr=True,
                                    displayMesgf=False),500

    else:   # password != password1
        return render_template('login.html',
                                loggingIn=False,
                                registering=True,
                                forgotpass=False,
                                displayMesg=False,
                                displayMesgr=True,
                                displayMesgf=False),500

@app.route('/userChangePassword', methods=['POST'])
@validatePassword
def updateUser():
    username = request.form['usernamef']
    email = request.form['emailf']
    password = request.form['passwordf']
    password1 = request.form['passwordf1']

    if (password == password1):
        try:        
            output = User.updateUser(username, email, password)
            jsonOutput = {'Rows Affected' : output}

            if output > 0:
                return render_template('login.html',
                                        loggingIn=False,
                                        registering=False,
                                        forgotpass=False,
                                        displayMesg=False,
                                        displayMesgr=False,
                                        displayMesgf=False),201
                                        
            else:
                return render_template('login.html',
                                        loggingIn=False,
                                        registering=False,
                                        forgotpass=True,
                                        displayMesg=False,
                                        displayMesgr=False,
                                        displayMesgf=True),500

        except Exception as err:
            print(err)
            return render_template('login.html',
                                    loggingIn=False,
                                    registering=False,
                                    forgotpass=True,
                                    displayMesg=False,
                                    displayMesgr=False,
                                    displayMesgf=True),500

    else:   # password != password1
        return render_template('login.html',
                                loggingIn=False,
                                registering=False,
                                forgotpass=True,
                                displayMesg=False,
                                displayMesgr=False,
                                displayMesgf=True),500

@app.route('/verifyUser', methods=['POST'])
def verifyUser():
    try:
        output = User.loginUser(request.form['email'], request.form['password'])
        if len(output['jwt']) > 0:
            info = Prediction.initPredInfo()
            resp = make_response(render_template('prediction.html', info=info),200)
            resp.set_cookie('jwt', output["jwt"]) #writes instructions in the header for browser to save a cookie to browser for the jwt 
            return resp

        else:
            return render_template('login.html',
                                    loggingIn=True,
                                    registering=False,
                                    forgotpass=False,
                                    displayMesg=True,
                                    displayMesgr=False,
                                    displayMesgf=False),401

    except Exception as err:
        print(err)
        return render_template('login.html',
                                loggingIn=True,
                                registering=False,
                                forgotpass=False,
                                displayMesg=True,
                                displayMesgr=False,
                                displayMesgf=False),401

@app.route('/<string:page>')
def getPage(page):
    try:
        return render_template(page),200

    except TemplateNotFound:
        return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)
