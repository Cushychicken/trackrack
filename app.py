from flask import Flask, render_template, request
import arrow
import json

app = Flask(__name__)

@app.route('/data/<data_id>', methods=['GET', 'POST'])
def show(data_id):
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
def boards():
    return render_template('boardlist.html',
                            data=DATA)

@app.route('/data/<data_id>/checkout', methods=['GET'])
def checkout(data_id):
    test = "Well, check you out, {0}, looking at board {1}"
    test = test.format(request.args.get('email'), data_id)
    return test

if __name__ == '__main__':
    with open('tests/demo_data.json') as data_file:    
        DATA = json.load(data_file)
        app.run('0.0.0.0', debug=True)
