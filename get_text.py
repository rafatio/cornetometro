import json

f = open("data/twitter_data.txt")


for line in f:
	try:
		obj = json.loads(line)
		print obj['text']
		print "####################"
	except:
		pass

f.close()
