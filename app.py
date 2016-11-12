from flask import Flask, render_template, request
import sys
import urllib
import arrow
import json
from dbmap import Board, Note
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/data/<data_id>', methods=['GET', 'POST'])
def board(data_id):
    # Adds note and updates time
    if request.method == 'POST':
        time = arrow.now()
        note = Note(time=time.format('YYYY-MM-DD HH:mm:ss ZZ'),
                    board_no=data_id,
                    info=request.form['boardnote'])
        session.add(note)
        session.commit()

    # Database fetch of board info
    board = session.query(Board).filter_by(board_no=data_id).first()
    notes = session.query(Note).filter_by(board_no=data_id).order_by(Note.time.desc()).all()
    bdata = []
    for entry in notes:
        data = {
                'info' : entry.info,
                'time' : entry.time
               }
        bdata.append(data)

    time = arrow.get(bdata[0]['time'], 'YYYY-MM-DD HH:mm:ss ZZ')

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
    engine = create_engine('sqlite:///tests/demo_board.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    app.run('0.0.0.0', debug=True)

