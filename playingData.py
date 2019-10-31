import pandas as pd 
import numpy as np

from pathlib import Path
import seaborn as sns
from sklearn.preprocessing import LabelEncoder



DF_FILE = Path ('data') /"label_data_5000.csv"
empty_keys = ['name','placeholder','class','id','aria-label']

# df = pd.read_csv(DF_FILE, usecols=('name', 'placeholder', 'class','id','aria-label'))
df = pd.read_csv(DF_FILE)
# print(df)

# Check if attributes have empty value
df2 = df[df[empty_keys].isnull().all(axis=1)]
print (df2)

# Plot visualization
# iris.drop(['class'], axis=1).plot.line(title='Iris Dataset')
# sns.heatmap(df.isnull(), cbar=False)
