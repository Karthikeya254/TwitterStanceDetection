# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 20:17:58 2017

@author: Karthikeya
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Filenames as per tweet_postag.py
st_train = ["norm_trn_ath.csv", "norm_trn_cli.csv", "norm_trn_fem.csv", "norm_trn_hil.csv", "norm_trn_leg.csv"]
st_test = ["norm_tst_ath.csv", "norm_tst_cli.csv", "norm_tst_fem.csv", "norm_tst_hil.csv", "norm_tst_leg.csv"]
acc_st = []
for i in range(5):
    trn_f = st_train[i]
    tst_f = st_test[i]
    
    train = pd.read_csv(trn_f, engine='python')
    test = pd.read_csv(tst_f, engine='python')
    
    train_features = train.iloc[:-1,:-1]
    train_target = train.iloc[:-1,-1]
    
    test_features = test.iloc[:-1,:-1]
    test_target = test.iloc[:-1,-1]
    
    clf = RandomForestClassifier()
    clf = clf.fit(train_features, train_target)
    
    pred_target = clf.predict(test_features)
    acc_st.append(accuracy_score(test_target, pred_target))
    print(accuracy_score(test_target, pred_target))