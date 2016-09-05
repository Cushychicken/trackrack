require 'Faker'
require 'json'

def makeBoardInfo()
	boardInfo = []
	(0..rand(25)).each do |counter| 
		data = {
			"info" => Faker::Lorem.sentence,
			"time" => Faker::Time.between(DateTime.now - 7, DateTime.now)
		}
		boardInfo << data
	end
	return boardInfo
end

def makeTestDataset()
	boardLotInfo = {} 
	(0..rand(25)).each do |counter|
		length = 13
		board_no = rand(36**length).to_s(36)
		data = {
			"owner"			=> Faker::Name.name,
			"last_update"	=> Faker::Time.between(DateTime.now - 1, DateTime.now),
			"mac_addr"		=> Faker::Internet.mac_address,
			"notes"			=> makeBoardInfo()
		}
		boardLotInfo[board_no] = data
	end
	return boardLotInfo
end

data = makeTestDataset()
File.open("demo_data.json", "w") do |f|
	f.write(data.to_json)
end
