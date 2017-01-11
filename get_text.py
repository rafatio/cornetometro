import json

f = open("data/twitter_data.txt")


print f.readline()[:-1]
print f.readline()[:-1]

for line in f:
	try:
		obj = json.loads(line)
		print obj['text']
		print "####################"
	except:
		pass

f.close()
	
