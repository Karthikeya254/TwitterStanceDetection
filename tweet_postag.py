# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:00:07 2017

@author: karth
"""

import csv
import re
import nltk
from nltk.tag import StanfordPOSTagger
st = StanfordPOSTagger('english-bidirectional-distsim.tagger')

##########################################################################
#Pre processing
http_re = re.compile(r'\s+http://[^\s]*')
remove_ellipsis_re = re.compile(r'\.\.\.')
at_sign_re = re.compile(r'\@\S+')
punct_re = re.compile(r"[\"'\[\],.:;()\-&!]")
price_re = re.compile(r"\d+\.\d\d")
number_re = re.compile(r"\d+")

def normalize_tweet(tweet):
    t = tweet.lower()
    t = re.sub(price_re, 'PRICE', t)
    t = re.sub(remove_ellipsis_re, '', t)
    t = re.sub(http_re, ' LINK', t)
    t = re.sub(punct_re, '', t)
#    t = re.sub(at_sign_re, '@', t)
    t = re.sub(number_re, 'NUM', t)
    return t

##########################################################################

train_tagged_tweets = []
train_tweets = []
train_labels = []
test_tweets = []
test_labels = []
filtered_words = []
train_feat = []
test_feat = []

file_final_words = "final_words.csv"
file_train_feat = "train_feat.csv"
file_test_feat = "test_feat.csv"

import os
filenames = [file_final_words, file_train_feat, file_test_feat]
for fn in filenames:
    if os.path.exists(fn):
        os.remove(fn)

noun = ["NN", "NNS", "NNP"]
verb = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
adjective = ["JJ", "JJR", "JJS"]


with open('train.csv', 'rU') as csvfile:
    csvreader = csv.reader(csvfile)
    for l in csvreader:
        if l[1] == "Atheism":
            train_tweets.append(normalize_tweet(l[0]).split())
            train_labels.append(l[2])
            train_tagged_tweets.append(nltk.pos_tag(normalize_tweet(l[0]).split()))  


with open('test.csv', 'rU') as csvfile:
    csvreader = csv.reader(csvfile)
    for l in csvreader:
        if l[1] == "Atheism":
            test_tweets.append(normalize_tweet(l[0]).split())
            test_labels.append(l[2])
            

for tweet in train_tagged_tweets:
    for word_tag in tweet:
        if(word_tag[1] in noun+verb+adjective):
            filtered_words.append(word_tag[0])
            
final_words = list(set(filtered_words))

with open("final_words.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows([final_words])

#Preparing feature set for training tweets
for t, l in zip(train_tweets, train_labels):
    v = [0]*len(final_words)
    v.append(l)
    print len(v)
    print l
    ids = [final_words.index(i) for i in t if i in final_words]
    for j in ids: v[j] = 1
    train_feat.append(v)

with open("train_feat.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(train_feat)   


#Preparing feature set for test tweets    
for t, l in zip(test_tweets, test_labels):
    v = [0]*len(final_words)
    v.append(l)
    print len(v)
    print l
    ids = [final_words.index(i) for i in t if i in final_words]
    for j in ids: v[j] = 1
    test_feat.append(v)

with open("test_feat.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(test_feat)