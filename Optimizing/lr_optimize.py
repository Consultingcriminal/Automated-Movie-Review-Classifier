import pandas as pd
import numpy as np 
from sklearn import linear_model
from sklearn import model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from hyperopt import tpe, hp, fmin, STATUS_OK,Trials
from hyperopt.pyll.base import scope
from functools import partial

def optimize(params,x,y):
    model=linear_model.LogisticRegression(**params)
    kf=model_selection.StratifiedKFold(n_splits=5)
    roc_scores=[]
    for idx in kf.split(X=x,y=y):
        
        train_idx,test_idx=idx[0],idx[1]
        xtrain=x[train_idx]
        ytrain=y[train_idx]
        
        tf=TfidfVectorizer()
        tf.fit(xtrain)

        xtest=x[test_idx]
        ytest=y[test_idx]

        xtrain=tf.transform(xtrain)
        xtest=tf.transform(xtest)

        model.fit(xtrain,ytrain)
        preds=model.predict(xtest)
        fold_roc=metrics.roc_auc_score(ytest,preds)
        roc_scores.append(fold_roc)
    return -1.0 * np.mean(roc_scores)    



if __name__=='__main__':
    
    df=pd.read_csv('cleaned.csv')
    X=df['review'].values
    y=df['sentiment'].values

    param_space={
        "penalty":hp.choice("penalty",['l2','none']),
        "C":hp.uniform("C",0,1)
    }

    optimization_func=partial(optimize,x=X,y=y)
    trials=Trials()
    result=fmin(
        fn=optimization_func,
        space=param_space,
        algo=tpe.suggest,
        trials=trials,
        max_evals=15

    )

    print(result)




    