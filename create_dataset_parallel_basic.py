from utils import *
import pandas as pd
import datetime
import time
from math import exp
import multiprocessing as mp

def divide_and_conquer(df):
    n_workers=16
    N_ROWS = round(len(df)/n_workers+1) # number of rows in each dataframe
    with mp.Pool(n_workers) as pool: # use 3 processes
        # break up dataframe into smaller daraframes of N_ROWS rows each
        cnt = len(df.index)
        n, remainder = divmod(cnt, N_ROWS)
        results = []
        start_index = 0
        for i in range(n):
            results.append(pool.apply_async(process_frame,(df.loc[start_index:start_index+N_ROWS-1, :],)))
            start_index += N_ROWS
        if remainder:
            results.append(pool.apply_async(process_frame,(df.loc[start_index:start_index+remainder-1, :],)))
        #print(type(results),len(results))
        print('start get')
        new_dfs = [result.get() for result in results]
        print('end get')
        # reassemble final dataframe:
        df = pd.concat(new_dfs, ignore_index=True)
        return df

def process_frame(base_df):
    column_names=base_df.columns.tolist()+['I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14','I15','I16','I17','I18','I19','I20','I21','I22','Y']
    op2 = pd.DataFrame(columns = column_names)
    for index,row in base_df.iterrows():
        start=time.time()
        temp_row=(row.to_dict())
        start_date=row['Procedure_time']-datetime.timedelta(days=2)#row['Admit Timestamp']
        end_date=row['Procedure_time']
        EMPI_val=row['EMPI']
        df=ICD_df[ICD_df['EMPI']==EMPI_val].copy()
        if df.empty==False:
            while end_date-start_date>=datetime.timedelta(days=1):
                df1=df[df['Service Day']<=start_date].copy()
                df1['diff']=(start_date-df1['Service Day'])
                df1['diff']=df1['diff'].dt.days
                df1['weight']=np.exp(-np.power(df1['diff'],2))
                for i in range(1,23): 
                    df2=df1[df1['ICD_group']==i].copy()
                    temp_row['I'+str(i)]=df2['weight'].sum()
                    df2=df2[0:0].copy()
                if(end_date-start_date==datetime.timedelta(days=1)):
                    temp_row['Y']=1
                else:
                    temp_row['Y']=0
                op2=op2.append(temp_row,ignore_index=True)
                start_date=start_date+datetime.timedelta(days=1)
                df1=df1[0:0].copy()
        df=df[0:0].copy()
    return op2

if __name__ == '__main__':
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
    df=divide_and_conquer(base_df)   
    df.to_csv("/labs/banerjeelab/Central_line/Data/processed_parallel.csv")
    
