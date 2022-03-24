from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import svm
import random
import json

class Sentiment:
    NEGATIVE = 'NEGATIVE'
    POSITIVE = 'POSITIVE'

class Review:
    def __init__(self, text, score):
        self.text = text
        self.score = score

    def get_sentiment(self):
        if self.score > 3: return Sentiment.POSITIVE
        else: return Sentiment.NEGATIVE

class ReviewContainer:
    def __init__(self, reviews):
        self.reviews = reviews

    def get_text(self):
        return [x.text for x in self.reviews]

    def get_sentiments(self):
        return [x.get_sentiment() for x in self.reviews]

    def evenly_distribute(self):
        negatives = list(filter(lambda x: x.get_sentiment() == Sentiment.NEGATIVE, self.reviews))
        positives = list(filter(lambda x: x.get_sentiment() == Sentiment.POSITIVE, self.reviews))
        positives = positives[:len(negatives)]
        self.reviews = negatives + positives
        random.shuffle(self.reviews)

# ========================================================== Load data
file_name = './data/reviews.json'
reviews = []
with open(file_name, errors='ignore') as f:
    reviews = json.load(f)

reviewsObjects = []
for review in reviews:
    reviewsObjects.append(Review(review['review'], float(review['rating'])))

# ========================================================== data prep
training, test = train_test_split(reviewsObjects, test_size=0.5)

training_cont = ReviewContainer(training)
test_cont = ReviewContainer(test)

training_cont.evenly_distribute()
test_cont.evenly_distribute()

X_train = training_cont.get_text()
y_train = training_cont.get_sentiments()

X_test = test_cont.get_text()
y_test = test_cont.get_sentiments()

# ========================================================== Bag of Words Vectorization
vectorizer = TfidfVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

# linear SVM
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(X_train_vectors, y_train)
svm_score = clf_svm.score(X_test_vectors, y_test)

# model tuning using GridSearch
parameters = {'kernel':('linear', 'rbf'), 'C': (1,4,8,16,32)}

svc = svm.SVC()
clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(X_train_vectors, y_train)
accuracy_score = clf.score(X_test_vectors, y_test)

# saving the model
import pickle
with open('./ML_models/sentiment_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)

# loading the model
with open('./ML_models/sentiment_classifier.pkl', 'rb') as f:
    loaded_clf = pickle.load(f)

def classify(text):
    text_vector = vectorizer.transform([text])
    return loaded_clf.predict(text_vector)