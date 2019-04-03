# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask, Response
from flask_restplus import Resource, Api, apidoc
import db_manipulation as db
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Dentist',
    description='Dentist Information API',)
db_name = "data.db"
@api.documentation
def swagger_ui():
    return apidoc.ui_for(api)

@api.response(200, 'OK')
@api.response(401, "Unauthorized")
@api.response(404, 'Not found')
@api.route('/dentists', endpoint="dentists")
class getDentistList(Resource):
    @api.doc(description='Get list of available dentists. No parameter needed, will return sqlite result'
                         ' in JSON format.')
    def get(self):
        conn, c = db.dentist_list('*')
        dentist_list = c.fetchall()
        conn.close()
        return Response(status=200, response=json.dumps(dentist_list))

@api.response(200, 'OK')
@api.response(401, "Unauthorized")
@api.response(404, 'Not found')
@api.route('/dentists/<name>', endpoint="docInfo")
class getDocInfo(Resource):
    @api.doc(description='Get information of a dentist by get dentist name. Need put a valid name in url to get '
                         'information of dentist related to the name.')
    def get(self, name):
        conn, c = db.dentist_list(name)
        dentist = c.fetchone()
        conn.close()
        return Response(status=200, response=json.dumps(dentist))


if __name__ == '__main__':
    db.create_db(db_name)
    app.run(host='0.0.0.0', port=9101)
