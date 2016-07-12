
# coding: utf-8

# In[36]:

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import string
import re
import nltk
import enchant
import sklearn

get_ipython().magic(u'matplotlib inline')


# In[37]:

data = pd.read_csv('finaldata.csv')


# In[38]:

data.head()


# In[39]:

###############Randomizing sequence of data
data = data.iloc[np.random.permutation(len(data))]
data = data.reset_index(drop=True)


# In[ ]:

d = enchant.Dict("en_US")
def removenonsensewords(text):
    tokens = nltk.word_tokenize(text)
    
    stemmed = []
    #i=0
    for token in tokens:
        #print(i)
        #i=i+1
        if d.check(token):
            stemmed.append(token)
        
    return ' '.join(stemmed)

data['Text_Dictionary']= data['Text'].apply(removenonsensewords)


# In[ ]:

def listofbadwords():
    from nltk.corpus import stopwords
    stopwords = stopwords.words('english')
    monthnames = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    randomrepetitive = ['edu','unl','mt']
    
    totlist = stopwords + monthnames + randomrepetitive
    return totlist

totlist = listofbadwords()
def removebadwords(x):
    
    wordlist = x.split()
    wordlist = [word for word in wordlist if word.lower() not in totlist]
    x = ' '.join(wordlist)
    return x
data['Text'] = data['Text'].apply(removebadwords)


# In[ ]:

data[['Text','Text_Dictionary']].head()


# In[ ]:

data.to_csv('removedstopwords.csv',index=False)


# In[ ]:

data = pd.read_csv('removedstopwords.csv')


# In[ ]:

data = data.dropna()


# In[ ]:

from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(norm = None)
train_tfidf = vect.fit_transform(data['Text_Dictionary'])


# In[ ]:

train_tfidf.shape


# In[ ]:

ch2 = sklearn.feature_selection.SelectKBest(sklearn.feature_selection.chi2, k = 2500)
train_tfidf500 = ch2.fit_transform(train_tfidf, data['Category'])


# In[ ]:

train_tfidf500.toarray()


# In[ ]:

from sklearn.cross_validation import train_test_split
train_tfidf = train_tfidf500.toarray()
data_train,data_validate,labels_train,labels_validate = train_test_split(train_tfidf, data['Category'],test_size = 0.2)


# In[ ]:

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(data_train,labels_train)
sklearn.metrics.accuracy_score(model.predict(data_validate),labels_validate)


# In[ ]:

from bs4 import BeautifulSoup
import requests
import string
def removepunctuation(x):
    #x = x.replace('.',' ')
    #x = x.replace(')',' ')
    #x = x.replace('(',' ')
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    x = x.translate(replace_punctuation)
    #retstr = x.translate(string.maketrans("",""), string.punctuation)
    return x
    
def removeunicode(x):
    return re.sub(r'[^\x00-\x7F]+',' ', x)
def lowercasestring(x):
    return x.lower()

def removedigits(s):
    s = re.sub(" \d+", " ", s)
    return s
    
def cleanstring(x):
    #x=replaceredundancy(x)
    #x=removepunctuation(x)
    x=removeunicode(x)
    #x = trimstring(x)
    x=removedigits(x)
    x=lowercasestring(x)
    return x 

def getprediction(url):
    website = requests.get(url)
    soup = BeautifulSoup(website.content)
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    text = soup.getText()
    temp = re.sub(r'[\n\t\r ]+', " ", text)
    temp= re.sub(r'\s+'," ",temp)
    temp =  re.sub(r'\s+'," ",temp)
    
    temp = cleanstring(temp)
    
    lis = []
    lis.append(temp)
    #print(temp)
    feature_text = vect.transform(lis)
    feature_text = ch2.transform(feature_text)
    
    
    pred = model.predict(feature_text)
    print(feature_text.shape)
    
    return pred


# In[ ]:

getprediction("http://www.facebook.com")


# In[ ]:

getprediction("http://economictimes.indiatimes.com/news/economy/agriculture/indians-go-for-cheaper-pulses-as-tur-dal-prices-keep-rising/articleshow/53042439.cms")


# In[ ]:

import pickle
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
save_object(model,"model")
save_object(vect,"vect")
save_object(ch2,"ch2")

