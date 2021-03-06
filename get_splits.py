import pandas as pd
import numpy as np 
from sklearn import model_selection

if __name__=="__main__":
    df=pd.read_csv('cleaned.csv')
    df['sentiment']=df['sentiment'].astype('i8')
    df.loc[:,"kfold"]=-1
    df=df.sample(frac=1).reset_index(drop=True)

    y=df.sentiment.values
    skf=model_selection.StratifiedKFold(n_splits=5)


    for f, (t_, v_) in enumerate(skf.split(X=df,y=y)):
        df.loc[v_,"kfold"]=f

    df.to_csv('cleaned_folds.csv',index=False)    