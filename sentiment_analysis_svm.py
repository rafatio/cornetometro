from numpy.random import randint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import metrics

preprocessed_dataset_path = 'preprocessed/dataset.txt'
POSITIVE = 'positive'
NEGATIVE = 'negative'

# Returns the list of tweets in the dataset and a list of their respective classes
def get_dataset():
    tweets = []
    classes = []

    dataset = open(preprocessed_dataset_path)

    for line in dataset:
        if line[:11] == '###!good###':
            classes.append(POSITIVE)
            tweets.append(line[12:])
        elif line[:10] == '###!bad###':
            classes.append(NEGATIVE)
            tweets.append(line[11:])
    dataset.close()

    return tweets, classes

def extract_test_data(data, classes, test_ratio):
    test_data = []
    test_classes = []

    test_size = int( len(data) * test_ratio )
    for i in xrange(test_size):
        id = randint(len(data))
        test_data.append(data.pop(id))
        test_classes.append(classes.pop(id))

    return test_data, test_classes

def test_classifier(data, classes):
    accuracy_total = 0.0
    pos_precision_total = 0.0
    pos_recall_total = 0.0
    pos_f_measure_total = 0.0
    neg_precision_total = 0.0
    neg_recall_total = 0.0
    neg_f_measure_total = 0.0
    
    repeat = 10
    for i in xrange(repeat):
        training_data = list(data)
        training_classes = list(classes)
        test_data, test_classes = extract_test_data(training_data, training_classes, 0.25)
    
        vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True)
        training_vectors = vectorizer.fit_transform(training_data)
        test_vectors = vectorizer.transform(test_data)
    
        classifier = svm.LinearSVC()
        classifier.fit(training_vectors, training_classes)
        prediction = classifier.predict(test_vectors)
    
        accuracy_total += metrics.accuracy_score(test_classes, prediction)
        pos_precision_total += metrics.precision_score(test_classes, prediction, average='binary', pos_label=POSITIVE)
        pos_recall_total += metrics.recall_score(test_classes, prediction, average='binary', pos_label=POSITIVE)
        pos_f_measure_total += metrics.f1_score(test_classes, prediction, average='binary', pos_label=POSITIVE)
        neg_precision_total += metrics.precision_score(test_classes, prediction, average='binary', pos_label=NEGATIVE)
        neg_recall_total += metrics.recall_score(test_classes, prediction, average='binary', pos_label=NEGATIVE)
        neg_f_measure_total += metrics.f1_score(test_classes, prediction, average='binary', pos_label=NEGATIVE)
    
    accuracy = accuracy_total / repeat
    pos_precision = pos_precision_total / repeat
    pos_recall = pos_recall_total / repeat
    pos_f_measure = pos_f_measure_total / repeat
    neg_precision = neg_precision_total / repeat
    neg_recall = neg_recall_total / repeat
    neg_f_measure = neg_f_measure_total / repeat
    
    print 'accuracy:', accuracy
    print 'pos_precision:', pos_precision
    print 'pos_recall:', pos_recall
    print 'pos_f_measure:', pos_f_measure
    print 'neg_precision:', neg_precision
    print 'neg_recall:', neg_recall
    print 'neg_f_measure:', neg_f_measure

data, classes = get_dataset()
test_classifier(data, classes)

