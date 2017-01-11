file_paths = ['mac-che-text.txt', 'mac-che2-text.txt', 'mac-che3-text.txt', 'mac-che4-text.txt']

count = 0
metadata_saved = False

for path in file_paths:
	file = open(path)

	teams = file.readline()[:-1]
	players = file.readline()[:-1]

	if not metadata_saved:
		print teams
		print players
		metadata_saved = True

	tweet = ''	

	for line in file:
		tweet += line
		
		if line[:3] == '###':
			if tweet[:2] != 'RT':
				print tweet[:-1]
				count += 1
			tweet = ''
	file.close()
