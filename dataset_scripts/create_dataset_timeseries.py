from utils import *
import pandas as pd
import datetime
import time
from math import exp

encounters_drop_list=["Unnamed: 2","# Encounters"]
patient_drop_list=['Patient Name','D/C Disp','Unnamed: 9','Discharge Day','Discharge Timestamp','Reason for Visit','Metrics', '# Encs', '# Encs.1', '# Encs.2','# Encs.3', '# Encs.4']
ICD_drop_list=['ICD-10 Diagnosis DESC','Patient Name','Patient ID']
medication_drop_list=['Unnamed: 1','Metrics']
ICD_file_list=['ICD10s_2018_2019.csv','ICD10s_2016_2018.csv','ICD10s_2013_2016.csv']

encounters_df=pd.read_csv("/labs/banerjeelab/Central_line/Data/Encounters.csv")
encounters_df=drop_columns(encounters_drop_list,encounters_df)
encounters_df=encounters_df.dropna()
patients_df=pd.read_csv("/labs/banerjeelab/Central_line/Data/Patient List.csv")
patients_df=drop_columns(patient_drop_list,patients_df)
patients_df=patients_df.dropna()
base_df=concatenate_dfs(encounters_df,patients_df,'Encounter','Encounter')

base_df['Date of Birth'] = pd.to_datetime(base_df['Date of Birth'], format="%m/%d/%Y")
base_df['Service Day']=pd.to_datetime(base_df['Service Day'], format="%m/%d/%Y")
base_df['Admit Timestamp']= pd.to_datetime(base_df['Admit Timestamp'],errors='coerce', format="%m/%d/%Y %H:%M:%S")
base_df['Age']=abs(base_df['Date of Birth']-base_df['Admit Timestamp'])
base_df['Age']=round(base_df['Age'].dt.days / 365,1)
base_df['EMPI']=base_df['EMPI'].astype(int)
base_df['EMPI']=base_df['EMPI'].astype(str)
base_df=drop_columns(['Date of Birth'],base_df)
base_df=base_df.rename(columns={'Service Day':'Procedure_time','Patient ID':'Patient'})

ICD_df=pd.DataFrame()
for i in ICD_file_list:
    df=pd.read_csv("/labs/banerjeelab/Central_line/New_data/"+i)
    df=preprocess_dropChars(-3,'ICD-10 Diagnosis Code',df)
    df=df.rename(columns={'ICD-10 Diagnosis Code':'ICD_code','Patient EMPI Nbr':'EMPI'})
    ICD=ICD_mapping('ICD_code',df)
    ICD['Service Day']=pd.to_datetime(ICD['Service Day'], format="%m/%d/%Y")
    ICD=drop_columns(ICD_drop_list,ICD)
    ICD_df=ICD_df.append(ICD)
ICD_df['EMPI']=ICD_df['EMPI'].astype(str)
ICD_df=ICD_df.dropna()
ICD_df['ICD_group']=ICD_df['ICD_group'].astype(int)

op2 = pd.DataFrame()
days_lag=365
for index,row in base_df[:2].iterrows():
    gap=datetime.timedelta(days=days_lag)
    temp_row=(row.to_dict())
    start_date=row['Procedure_time']-datetime.timedelta(days=2)#row['Admit Timestamp']
    end_date=row['Procedure_time']
    EMPI_val=row['EMPI']
    df=ICD_df[ICD_df['EMPI']==EMPI_val].copy()
    if df.empty==False:
        while end_date-start_date>=datetime.timedelta(days=1):
            df1=df[(df['Service Day']<=start_date)&(df['Service Day']>=start_date-gap)].copy()
            date_list = [(start_date-gap) + datetime.timedelta(days=x) for x in range(days_lag+1)]
            date_list = pd.to_datetime(date_list,format="%m/%d/%Y")
            for i in range(1,23): 
                df2=df1[df1['ICD_group']==i].copy()
                #if(df2.empty==False):
                    #print(df2['Service Day'])
                for f in range(len(date_list)):
                    if(df2.empty==False):
                        if(date_list[f] in df2['Service Day'].values):
                            #print('Here','I'+str(i)+'_'+str(f))
                            temp_row['I'+str(i)+'_'+str(f)]=1
                        else:
                            temp_row['I'+str(i)+'_'+str(f)]=0
                    else:
                            temp_row['I'+str(i)+'_'+str(f)]=0
                df2=df2[0:0].copy()
            if(end_date-start_date==datetime.timedelta(days=1)):
                temp_row['Y']=1
            else:
                temp_row['Y']=0
            op2=op2.append(temp_row,ignore_index=True)
            start_date=start_date+datetime.timedelta(days=1)
            df1=df1[0:0].copy()
    df=df[0:0].copy()

op2.to_csv("/labs/banerjeelab/Central_line/Data/timeseries_dataset_basic.csv")