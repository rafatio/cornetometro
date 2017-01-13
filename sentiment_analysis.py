import os
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
from numpy.random import randint
import collections
from nltk.stem.porter import PorterStemmer



def word_feats(words):
    return dict([(word, True) for word in words])

def get_classified_tweets():
    positive_tweets = []
    negative_tweets = []
    for filename in os.listdir('preprocessed'):
        file = open('preprocessed/' + filename)
        for tweet in file:
            if tweet[:11] == '###!good###':
                positive_tweets.append(tweet[12:])
            elif tweet[:10] == '###!bad###':
                negative_tweets.append(tweet[11:])
        file.close()
        return positive_tweets, negative_tweets

def tokenize_tweets(tweets):
    tokenized_tweets = []
    stemmer = PorterStemmer()
    for tweet in tweets:
        tokenized_tweet = []
        words = nltk.word_tokenize(tweet)
        for word in words:
            if word not in stopwords.words('english'):
                stemmed_word = stemmer.stem(word)
                tokenized_tweet.append(stemmed_word)
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

def best_word_feats(tweets, sentiment):
    best_words = []
    for tweet in tweets:
        tokens = {}
        for word in tweet:
            if word in bestwords:
                tokens[word] = True
        best_words.append((tokens, sentiment))
    return best_words

def best_bigram_word_feats(tweets, sentiment, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigramx = []
    for tweet in tweets:
        tokens = {}
        bigram_finder = BigramCollocationFinder.from_words(tweet)
        bigrams = bigram_finder.nbest(score_fn, n)
        for bigram in bigrams:
            tokens[bigram] = True
        tokens.update(dict([(word, True) for word in tweet if word in bestwords]))
        bigramx.append((tokens,sentiment))
    return bigramx

def classifier(method):
    positive_features = method(tokenize_tweets(positive_tweets), "positive")
    negative_features = method(tokenize_tweets(negative_tweets), "negative")

    acc = 0.0
    repeat = 10
    pos_precision = 0.0
    pos_recall = 0.0
    neg_precision = 0.0
    neg_recall = 0.0
    pos_f_measure = 0.0
    neg_f_measure = 0.0

    for x in xrange(repeat):
        train_features, test_features = train_test_split(negative_features + positive_features, test_size=0.25, random_state=seed_random)

        print 'train on %d instances, test on %d instances' % (len(train_features), len(test_features))

        classifier = NaiveBayesClassifier.train(train_features)
        ref_sets = collections.defaultdict(set)
        test_sets = collections.defaultdict(set)

        for i, (feats, label) in enumerate(test_features):
            ref_sets[label].add(i)
            observed = classifier.classify(feats)
            test_sets[observed].add(i)

        acc += nltk.classify.accuracy(classifier, test_features)
        pos_precision += nltk.precision(ref_sets['positive'], test_sets['positive'])
        pos_recall += nltk.recall(ref_sets['positive'], test_sets['positive'])
        pos_f_measure += nltk.f_measure(ref_sets['positive'], test_sets['positive'])

        neg_precision += nltk.precision(ref_sets['negative'], test_sets['negative'])
        neg_recall += nltk.recall(ref_sets['negative'], test_sets['negative'])
        neg_f_measure += nltk.f_measure(ref_sets['negative'], test_sets['negative'])

    print 'accuracy:', str(acc / repeat)
    print 'pos_precision', str(pos_precision / repeat)
    print 'pos_recall', str(pos_recall / repeat)
    print 'pos_f_measure', str(pos_f_measure / repeat)

    print 'neg_precision', str(neg_precision / repeat)
    print 'neg_recall', str(neg_recall / repeat)
    print 'neg_f_measure', str(neg_f_measure / repeat)


positive_tweets, negative_tweets = get_classified_tweets()

word_fd = FreqDist()
label_word_fd = ConditionalFreqDist()

for tweet in tokenize_tweets(positive_tweets):
    for word in tweet:
        word_fd[word.lower()] +=1
        label_word_fd['pos'][word.lower()] +=1

for tweet in tokenize_tweets(positive_tweets):
    for word in tweet:
        word_fd[word.lower()] +=1
        label_word_fd['neg'][word.lower()] +=1

pos_word_count = label_word_fd['pos'].N()
neg_word_count = label_word_fd['neg'].N()
total_word_count = pos_word_count + neg_word_count

word_scores = {}

for word, freq in word_fd.iteritems():
    pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
        (freq, pos_word_count), total_word_count)
    neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
        (freq, neg_word_count), total_word_count)
    word_scores[word] = pos_score + neg_score

best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:500]
bestwords = set([w for w, s in best])

seed_random = randint(100)

print 'evaluating single word features'
classifier(get_features)

print 'best words'
classifier(best_word_feats)

print 'evaluating best words + bigram chi_sq word features'
classifier(best_bigram_word_feats)
