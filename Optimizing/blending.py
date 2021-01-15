import glob
import pandas as pd
import numpy as np

from sklearn import metrics

if __name__=='__main__':
    #files=glob.glob('cleaned_models_pred/*.csv')
    #df=None
    #for f in files:
        #if df is None:
            #df=pd.read_csv(f)
        #else:
            #temp_df=pd.read_csv(f)
            #df=df.merge(temp_df,on='id',how='left')

    #print(df.head())
    df=pd.read_csv('cleaned_models_pred/combined.csv')
    targets=df.sentiment_x.values

    pred_cols=['lr_cnt_pred','rf_svd_pred','lr_pred','MNB_pred'] 

    for col in pred_cols:
        auc=metrics.roc_auc_score(targets,df[col].values.reshape(-1,1))
        print(f'{col},overall_auc={auc}') 

    avg_pred=np.mean(df[['lr_cnt_pred','rf_svd_pred','lr_pred','MNB_pred']].values,axis=1).reshape(-1,1)
    print(avg_pred.shape)
    averaged_auc=metrics.roc_auc_score(targets,avg_pred)
    print(f'mean={averaged_auc}')    


    print('Something Else')
    lr_pred=df.lr_pred.values 
    lr_cnt_pred=df.lr_cnt_pred.values 
    rf_svd_pred=df.rf_svd_pred.values
    MNB_pred=df.MNB_pred.values

    
    print('Weighted Average')
    score=(0.21373736*lr_pred+ 0.09538379 *lr_cnt_pred-0.21543744*rf_svd_pred+0.17187048*MNB_pred).reshape(-1,1)
    print('weighted score={}'.format(metrics.roc_auc_score(targets,score)))
    
    #score=(1.67602099*lr_pred + 0.73691296 *lr_cnt_pred-1.54306287*rf_svd_pred+1.37374681*MNB_pred).reshape(-1,1)
    #print('weighted score={}'.format(metrics.roc_auc_score(targets,score)))

    print('Rank Averaging')
    lr_pred_rank=df.lr_pred.rank().values 
    lr_cnt_pred_rank=df.lr_cnt_pred.rank().values 
    rf_svd_pred_rank=df.rf_svd_pred.rank().values
    MNB_pred_rank=df.MNB_pred.rank().values
    avg_rank=((3*lr_pred_rank+1.5*lr_cnt_pred_rank+rf_svd_pred_rank+MNB_pred)/6.5).reshape(-1,1)
    print('Rank score={}'.format(metrics.roc_auc_score(targets,avg_rank)))

