#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tokens import *
import json
import time

class CustomListener(StreamListener):
    def __init__(self, teams, players):
        self.tweets_json_file = open("data/twitter_data_" + time.strftime("%H:%M:%S_%d-%m"), "w")
        self.tweets_json_file.write(' '.join(teams))
        self.tweets_json_file.write('\n')
        self.tweets_json_file.write(' '.join(players))
        self.tweets_json_file.write('\n')

    def on_data(self, data):
        tweet_json = json.loads(data)
        if not tweet_json['text'].startswith('RT'):
            self.tweets_json_file.write(data)
            print tweet_json
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__': 
    teams = ['Barcelona', 'Barca', 'Athletic', 'Bilbao']
    players = ['Cillessen', 'Sergi', 'Roberto', 'Pique', 'Umtiti', 'Jordi', 'Alba', 'Busquets', 'Iniesta', 'Rafinha', 'Alcantara', 'Messi', 'Neymar', 'Suarez', 'Iraizoz',  'Boveda', 'Etxeita', 'Laporte', 'Balenziaga', 'San Jose', 'Benat', 'Eraso', 'Inaki', 'Williams', 'Saborit', 'Sabin', 'Merino']

    listener = CustomListener(teams, players)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    #players_list = ['stegen', 'pique', 'rakitic', 'suarez', 'messi', 'neymar', 'mascherano', 'alba', 'navas', 'carvajal', 'sergio ramos', 'varane', 'cristiano ronaldo', 'cr7', 'benzema', 'marcelo', 'kovacic', 'vazquez', 'modric', 'isco']

    #stream.filter(languages=['en'], track=['bravo', 'fernandinho', 'gundogan', 'navas', 'silva', 'de bruyne', 'aguero', 'curtois', 'kolarov', 'cahill', 'kante', 'fabregas', 'pedro', 'costa', 'hazard'])
    stream.filter(languages=['en'], track=players)
