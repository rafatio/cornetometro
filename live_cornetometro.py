#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tokens import *
import json
import time
import sys
from cornetometro import Cornetometro

class CornetometroListener(StreamListener):
    def __init__(self, teams, players):
        self.cornetometro = Cornetometro(teams, players)
        self.cornetometro.load('classifier.obj')
        self.time = time.time()
        self.print_scores()

    def on_data(self, data):
        tweet_json = json.loads(data)
        if not tweet_json['text'].startswith('RT'):
            tweet = tweet_json['text']
            self.cornetometro.classify(tweet)

        if self.__minute_passed():
            self.record_scores()
            self.time = time.time()

        return True

    def record_scores(self):
        # Could do more than printing, like saving or putting in a list
        self.print_scores()

    def print_scores(self):
        print time.strftime("%H:%M:%S")
        for player in self.cornetometro.players:
            stats = self.cornetometro.get_stats(player)
            print "{}: {}   ({} / {})".format(player, self.cornetometro.get_score(player), stats['positive'], stats['negative'])
        print ''

    def __minute_passed(self):
        return time.time() - self.time >=  60

    def on_error(self, status):
        print status


def main():
    if len(sys.argv) < 2:
        print "ERROR: Less arguments than expected"
        print "python live_cornetometro.py <input file>"
        return

    input_file = open(sys.argv[1])
    teams = input_file.readline().split(',')
    players = input_file.readline().split(',')
    input_file.close()

    for i in xrange(len(teams)):
        teams[i] = teams[i].strip()

    for i in xrange(len(players)):
        players[i] = players[i].strip()

    listener = CornetometroListener(teams, players)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    stream.filter(languages=['en'], track=players)

if __name__ == '__main__':
    main()
