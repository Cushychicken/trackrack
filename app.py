from flask import Flask, render_template, request
import urllib
import arrow
import json
import socket 
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


app = Flask(__name__)

@app.route('/data/<data_id>', methods=['GET', 'POST'])
def board(data_id):
    time = ''
    if request.method == 'POST':
        time = arrow.now()
        newnote = { "time" : time.format('YYYY-MM-DD HH:mm:ss ZZ'), 
                    "info" : request.form['boardnote'] }
        DATA[data_id]['notes'].append(newnote)
        DATA[data_id]['last_update'] = time.format('YYYY-MM-DD HH:mm:ss ZZ')
    else:
        time = arrow.get(DATA[data_id]['last_update'], 'YYYY-MM-DD HH:mm:ss ZZ')
    
    tmp = DATA[data_id]
    return render_template('board.html', 
                           owner=tmp['owner'],
                           board_no=data_id,
                           last_update=time.humanize(),
                           mac_addr=tmp['mac_addr'],
                           notes=tmp['notes'])

@app.route('/', methods=['GET'])
def boardlist():
    return render_template('boardlist.html',
                            data=DATA)

@app.route('/data/<data_id>/checkout', methods=['GET'])
def checkout(data_id):
    new_owner = request.args.get('email')
    return render_template('checkout.html',
                           board_no=data_id,
                           new_owner=new_owner,
                           owner=DATA[data_id]['owner'])

@app.route('/scansetup/', methods=['GET', 'POST'])
def scansetup():
    if request.method == 'POST':
        tmp = 'http://{1}:5000/data/%s?email={2}'
        email = request.form['email']
        ipadr = get_ip_address('eth0')
        tmp = tmp.format(ipadr, email)
        tmp = urllib.urlencode(tmp)
        return tmp
        
        

if __name__ == '__main__':
    with open('tests/demo_data.json') as data_file:    
        DATA = json.load(data_file)
        app.run('0.0.0.0', debug=True)
