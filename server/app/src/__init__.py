# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask, request, render_template, jsonify
from Wit.WitAi import ChatBotQuery
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt_refresh_token_required, set_refresh_cookies,
    create_refresh_token, set_access_cookies, unset_jwt_cookies)
import json
import requests
import db_manipulation as db
from random import randint
from datetime import timedelta, date

db_name = 'data.db'
doc_ip = 'http://172.18.0.2:9101'
time_ip = 'http://172.18.0.4:9100'
app = Flask(__name__, static_folder='static')

b_name = "data.db"
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'red-panda'

jwt = JWTManager(app)

def getID(id):
    digit = []
    for char in id:
        if char.isdigit():
            digit.append(char)
    return ''.join(digit)

@jwt.unauthorized_loader
def unauth_callback(tocken):
    return render_template('login.html'), 401

@app.errorhandler(401)
def unauthorized_page(e):
    return render_template('login.html'), 401

@app.route('/')
@jwt_required
def index():
    return render_template('index.html')

@app.route('/userlogin', methods=['POST'])
def user_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if not db.validate(username, password):
        return jsonify({"msg": "unauth"}), 401

    access_token = create_access_token(identity=username, expires_delta=False)
    refresh_token = create_refresh_token(identity=username, expires_delta=False)
    resp = jsonify({'msg': 'OK'})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@app.route('/usersignup', methods=['POST'])
def user_signup():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if not db.register(username, password):
        return jsonify({"msg": "occupied"}), 401
    access_token = create_access_token(identity=username, expires_delta=False)
    refresh_token = create_refresh_token(identity=username, expires_delta=False)
    resp = jsonify({'msg': 'OK'})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

@app.route('/logout', methods=['GET', 'POST'])
@jwt_refresh_token_required
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/userquery', methods=['POST'])
@jwt_required
def userQuery():
    current_user = get_jwt_identity()
    content = json.loads(request.data)['userquery']
    cmd = json.loads(request.data)['cmd']
    chatAnswer = ChatBotQuery(content)
    intent = chatAnswer['intent']
    name = chatAnswer['value']
    time = chatAnswer['start']
    command = "message"
    rez = "I do not quite understand, can you say it more specifically?"
    session = requests.Session()
    session.trust_env = False
    if cmd == "query":
        if intent == "dentist_list":
            r = session.get(doc_ip + '/dentists')
            r = json.loads(r.content)
            rez = "Available Dentists:\n"
            for i, dentist in enumerate(r):
                rez += str(i+1)+". " + dentist['name'] + " (" + dentist['spec'] + ')\n'
        elif intent == 'dentist':
            r = session.get(doc_ip + '/dentists/' + name)
            r = json.loads(r.content)
            if r == None:
                rez = "Doctor " + name + " does NOT exist, please try again or ask for dentists list."
            else:
                rez = "Here is information of Doctor " + r['name'] + ': Location - ' + r['location'] + ", specialization - " + r['spec']
        elif intent == 'schedule':
            r = session.get(doc_ip + '/dentists/' + name)
            r = json.loads(r.content)
            if r == None:
                rez = "Doctor " + name + " does NOT exist, please try again or ask for dentists list."
            else:
                id = r['id']
                name = r['name']
                r = session.get(time_ip + '/timeslot/' + str(id))
                r = json.loads(r.content)
                if len(r) == 0:
                    rez = "Sorry, doctor " + name + " is not available for tomorrow, please come back check tomorrow."
                else:
                    rez = "Schedule of " + name + ":<br>"
                    rez += "Tomorrow(" + str(date.today()+timedelta(days=1)).split()[0] + ")<br>"
                    index = 1
                    for timeslot in r:
                        if timeslot['status'] == 0:
                            startTime = timeslot['start']
                            rez += str(index) + ". " + str(startTime).zfill(2) + ":00 - " + str(startTime+1) + ":00<br>"
                            index += 1
        elif intent == 'book':
            command = 'book'
            rez = name + " at " + str(time).zfill(2) + ":00?"
        elif intent == 'cancel':
            command = 'cancel'
            rez = name + " at " + str(time).zfill(2) + ":00?"
        elif intent == 'cancelID':
            command = 'cancelID'
            rez = "Booking ID " + str(name)
        elif intent == 'greeting':
            greet = ["Hello", "Hi", "How can I help?", "Greetings!", "Hi, I am Dental bot, may I help you?"]
            rez = greet[randint(0, 4)]
        elif intent == 'hay':
            ans = ['I feel great!', 'Pretty good!', 'Just fine.', 'Nothing to be complained.',
                   'I feel my body is a little bit rusty.', 'I\'m doing well.']
            que = [' How\'s going?', ' How are you?', ' What\'s up?', ' How you doing?']
            rez = ans[randint(0, 5)] + que[randint(0, 3)]
        elif intent == 'ans':
            rez = 'Oh..How can I help?'
    elif cmd == "book":
        r = session.get(time_ip + '/book?name=%s&time=%s&user=%s'
                             % (name, str(time),current_user))
        rez = r.content.decode()
    elif cmd == "cancel":
        r = session.get(time_ip + '/cancel?name=%s&time=%s&user=%s'
                             % (name, str(time), current_user))
        rez = r.content.decode()
    elif cmd == "cancelID":
        name = getID(name)
        r = session.get(time_ip + '/cancel_id/%s?user=%s' % (name, current_user))
        rez = r.content.decode()
    context = {
        'cmd': command,
        'msg': rez
    }
    return json.dumps(context)
    
if __name__ == '__main__':
    db.create_db(db_name)
    app.run("0.0.0.0", port=9102)
