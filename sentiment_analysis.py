import os
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

def word_feats(words):
    return dict([(word, True) for word in words])
 
def get_classified_tweets():
    positive_tweets = []
    negative_tweets = []
    for filename in os.listdir('preprocessed'):
        file = open('bin/' + filename)
        for tweet in file:
            if tweet[:11] == '###!good###':
                positive_tweets.append(tweet[12:])
            elif tweet[:10] == '###!bad###':
                negative_tweets.append(tweet[11:])
        file.close()
        return positive_tweets, negative_tweets
        
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
    
def get_features(tokenized_tweets, sentiment):
    features = []
    for tweet in tokenized_tweets:
        tokens = {}
        for token in tweet:
            tokens[token] = True
        features.append((tokens, sentiment))
    return features
        
positive_tweets, negative_tweets = get_classified_tweets()

positive_features = get_features(tokenize_tweets(positive_tweets), "positive")
negative_features = get_features(tokenize_tweets(negative_tweets), "negative")

train_features, test_features = train_test_split(negative_features + positive_features, test_size=0.25, random_state=40)

print 'train on %d instances, test on %d instances' % (len(train_features), len(test_features))

classifier = NaiveBayesClassifier.train(train_features)

print 'accuracy:', nltk.classify.accuracy(classifier, test_features)
classifier.show_most_informative_features()
#print classifier.classify(word_feats(nltk.word_tokenize("Benzema you fat shit, should be sold")))
