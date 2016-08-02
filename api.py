#!/usr/bin/python

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import arrow

app = Flask(__name__)
api = Api(app)

DATA = {
    'data1': {'meas': 123, 'time': '2016-01-02 11:28:09 -05:00'},
    'data2': {'meas': 456, 'time': '2016-01-02 11:28:11 -05:00'},
    'data3': {'meas': 789, 'time': '2016-01-02 11:28:13 -05:00'},
}


def abort_if_data_doesnt_exist(data_id):
    if data_id not in DATA:
        abort(404, message="data {} doesn't exist".format(data_id))

parser = reqparse.RequestParser()
parser.add_argument('meas', required=True)

# data
# shows a single data item and lets you delete a data item
class Data(Resource):
    def get(self, data_id):
        print "Data:", data_id
        abort_if_data_doesnt_exist(data_id)
        return DATA[data_id]

    def delete(self, data_id):
        abort_if_data_doesnt_exist(data_id)
        del DATA[data_id]
        return '', 204

    def put(self, data_id):
        args = parser.parse_args()
        meas = {'meas': args['meas']}
        DATA[data_id] = meas
        return meas, 201


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
        args = parser.parse_args()
        data_id = int(len(DATA)) + 1
        data_id = 'data%i' % data_id
        print data_id, args
        time = arrow.now().format('YYYY-MM-DD HH:mm:ss ZZ') 
        DATA[data_id] = {'meas': args['meas'],
                         'time': time}
        return DATA[data_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(DataList, '/', '/data')
api.add_resource(Data, '/data/<data_id>')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
