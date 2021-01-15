import pandas as pd 
import joblib
import numpy as np
import statistics
from text_cleaning import text_cleaner

def hard_voting(review):

    model1 = joblib.load('Models/lr.sav')
    vectorizer1 = joblib.load('Models/lr_vectorizer.sav')
    vec1 = vectorizer1.transform(review)
    predict1 = model1.predict(vec1).item()
    
    # Model 2
    model2 = joblib.load('Models/lr_cnt.sav')
    vectorizer2 = joblib.load('Models/lr_cnt_vectorizer.sav')
    vec2 = vectorizer2.transform(review)
    predict2 = model1.predict(vec2).item()
   

    # Model 3
    model3 = joblib.load('Models/rf.sav')
    vectorizer3 = joblib.load('Models/rf_vectorizer.sav')
    vec3 = vectorizer3.transform(review)
    predict3 = model1.predict(vec3).item()
   

    # Model 4
    model4 = joblib.load('Models/MNB.sav')
    vectorizer4 = joblib.load('Models/MNB_vectorizer.sav')
    vec4 = vectorizer4.transform(review)
    predict4 = model1.predict(vec4).item()

    predictions=[predict1,predict2,predict3,predict4]

    return statistics.mode(predictions)

def soft_voting(review):
    
    # Model 1
    model1 = joblib.load('Models/lr.sav')
    vectorizer1 = joblib.load('Models/lr_vectorizer.sav')
    vec1 = vectorizer1.transform(review)
    predict_proba01 = model1.predict_proba(vec1)[:,0].item()
    predict_proba11 = model1.predict_proba(vec1)[:,1].item()

    # Model 2
    model2 = joblib.load('Models/lr_cnt.sav')
    vectorizer2 = joblib.load('Models/lr_cnt_vectorizer.sav')
    vec2 = vectorizer2.transform(review)
   
    predict_proba02 = model1.predict_proba(vec2)[:,0].item()
    predict_proba12 = model1.predict_proba(vec2)[:,1].item()

    # Model 3
    model3 = joblib.load('Models/rf.sav')
    vectorizer3 = joblib.load('Models/rf_vectorizer.sav')
    vec3 = vectorizer3.transform(review)
    
    predict_proba03 = model1.predict_proba(vec3)[:,0].item()
    predict_proba13 = model1.predict_proba(vec3)[:,1].item()

    # Model 4
    model4 = joblib.load('Models/MNB.sav')
    vectorizer4 = joblib.load('Models/MNB_vectorizer.sav')
    vec4 = vectorizer4.transform(review)
    
    predict_proba04 = model1.predict_proba(vec4)[:,0].item()
    predict_proba14 = model1.predict_proba(vec4)[:,1].item()

    predict_proba0 = [predict_proba01,predict_proba02,predict_proba03,predict_proba04]
    predict_proba1 = [predict_proba11,predict_proba12,predict_proba13,predict_proba14]

    
    weight_coeff = [0.21373736,0.09538379,-0.21543744,0.17187048]
    predict_prob0 = np.dot(weight_coeff,predict_proba0)
    predict_prob1 = np.dot(weight_coeff,predict_proba1)

    if predict_prob0 > predict_prob1:
        return 0

    else:
        return 1    







if __name__ == '__main__':
    X="The movie was awesome with brilliant cinematography and an amazing soundtrack."
    y=text_cleaner(X)
    print(y)
    y=[y]
    
    hard_voting_result=hard_voting(y)
    print(hard_voting_result)


    soft_voting_result = soft_voting(y)
    print(soft_voting_result)