#!/bin/bash
if [ -e ./demo_data.json ]; then
	echo "Deleting old JSON..."
	rm ./demo_data.json
	ruby make_testset.rb
fi

rm ./demo_board.db
python make_database.py
