from numpy.random import randint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

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
    training_data = list(data)
    training_classes = list(classes)
    test_data, test_classes = extract_test_data(training_data, training_classes, 0.25)

    vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True)
    training_vectors = vectorizer.fit_transform(training_data)
    test_vectors = vectorizer.transform(test_data)

    classifier = svm.SVC()
    classifier.fit(training_vectors, training_classes)
    prediction = classifier.predict(test_vectors)

    correct = 0
    for i in xrange(len(prediction)):
        if prediction[i] == test_classes[i]:
            correct += 1

    print 'accuracy:', (float(correct) / len(prediction))

data, classes = get_dataset()
test_classifier(data, classes)
