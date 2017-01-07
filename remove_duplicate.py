import json

#f = open("data_classified/realxbarca-dataset-classified.txt")
f = open("data/realxbarca-dataset.txt")

tweets = f.readlines()

new_tweets= []
print tweets

print len(tweets)

for line in tweets:
	try:
		if line[:5] != "#####" and line not in new_tweets:
			new_tweets.append(line)
			new_tweets.append("####################")
	except:
		pass


print len(new_tweets)
print new_tweets
f.close()
