#!/usr/local/bin/python

from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
import arrow
import json

app = Flask(__name__)
api = Api(app)

def abort_if_data_doesnt_exist(data_id):
    if data_id not in DATA:
        abort(404, message="data {} doesn't exist".format(data_id))

new_board_parser = reqparse.RequestParser()
new_board_parser.add_argument('boardnum', required=True)
new_board_parser.add_argument('owner')
new_board_parser.add_argument('mac_addr')

board_data_parser = reqparse.RequestParser()
board_data_parser.add_argument('owner')
board_data_parser.add_argument('mac_addr')
board_data_parser.add_argument('notes')

# data
# shows a single data item and lets you delete a data item
class Data(Resource):
    def get(self, data_id):
        print 'Data:', data_id
        abort_if_data_doesnt_exist(data_id)
        return DATA[data_id]

    def delete(self, data_id):
        abort_if_data_doesnt_exist(data_id)
        del DATA[data_id]
        return '', 204

    def put(self, data_id):
        abort_if_data_doesnt_exist(data_id)
        args = board_data_parser.parse_args()
        
        for k, v in args.iteritems():
            if v != None:
                DATA[data_id][k] = v

        DATA[data_id]['last_update'] = arrow.now().format('YYYY-MM-DD HH:mm:ss ZZ') 
        
        return DATA[data_id], 201


# dataList
# shows a list of all data, and lets you POST to add new meas
class DataList(Resource):
    def get(self):
        if len(DATA) <= 20:
            return DATA
        else:
            last = len(DATA)
            tmp = [ DATA.get('data'+str(a)) for a in range((DATA-20), DATA) ]
            return tmp

    def post(self):
        args = new_board_parser.parse_args()
        
        data_id = args['boardnum']
        data = { 'mac_addr'     : '',
                 'notes'        : '',
                 'owner'        : '',
                 'last_update'  : ''}
        
        for k, v in args.iteritems():
            if v != None:
                data[k] = v
            
        data['last_update'] = arrow.now().format('YYYY-MM-DD HH:mm:ss ZZ') 
        DATA[data_id] = data
        return DATA[data_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(DataList, '/', '/data')
api.add_resource(Data, '/data/<data_id>')

if __name__ == '__main__':
    with open('demo_data.json') as data_file:    
        DATA = json.load(data_file)
        app.run('0.0.0.0', debug=True)
