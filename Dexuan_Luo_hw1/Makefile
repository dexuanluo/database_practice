t1:
	python3 src/stats.py data/551-0125.txt output/stats.json
t2:
	python3 src/nochats.py data/nochats.py data/551-0125.txt data/551-mw-roster.csv output/nochats.json
t3:
	python3 src/convert_chats.py data/551-0125.txt output/convert_chats.json
t4:
	python3 src/convert_roster.py data/convert_roster.py data/551-mw-roster.csv output/convert_roster.json
t5:
	python3 src/load.py output/convert_chats.json output/convert_roster.json
t6:
	python3 src/search-person.py 'dexuan'
t7:
	python3 src/search-message.py 'sarah pursley'
clean:
	rm output/*.json