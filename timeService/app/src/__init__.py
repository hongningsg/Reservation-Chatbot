# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask, request, Response
from flask_restplus import Resource, Api, apidoc
import db_manipulation as db
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Time Slot',
    description='Dentist Reservation API',)
db_name = "data.db"
@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)

@api.response(200, 'OK')
@api.response(401, "Unauthorized")
@api.response(404, 'Not found')
@api.route('/timeslot/<doc_id>', endpoint="decTimeslot")
class docTimeslot(Resource):
    @api.doc(description='Get time slot of a dentist by dentist id. To get a doctor ID, server will ask doctor Service'
                         ' to query related id using name. If you are using Swagger testing, you can use:\n'
                         'Tony Stark: 1, Bruce Banner: 2, Peter Parker: 3')
    def get(self, doc_id):
        conn, c = db.getDocTime(doc_id)
        timetable = c.fetchall()
        conn.close()
        return Response(status=200, response=json.dumps(timetable, sort_keys=False,
                                                        indent=4, separators=(',', ': ')))

@api.response(200, 'OK')
@api.response(401, "Unauthorized")
@api.response(404, 'Not found')
@api.route('/book', endpoint="bookDentist")
@api.doc(params = {'name': 'doc_name', 'time':'startTime', 'user':'user'})
class bookDentist(Resource):
    @api.doc(description="Make a reservation to a dentist at a time slot by query name and time of a dentist. All "
                         "three parameters are required in order to book successfully.\n"
                         "Parameters description: name(doctor name), time(start time of reservation, i.e., "
                         "if you want to book 9:00 - 10:00am then value is 9), user(username of user,"
                         " do not need encrypt here for test purpose.)")
    def get(self):
        try:
            request.args = request.args.to_dict()
            name = request.args['name']
            time = request.args['time']
            current_user = request.args['user']
        except:
            errorMessage = "Query to reservation should follow format ?name=" \
                           "<doc_name>&time=<timeslot>&user=<user>."
            return Response(status=401, response=errorMessage)
        conn, c = db.dentist_list(name)
        dentist = c.fetchone()
        conn.close()
        if dentist == None:
            rez = "Doctor " + name + " does NOT exist, please correct before reservation."
            return Response(status=200, response=rez)
        id = dentist['id']
        availability, book_id = db.book(id, time, current_user)
        if availability:
            message = "Reservation of doctor " + dentist['name'] + " at " + time\
                      + ":00 - " + str(int(time)+1) + ":00 successful! Your booking ID is " + str(book_id)
            return Response(status=200, response= message)
        conn, closetTime = db.closestTime(id)
        conn.close()
        if closetTime == None:
            message = "The time you are trying to reserve is not available tomorrow or" \
                      " I cannot understand the format you entered, please try again."
        else:
            timeslot = closetTime['start']
            message = "The time you are trying to reserve is not available or" \
                      " I cannot understand the format you entered, please try again. My suggestion " \
                      "timeslot would be " + str(timeslot).zfill(2) + ":00."
        return Response(status=200, response= message)

@api.response(200, 'OK')
@api.response(401, "Unauthorized")
@api.response(404, 'Not found')
@api.route('/cancel', endpoint="cancelTime")
@api.doc(params = {'name': 'doc_name', 'time':'startTime', 'user':'user'})
class cancelTime(Resource):
    @api.doc(description="Cancel a reservation to a dentist at a time slot by query name and time of a dentist. All "
                         "three parameters are required in order to book successfully. Only the user who made "
                         "the appointment can cancel relative reservation.\n"
                         "Parameters description: name(doctor name), time(start time of reservation, i.e., "
                         "if you want to book 9:00 - 10:00am then value is 9), user(username of user,"
                         " do not need encrypt here for test purpose.)")
    def get(self):
        try:
            request.args = request.args.to_dict()
            name = request.args['name']
            time = request.args['time']
            current_user = request.args['user']
        except:
            errorMessage = "Cancel reservation should follow format ?name=" \
                           "<doc_name>&time=<timeslot>&user=<user>."
            return Response(status=404, response=errorMessage)
        conn, c = db.dentist_list(name)
        dentist = c.fetchone()
        conn.close()
        if dentist == None:
            rez = "Doctor " + name + " does NOT exist, please correct before reservation."
            return Response(status=200, response=rez)
        id = dentist['id']
        availability = db.cancel(id, time, current_user)
        if availability:
            message = "Reservation of doctor " + dentist['name'] + " at " + time + \
                      ":00 - " + str(int(time)+1) + ":00 is cancelled!"
            return Response(status=200, response= message)
        message = "The timeslot you are trying to cancel is not reserved" \
                  " by you (" + current_user +") or" \
                  " I cannot understand the time format you entered, please try again."
        return Response(status=200, response= message)

@api.response(200, 'OK')
@api.response(401, "Unauthorized")
@api.response(404, 'Not found')
@api.route('/cancel_id/<id>', endpoint="cancelID")
@api.doc(params = {'user':'user'})
class cancelID(Resource):
    @api.doc(description="Cancel a reservation to a dentist at a time slot by booking ID. Fill parameter "
                         "user with username will be regarded as logged in. Only the user who made "
                         "the appointment can cancel relative reservation.")
    def get(self, id):
        try:
            request.args = request.args.to_dict()
            current_user = request.args['user']
        except:
            errorMessage = "Please Log in."
            return Response(status=401, response=errorMessage)
        availability = db.cancelID(id, current_user)
        if availability:
            message = "Reservation of booking " + str(id) + " is cancelled!"
            return Response(status=200, response= message)
        message = "The timeslot you are trying to cancel is not reserved" \
                  " by you (" + current_user +") or" \
                  " I cannot understand the time format you entered, please try again."
        return Response(status=200, response= message)

if __name__ == '__main__':
    db.create_db(db_name)
    app.run(host='0.0.0.0', port=9100)
