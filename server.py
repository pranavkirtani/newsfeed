
# pandas for data manipulation
import pandas as pd
pd.options.mode.chained_assignment = None
# nltk for nlp
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
# list of stopwords like articles, preposition
stop = set(stopwords.words('english'))
from string import punctuation
from collections import Counter
import re
import numpy as np
import os
trainFile=os.path.basename("news.csv")
data = pd.read_csv(trainFile, encoding = "ISO-8859-1")
data.head()
print('data shape:', data.shape)
data.category.value_counts().plot(kind='bar', grid=True, figsize=(16, 9))