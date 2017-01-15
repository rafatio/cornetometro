import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import build_classifier
from preprocessing import preprocess_tweet
import pickle

POSITIVE = 'positive'
NEGATIVE = 'negative'
NONE = 'none'

DEFAULT_CONFIDENCE_THRESHOLD = 0.85

# THE MAIN CLASS
# 1) INSTANCE THIS CLASS WITH A LIST OF TEAMS AND A LIST OF PLAYERS
# 2) LOAD OR TRAIN THE CLASSIFIER
# 3) FEED IT THE TWEETS
# 4) GET THE STATS

class Cornetometro:
    def __init__(self, teams, players):
        self.classifier = None
        self.teams = teams
        self.players = players

        self.count = {}
        for player in players:
            self.count[player.lower()] = {POSITIVE: 0, NEGATIVE: 0}
        self.confidence_threshold = DEFAULT_CONFIDENCE_THRESHOLD

    def train(self, dataset_path):
        self.classifier = build_classifier.classifier(dataset_path)

    def load(self, file_path):
        input_file = open(file_path)
        self.classifier = pickle.load(input_file)
        input_file.close()

    def classify(self, tweet):
        processed_tweet = self.__preprocess_tweet(tweet)
        answer = self.classifier.classify(processed_tweet)

        dist = self.classifier.prob_classify(processed_tweet)
        if dist.prob(dist.max()) > self.confidence_threshold:
            for player in self.players:
                for name in player.split():
                    if name.lower() in tweet.lower():
                        self.count[player.lower()][answer] += 1
                        break

            return answer
        else:
            return NONE

    def get_stats(self, player):
        return self.count[player.lower()]

    def get_score(self, player):
        pos = self.get_stats(player)[POSITIVE]
        neg = self.get_stats(player)[NEGATIVE]
        total = pos + neg

        if total == 0 or pos - neg == 0:
            return 5.0

        max_tweets = self.__max_tweets()
        amount_proportion = float(total)/(0.5*max_tweets) if float(total) < 0.5*max_tweets else 1
        amount_weight = (1 + (4 * amount_proportion)) / 5

        if pos > neg:
            outlook = 1
            digg = pos - neg
        else:
            outlook = -1
            diff = neg - pos

        weight = float(diff) / total

        score = 5.0 + (outlook * 5 * amount_weight * weight)
        return score

    def __max_tweets(self):
        maxt = 0
        for player in self.players:
            pos = self.get_stats(player)[POSITIVE]
            neg = self.get_stats(player)[NEGATIVE]
            total = pos + neg
            if total > maxt:
                maxt = total

        return maxt

    def __preprocess_tweet(self, tweet):
            return self.__word_feats(nltk.word_tokenize(preprocess_tweet(tweet, self.teams, self.players)))

    def __word_feats(self, words):
        return dict([(word, True) for word in words])
