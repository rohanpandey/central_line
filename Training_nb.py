from utils import *
from models import *

df=pd.read_csv("/labs/banerjeelab/Central_line/Data/processed1.csv")

one_hot_list=['Gender','Race','Ethnic Group']
one_hot_prefix=['Gender','Race','Ethnic']
df=pd.get_dummies(df, columns=one_hot_list, prefix=one_hot_prefix)

drop_list=['Unnamed: 0', 'Encounter', 'CPT Procedure', 'Procedure_time', 'MRN','Patient', 'EMPI','Admit Timestamp']
df=drop_columns(drop_list,df)

X_train,X_test,Y_train,Y_test=split_data_standardize(df,0.25)

model=model_adaboost(X_train,Y_train)

values=predict_performance(model,X_test,Y_test)
print(values)