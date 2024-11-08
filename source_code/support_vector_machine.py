# -*- coding: utf-8 -*-
"""Quiz2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f3FVgNRJoSXTlavORZN5pW8QnY5Qki7B
"""

import pandas as pd
import io
from google.colab import files
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import copy
from sklearn import datasets

"""# Upload Dataset"""

# Check if Churn_Modelling1.csv is already uploaded, if so, no need to run this cell
# skip to the next cell
uploaded = files.upload()

df = pd.read_csv('Churn_Modelling1.csv')

df

df.columns

print(df.shape)

print(df.dtypes)

df.describe()

columns_with_missing_values = df.columns[df.isnull().any()]
columns_with_missing_values

percent_missing = df.isnull().sum() * 100 / len(df)
percent_missing

"""# Data Cleaning"""

df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

df.columns

categorical_features = ['Geography', 'Gender']

df = pd.get_dummies(df, columns=categorical_features, drop_first=True)
df

"""# Train, Test, Split


"""

# Split into train/test:
train, test = train_test_split(df, test_size=0.2, random_state=22)

"""# Scale features"""

from sklearn.preprocessing import StandardScaler

scale= StandardScaler()

numerical_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'EstimatedSalary']

categorical_features_encoded = ['Geography_Germany', 'Geography_Spain', 'Gender_Male']

binary_features = ['HasCrCard', 'IsActiveMember']

all_features = numerical_features + categorical_features_encoded + binary_features
all_features

train[all_features]

train[all_features] = scale.fit_transform(train[all_features])

test[all_features] = scale.transform(test[all_features])

train

X = train.drop('Exited', axis=1)

X

y = train['Exited']

from sklearn.svm import SVC

svm_clf_svc= SVC(kernel='linear', C=1)

svm_clf_svc.fit(X, y)

X_test = test.drop('Exited', axis=1)

X_test

y_test = test['Exited']

y_test

y_test_predictions = svm_clf_svc.predict(X_test)

from sklearn import metrics

print("Accuracy:", metrics.accuracy_score(y_test, y_test_predictions))
print("Recall:", metrics.recall_score(y_test, y_test_predictions, average='weighted'))

"""# Visualize"""

test['y_test_pred'] = y_test_predictions
# Plot actual vs predicted
plt.figure(figsize=(10, 6))
plt.scatter(test.loc[test['Exited'] == test['y_test_pred'], 'Age'],
            test.loc[test['Exited'] == test['y_test_pred'], 'CreditScore'],
            color='green', label='Correctly Classified')
plt.scatter(test.loc[test['Exited'] != test['y_test_pred'], 'Age'],
            test.loc[test['Exited'] != test['y_test_pred'], 'CreditScore'],
            color='red', label='Misclassified')

plt.xlabel('Age')
plt.ylabel('CreditScore')
plt.title('SVM Predictions Visualization')
plt.legend()
plt.show()

"""# Polynomial Kernel

"""

poly_svm_clf = SVC(kernel='poly', degree=3, C=1)

poly_svm_clf.fit(X, y)

y_test_predictions_poly = poly_svm_clf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_test_predictions_poly))
print("Recall:", metrics.recall_score(y_test, y_test_predictions_poly, average='weighted'))