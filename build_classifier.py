import os
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from numpy.random import randint
import collections
import pickle

# THIS FILE TAKES THE BEST APPROACH FROM sentiment_analysis.py AND PROVIDES A WAY TO SAVE THE CLASSIFIER IN A FILE

def get_classified_tweets(dataset_path):
    positive_tweets = []
    negative_tweets = []

    file = open(dataset_path)
    for tweet in file:
        if tweet[:11] == '###!good###':
            positive_tweets.append(tweet[12:])
        elif tweet[:10] == '###!bad###':
            negative_tweets.append(tweet[11:])
    file.close()
    return positive_tweets, negative_tweets

def get_features(tokenized_tweets, sentiment):
    features = []
    for tweet in tokenized_tweets:
        tokens = {}
        for token in tweet:
            tokens[token] = True
        features.append((tokens, sentiment))
    return features

def tokenize_tweets(tweets):
    tokenized_tweets = []
    for tweet in tweets:
        tokenized_tweet = []
        words = nltk.word_tokenize(tweet)
        for word in words:
            if word not in stopwords.words('english'):
                tokenized_tweet.append(word)
        tokenized_tweets.append(tokenized_tweet)
    return tokenized_tweets

def classifier(dataset_path):
    positive_tweets, negative_tweets = get_classified_tweets(dataset_path)
    positive_features = get_features(tokenize_tweets(positive_tweets), "positive")
    negative_features = get_features(tokenize_tweets(negative_tweets), "negative")
    train_features = positive_features + negative_features

    classifier = NaiveBayesClassifier.train(train_features)
    return classifier

def save_classifier(dataset_path, destination_path):
    nb_classifier = classifier(dataset_path)
    output = open(destination_path, 'w')
    pickle.dump(nb_classifier, output, protocol=pickle.HIGHEST_PROTOCOL)
    output.close()
