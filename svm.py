import numpy as np
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path


df_file = Path("data") / "label_data_5000.csv"

df = pd.read_csv(df_file)
# Feature columns
X = df.drop(['url', 'target'], axis=1)
y = df['target']

# split to training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

# Training using SVM linear
svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

# Making prediction
y_pred = svclassifier.predict(X_test)
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))





