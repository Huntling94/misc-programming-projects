import pandas as pd
import numpy as np
import os.path
import time
import tabulate
import jellyfish
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import RidgeClassifier
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from collections import defaultdict
import random
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# The key will be the name of the learner showing up in analysis.
# The value is the learner we wish to use for cross-validation purposes
LEARNER_DICT = {'MultinomialNB': MultinomialNB,
                'LogisticRegression': LogisticRegression,
                'RandomForest': RandomForestClassifier,
                'SVM, kernel=linear': LinearSVC,
                'ADA Boost': AdaBoostClassifier,
                'Perceptron': Perceptron,
                'Multi-layer Perceptron': MLPClassifier,
                'Ridge Classifier': RidgeClassifier}

DELIMS = [",", "\t", ";"]

"""
Returns the X_train, y_train and X_test tables so they can be fed into sklearn functions

Arguments:
    train_fname: string, file name of the training set (last column should be the labels, second last column the descriptions)
    test_fname: string, file name of the testing seet (last column should be the descriptions)

Returns: 3 data frames: X_train (training set descriptions), y_train (training set classifications), X_test (testing set descriptions)
"""
def get_datasets(train_fname, test_fname):
    training_set = None
    testing_set = None
    for delimiter in DELIMS:
        training_set = pd.read_csv(train_fname, delimiter)
        if training_set.shape[1] > 1:
            break
    for delimiter in DELIMS:
        testing_set = pd.read_csv(test_fname, delimiter)
        if training_set.shape[1] > 1:
            break

    try:
        X_train, y_train = training_set.iloc[:, -2], training_set.iloc[:, -1]
        X_test = testing_set.iloc[:, -1]
    except IndexError:
        print(f"Ensure the training and testing files have at least 2 columns (check delimiters)."
                "The last column in the training file should be the Classifications (labels)."
                "The last column in the testing file should be the Description (text).", file=sys.stderr)
        sys.exit()

    return X_train, y_train, X_test

"""
Creates an sklearn pipeline

Arguments:
    estimator: sklearn learner: See LEARNER_DICT for compatible learners

Returns: A Pipeline
"""
def create_pipeline(estimator):
    steps = [
            ('vectorize', CountVectorizer())
            ]
    steps.append(('classifier', estimator))
    return Pipeline(steps)


"""
Performs 10-fold cross-validation on the training set across all learners, and analyzes the
relevant scores (eg accuracy) for each learner, returning with the instances being the
name of the learner (eg LogisticRegression), and the features being scoring metrics (eg accuracy)

Arguments:
    train_fname: string, file name of the training set (last column should be the labels, second last column the descriptions)
    test_fname: string, file name of the testing seet (last column should be the descriptions)
    verboose: boolean, True will print out the analysis, False will not

Returns: array of arrays containing how each learner performed based on various metrics
"""
def model_comparisons_crossvalidate(train_fname, test_fname, verbose=True):
    training_set = None
    delim = None
    for delimiter in DELIMS:
        training_set = pd.read_csv(train_fname, delimiter)
        if training_set.shape[1] > 1:
            delim = delimiter
            break

    try:
        X, y = np.array(training_set.iloc[:, -2]), np.array(training_set.iloc[:, -1])
    except IndexError:
        print(f"Ensure the training set has at least 2 columns (check delimiters)."
                "The last column should be the Classifications (labels).", file=sys.stderr)
        sys.exit()

    num_folds = 10
    kf = KFold(n_splits=num_folds, shuffle=True, random_state = random.randint(1,100000))

    # Models from the pipeline stored here
    models = []
    
    # Names of the learners
    learners = list(LEARNER_DICT.keys())
    best_learners = {}

    scores = {}
    for learner in learners:
        scores[learner] = defaultdict(list)


    curr = 1
    # Do the KFold cross-validation and output the scores for each fold into scores for each learner
    for train_index, test_index in kf.split(X):
        print(f"Analyzing fold {curr} of {num_folds}")
        curr += 1
        # Training set split here
        X_train, y_train, X_test, y_test = X[train_index], y[train_index], X[test_index], y[test_index]
        models = []

        # Add learners
        for learner in learners:
            models.append(create_pipeline(LEARNER_DICT[learner]()))

        # Fit model to data and score
        for i, model in enumerate(models):
            start = time.process_time()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            score = accuracy_score(y_test, y_pred)
            
            scores[learners[i]]['accuracy'].append(accuracy_score(y_test, y_pred))
            # Since our labels are not binary, the average parameter can be changed, and is set to weighted.
            # Weighted calculates the metric for each label and finds the average weighted by instances involved in weighting score (ie accounts for label imbalance)
            # If there are no predicted samples or true samples for a particular label, score set to 0, warnings suppressed.
            scores[learners[i]]['precision'].append(precision_score(y_test, y_pred, average="weighted", zero_division=0))
            scores[learners[i]]['recall'].append(recall_score(y_test, y_pred, average="weighted", zero_division=0))
            scores[learners[i]]['seconds to train'].append(time.process_time()-start)

    # Analyze and tabulate the data from scores
    fields = ['model', 'accuracy', 'precision', 'recall', 'seconds to train']
    table = []
    for learner in learners:
        row = [learner]
        for field in fields[1:]:
            row.append(np.mean(scores[learner][field]))
        table.append(row)
    table.sort(key=lambda x: x[1], reverse=True)
    if verbose == True:
        print(tabulate.tabulate(table, headers=fields))
    return table

"""
Trains the relevant learners with the training set and then predicts the labels for the testing set and
outputs the classification to a new text file.

Arguments:
    train_fname: string, file name of the training set (last column should be the labels, second last column the descriptions)
    test_fname: string, file name of the testing set (last column should be the descriptions)

Returns: void
"""
def classify(train_fname, test_fname):
    # Training set does not have class labels: we want to predict these
    X_train, y_train, X_test = get_datasets(train_fname, test_fname)

    df = pd.DataFrame(model_comparisons_crossvalidate(train_fname, test_fname, verbose=False))

    # Model used is the model with the highest accuracy deteremined after cross validation
    model = create_pipeline(LEARNER_DICT[df.iloc[0][0]]()) # If you want to use a specific learner, replace the input with  a particupar learner, eg MultinomialNB()

    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    
    write_fname = test_fname[:-4] + "predicted" + ".txt"
    if os.path.isfile(write_fname) is True:
        for i in range(100):
            write_fname = test_fname[:-4] + "predicted" + str(random.randint(1, 1000000)) + test_fname[-4:]
            if os.path.isfile(write_fname) is False:
                break
    if os.path.isfile(write_fname) is True:
        print("Could not find a safe new file to write the data to; try renaming your testing set file name")
        sys.exit()

    fp = open(write_fname, "w")

    dump_result = pd.read_csv(test_fname)

    for col in dump_result.columns:
        print(f"{col}\t", file=fp, end="")
    print(f"Predicted Category {df.iloc[0][0]}", file=fp)
    for i, row in enumerate(dump_result.itertuples(index=False)):
        for j in range(0, len(row)):
            print(f"{row[j]}\t", file=fp, end="")
        print(y_pred[i], file=fp)
    
    fp.close()

    print(f"{dump_result.shape[0]} line items classified with the algorithm: {df.iloc[0][0]}, outputted to: {write_fname}")

"""
Tests whether user provided file names are valid (they should exist in the current directory), and exits program if they are not.

Arguments:
    fname: file name, which should be either the training set or testing set
Returns: void
"""
def test_valid_filename(fname):
    if((len(fname) < 5)):
        print(f"{fname} is not a valid file name.")
        sys.exit()
    if(fname[-4:] not in [".csv", ".txt", ".tsv"]):
        print("Only csv, tsv and txt file extensions are recognised.")
        sys.exit()
    if os.path.isfile(fname) is False:
        print(f"{fname} is not a valid file in your current directory.")
        sys.exit()

def main():
    ### Process files
    if((len(sys.argv) >= 3)):
        train_fname = sys.argv[1]
        test_valid_filename(train_fname)
        test_fname = sys.argv[2]
        test_valid_filename(test_fname)
    else:
        print("Note that for the training set, the last column should contain the class labels, "
              "and the second last column should contain the description. "
              "For the testing set, the last column should only contain the description which is used to predict the class label.")
        train_fname = input("Please enter the filename of the training set: ")
        test_valid_filename(train_fname)
        
        test_fname = input("Please enter the filename of the testing set: ")
        test_valid_filename(test_fname)

    
    # Accepted responses
    cross_validate_responses = ["c", "cv", "cross-validate", "cross validate", 'test']
    classify_responses = ['p', 'classify', 'predict', 'classify and predict', 'predict and classify']
    both_responses = ['b', 'both']

    matching_responses = [cross_validate_responses, classify_responses, both_responses]
    response_similarity ={}

    ### Process responses and act depending on user input
    while True:
        mode = input("Would you like to cross-validate the training set against different learners (type c), or would you like to predict and classify the test set (type p), or both (type b)?: ")
        for i, matching_categories in enumerate(matching_responses):
            for response in matching_categories:
                response_similarity[response] = jellyfish.levenshtein_distance(mode, response)


        distances = [(k, response_similarity[k]) for k in response_similarity]
        distances.sort(key=lambda x: x[1])

        # Exact match for 1 letter suggestions
        if len(mode) == 1 and distances[0][1] == 0:
            if mode == cross_validate_responses[0]:
                model_comparisons_crossvalidate(train_fname, test_fname)
            elif mode == classify_responses[0]:
                classify(train_fname, test_fname)
            else:
                model_comparisons_crossvalidate(train_fname, test_fname)
                classify(train_fname, test_fname)

        # Approximate match to accepted responses
        elif len(mode) > 4 and distances[0][1] < 3:
            print(f"You entered {mode}. ", end="")
            if distances[0][0] in cross_validate_responses:
                print("We assumed you want to cross-validate.")
                model_comparisons_crossvalidate(train_fname, test_fname)
            elif distances[0][0] in classify_responses:
                print("We assumed you wanted to predict and classify the test set.")
                classify(train_fname, test_fname)
            elif distances[0][0] in both_responses:
                print("We assumed you wanted to cross-validate and predict and classify the test set.")
                model_comparisons_crossvalidate(train_fname, test_fname)
                classify(train_fname, test_fname)

        # No approximate match
        else:
            print(f"You entered {mode}. We do not know what you want, please try again.\n")
            continue
        break




if __name__ == "__main__":
    main()