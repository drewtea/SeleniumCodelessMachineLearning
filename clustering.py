from pathlib import Path
import numpy as np
import pandas as pd
from kmodes import kmodes

DF_FILE = Path ('data') /"df_1_1011.csv"
df = pd.read_csv(DF_FILE, usecols=('name', 'placeholder', 'class','id','aria-label'))

from sklearn.base import TransformerMixin

class DataFrameImputer(TransformerMixin):

    def __init__(self):
        """Impute missing values.

        Columns of dtype object are imputed with the most frequent value 
        in column.

        Columns of other types are imputed with mean of column.

        """
    def fit(self, X, y=None):

        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],
            index=X.columns)

        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

X = pd.DataFrame(df)
xt = DataFrameImputer().fit_transform(X)

print('before...')
print(X)
print('after...')
print(xt)
km = kmodes.KModes(n_clusters=5, init='Huang', n_init=6, verbose=1, ) 
clusters = km.fit_predict(xt)
kmodes = km.cluster_centroids_
shape = kmodes.shapes
for i in range(shape[0]):
    print("\ncluster " + str(i) + ": ")
    cent = kmodes[i,:]
    for j in xt.columns[np.nonzero(cent)]:
        print(j)




