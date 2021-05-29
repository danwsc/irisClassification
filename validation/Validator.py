import functools
from flask import Flask, jsonify, request, g, render_template, redirect
from config.Settings import Settings

import jwt
import re

def require_login(func):
    @functools.wraps(func)
    def secure_login(*args, **kwargs):
        auth = True
        auth_token=request.cookies.get("jwt")

        if auth_token == None:
            auth = False
        if auth_token:
            try:
                print('auth_token found')
                # auth_token = auth_token.encode('utf-8')
                print('Validator.py')
                payload = jwt.decode(auth_token, Settings.secretKey, algorithms=["HS256"])
                g.userid = payload['userid'] # update info in flask application context's g which lasts for one req/res cycle
                g.role = payload['role']

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth = False # Failed check

        if auth==False:
            return render_template('login.html',
                                    loggingIn=True,
                                    registering=False,
                                    forgotpass=False,
                                    displayMesg=True,
                                    displayMesgr=False,
                                    displayMesgf=False),401
        return func(*args, **kwargs)
    
    return secure_login

def require_admin(func):
    @functools.wraps(func)
    def secure_admin(*args, **kwargs):
        auth = True
        if g.role != 'admin':
            auth = False

        if auth==False:
            return jsonify({'Message' : 'Not Authorized!'}),401 # return response

        return func(*args, **kwargs)
    
    return secure_admin

def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def secure_adminorself(*args, **kwargs):
        auth = True

        if g.role != 'admin' and g.userid != kwargs['userid']:
            auth = False # Failed check

        if auth==False:
            return jsonify({'Message' : 'Not Authorized!'}),401 # return response

        return func(*args, **kwargs)
    
    return secure_adminorself

def validateRegister(func):
    @functools.wraps(func)
    def validate(*args, **kwargs):
        username = request.form['usernamer']
        email = request.form['emailr']
        role = request.form['roler']
        password = request.form['passwordr']

        patternUsername = re.compile('^[a-zA-Z0-9_. -]+$')
        # patternEmail = re.compile('^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+@\w+\.\w+$')
        patternEmail = re.compile('^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.]+$')
        patternPassword = re.compile('^[a-zA-Z0-9]{8,}$')
        # print('Testing')
        # print(username, patternUsername.match(username))
        # print(email, patternEmail.match(email))
        # print(password, patternPassword.match(password))

        if (patternUsername.match(username) and
            patternEmail.match(email) and
            patternPassword.match(password) and
            (role.lower() == 'admin' or role.lower() == 'member' or role.lower() == 'user')):
            print('Validation correct.')
            return func(*args, **kwargs)

        else:
            # return jsonify({"Message" : "Validation Failed!"}),403 # return response
            print('Validaton failed.')
            return render_template('login.html',
                                    loggingIn=False,
                                    registering=True,
                                    forgotpass=False,
                                    displayMesg=False,
                                    displayMesgr=True,
                                    displayMesgf=False)

    return validate

def validatePassword(func):
    @functools.wraps(func)
    def validatepw(*args, **kwargs):
        password = request.form['passwordf']

        patternPassword = re.compile('^[a-zA-Z0-9]{8,}$')

        if (patternPassword.match(password)):
            print('Validation correct.')
            return func(*args, **kwargs)

        else:
            print('Validaton failed.')
            return render_template('login.html',
                                    loggingIn=False,
                                    registering=True,
                                    forgotpass=False,
                                    displayMesg=False,
                                    displayMesgr=True,
                                    displayMesgf=False)

    return validatepw
