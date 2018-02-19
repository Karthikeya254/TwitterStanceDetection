# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 08:00:07 2017

@author: Karthikeya
"""

import csv
import re
#import nltk
from nltk.tag import StanfordPOSTagger
st = StanfordPOSTagger('english-bidirectional-distsim.tagger')

##########################################################################
#Pre processing
http_re = re.compile(r'\s+http://[^\s]*')
remove_ellipsis_re = re.compile(r'\.\.\.')
at_sign_re = re.compile(r'\@\S+')
punct_re = re.compile(r"[\"'\[\],.$<@>?:;()\-&!]")
slash_re = re.compile(r"[\"'\[\]\/\\]")
price_re = re.compile(r"\d+\.\d\d")
number_re = re.compile(r"\d+")

def normalize_tweet(tweet):
    t = tweet.lower()
    t = re.sub(price_re, '', t)
    t = re.sub(remove_ellipsis_re, '', t)
    t = re.sub(http_re, '', t)
    t = re.sub(punct_re, '', t)
    # t = re.sub(at_sign_re, '@', t)
    t = re.sub(number_re, '', t)
    t = re.sub(slash_re, ' ', t)
    return t
##########################################################################
import os

train_file = "train.csv"
test_file = "test.csv"
targets = ["Atheism", "Climate Change is a Real Concern", "Feminist Movement", "Hillary Clinton", "Legalization of Abortion"]
files_fw = ["fw_ath.csv", "fw_cli.csv", "fw_fem.csv", "fw_hil.csv", "fw_leg.csv"]
files_trn = ["trn_ath.csv", "trn_cli.csv", "trn_fem.csv", "trn_hil.csv", "trn_leg.csv"]
files_tst = ["tst_ath.csv", "tst_cli.csv", "tst_fem.csv", "tst_hil.csv", "tst_leg.csv"]

for i in range(5):
    train_tagged_tweets = []
    train_tweets = []
    train_labels = []
    test_tweets = []
    test_labels = []
    filtered_words = []
    train_feat = []
    test_feat = []
    target = targets[i]
    file_final_words = "norm_"+files_fw[i]
    file_train_feat = "norm_"+files_trn[i]
    file_test_feat = "norm_"+files_tst[i]
    print target
    filenames = [file_final_words, file_train_feat, file_test_feat]
    for fn in filenames:
        if os.path.exists(fn):
            os.remove(fn)
    # Nouns, Verbs, Adjectives as per Penn Treebank
    noun = ["NN", "NNS", "NNP"]
    verb = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    adjective = ["JJ", "JJR", "JJS"]
    
    # Tokenizing and POS tagging train tweets
    with open(train_file, 'rU') as csvfile:
        csvreader = csv.reader(csvfile)
        for l in csvreader:
            if l[1] == target:
                train_tweets.append(normalize_tweet(l[0]).split())
                train_labels.append(l[2])
                # POS taggers (using Stanford Tagger as default and commented out NLTK tagger)
                train_tagged_tweets.append(st.tag(normalize_tweet(l[0]).split()))
                # train_tagged_tweets.append(nltk.pos_tag(normalize_tweet(l[0]).split()))
    
    # Tokenizing test tweets
    with open(test_file, 'rU') as csvfile:
        csvreader = csv.reader(csvfile)
        for l in csvreader:
            if l[1] == target:
                test_tweets.append(normalize_tweet(l[0]).split())
                test_labels.append(l[2])
    
    # Filtering words based on their POS tags
    for tweet in train_tagged_tweets:
        for word_tag in tweet:
            # Use this line if you want to use bag of words with all POS tags
            # filtered_words.append(word_tag[0].encode('utf8', 'replace'))
            if(word_tag[1] in noun+verb+adjective):
                filtered_words.append(word_tag[0].encode('utf8', 'replace'))

    final_words = list(set(filtered_words))
    
    with open(file_final_words, "wb") as f:
        writer = csv.writer(f)
        writer.writerows([final_words])
    
    #Preparing Bag of Words feature set for training tweets
    for t, l in zip(train_tweets, train_labels):
        v = [0]*len(final_words)
        v.append(l)
        ids = [final_words.index(i) for i in t if i in final_words]
        for j in ids: v[j] = 1
        train_feat.append(v)
    
    with open(file_train_feat, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(train_feat)   
    
    
    #Preparing Bag of Words feature set for test tweets    
    for t, l in zip(test_tweets, test_labels):
        v = [0]*len(final_words)
        v.append(l)
        ids = [final_words.index(i) for i in t if i in final_words]
        for j in ids: v[j] = 1
        test_feat.append(v)
    
    with open(file_test_feat, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(test_feat)