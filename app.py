from flask import Flask, render_template, request
<<<<<<< HEAD
<<<<<<< HEAD
import sys
import dataset
import urllib
import arrow
import json
from dbmap import Board, Note
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
=======
import urllib
import arrow
import json
import helpers
>>>>>>> origin/master
=======
import urllib
import arrow
import json
import helpers
>>>>>>> origin/master

app = Flask(__name__)

@app.route('/data/<data_id>', methods=['GET', 'POST'])
def board(data_id):
    board = session.query(Board).filter_by(board_no=data_id).first()
    notes = session.query(Note).filter_by(board_no=data_id).all()
    bdata = []
    for entry in notes:
        data = {
                'info' : entry.info,
                'time' : entry.time
               }
        bdata.append(data)
    print bdata
    time = ''
    if request.method == 'POST':
        time = arrow.now()
        newnote = { "time" : time.format('YYYY-MM-DD HH:mm:ss ZZ'), 
                    "info" : request.form['boardnote'] }
        DATA[data_id]['notes'].append(newnote)
        DATA[data_id]['last_update'] = time.format('YYYY-MM-DD HH:mm:ss ZZ')
    else:
        time = arrow.get(board.last_update, 'YYYY-MM-DD HH:mm:ss ZZ')
    return render_template('board.html', 
                           owner=board.owner,
                           board_no=data_id,
                           last_update=time.humanize(),
                           mac_addr=board.mac_addr,
                           notes=bdata)

@app.route('/', methods=['GET'])
def boardlist():
    data = session.query(Board).all()
    boards = {}
    for entry in data:
        data = {
                'owner'       : entry.owner,
                'mac_addr'    : entry.mac_addr,
                'last_update' : entry.last_update
               }
        boards[entry.board_no] = data
    return render_template('boardlist.html',
                            data=boards)

@app.route('/data/<data_id>/checkout', methods=['GET'])
def checkout(data_id):
    new_owner = request.args.get('email')
    print new_owner
    return render_template('checkout.html',
                           board_no=data_id,
                           new_owner=new_owner,
                           owner=DATA[data_id]['owner'])

<<<<<<< HEAD
<<<<<<< HEAD
if __name__ == '__main__':   
    engine = create_engine('sqlite:///tests/demo_board.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    app.run('0.0.0.0', debug=True)
=======
=======
>>>>>>> origin/master
@app.route('/scansetup', methods=['GET', 'POST'])
def scansetup():
    if request.method == 'POST':
        tmp   = 'http://{0}:5000/data/%s?'
        email = urllib.urlencode({'email' : request.form['email']})
        ipadr = helpers.get_ip_address('wlxb07fb94fbcab')
        tmp   = tmp.format(ipadr) + email
        return render_template('appsetup.html', tmp=tmp)
    else:
        return render_template('appsetup.html')

        

if __name__ == '__main__':
    with open('tests/demo_data.json') as data_file:    
        DATA = json.load(data_file)
        app.run('0.0.0.0', debug=True)
>>>>>>> origin/master
