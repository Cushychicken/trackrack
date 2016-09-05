import dataset
import json
import arrow

with open('demo_data.json') as f:
    data = json.load(f)

db = dataset.connect('sqlite:///demo_board.db')
table = db['boards']
notes = db['notes']
for entry in data:
    table.insert(dict(board_no   =entry,
                      last_update=data[entry]['last_update'],
                      mac_addr   =data[entry]['mac_addr'],
                      owner      =data[entry]['owner']))
    for note in data[entry]['notes']:
        notes.insert(dict(board_no = entry,
                          info     = note['info'],
                          time     = note['time']))
