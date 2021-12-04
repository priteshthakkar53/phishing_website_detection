import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def load_data():
	'''
	This is a function to load the data dataset saved in CSV file.
	This function returns 4 arrays - training set inputs
	(features) and results and the testing set inputs and results.
	'''
	#load the dataset from CSV file
	print("Loading dataset in csv file..")
	dataset_train1 = pd.read_csv("phishing_train.csv")
	dataset_train2 = pd.read_csv("legitimate_train.csv")
	
	#Extract the inputs (features), all columns except the Result coloumn
	#Here the columns to be extracted are written manually	
	X = dataset_train1[['Protocol', 'Length', '-', '@', 'Dots', 'In Domain Http',
       'Is IP Address', 'Harmful Host', 'Alexa Availability', 'Alexa Rank',
       'Whois Availability', 'Rank2traffic Availability',
       'Siterankdata Availability', 'Daily Unique Visitors']]
	X1 = dataset_train2[['Protocol', 'Length', '-', '@', 'Dots', 'In Domain Http',
       'Is IP Address', 'Harmful Host', 'Alexa Availability', 'Alexa Rank',
       'Whois Availability', 'Rank2traffic Availability',
       'Siterankdata Availability', 'Daily Unique Visitors']]
	X = X.append(X1)
	
    #Extract the output coloumn (Result column only)
	y = dataset_train1['Result']
	y1 = dataset_train2['Result']
	y = y.append(y1)

	#Separate training and testing data
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

	#Return the the four arrays
	return X_train, X_test, y_train, y_test

def train_logistic_regressing():
	print()
	print("***Training algorithm: Logistic Regression***")
	
	#Load the training dataset
	X_train, X_test, y_train, y_test = load_data()
	print("Training data loaded...")

	#Create a logistic regression classfier instance (scikit-learn)
	classifier = LogisticRegression()
	print("Classifier created...")

	#Train the classifier
	classifier.fit(X_train, y_train)
	print("Model training completed...")
	
	#Predict the test data using the trained classifier
	predictions = classifier.predict(X_test)
	print("Predictions of test data done...")

	#Calculate and print the accuracy (percentage of correct predictions)
	accuracy = 100.0 * accuracy_score(y_test, predictions)
	print("Logistic Regression accuracy : " + str(accuracy) + "%")

	return classifier

def train_decision_tree():
	print()
	print("***Training algorithm: Decision Tree***")
	
	#Load the training dataset
	X_train, X_test, y_train, y_test = load_data()
	print("Training data loaded...")

	#Create a decision tree classfier instance (scikit-learn)
	classifier = tree.DecisionTreeClassifier()
	print("Classifier created...")

	#Train the classifier
	classifier.fit(X_train, y_train)
	print("Model training completed...")
	
	#Predict the test data using the trained classifier
	predictions = classifier.predict(X_test)
	print("Predictions of test data done...")

	#Calculate and print the accuracy (percentage of correct predictions)
	accuracy = 100.0 * accuracy_score(y_test, predictions)
	print("Decision Tree accuracy : " + str(accuracy) + "%")

	return classifier


def train_random_forest():
	print()
	print("***Training algorithm: Random Forest***")
	
	#Load the training dataset
	X_train, X_test, y_train, y_test = load_data()
	print("Training data loaded...")

	#Create a decision tree classfier instance (scikit-learn)
	classifier = RandomForestClassifier()
	print("Classifier created...")

	#Train the classifier
	classifier.fit(X_train, y_train)
	print("Model training completed...")
	
	#Predict the test data using the trained classifier
	predictions = classifier.predict(X_test)
	print("Predictions of test data done...")

	#Calculate and print the accuracy (percentage of correct predictions)
	accuracy = 100.0 * accuracy_score(y_test, predictions)
	print("Random Forest accuracy : " + str(accuracy) + "%")

	return classifier


#train_logistic_regressing()
#print()
#train_decision_tree()


#rf = train_random_forest()