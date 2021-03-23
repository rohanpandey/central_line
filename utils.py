import pandas as pd 
import numpy as np

encounters_drop_list=['CPT Procedure',"Unnamed: 2","# Encounters"]
patient_drop_list=['Patient Name','EMPI','D/C Disp','Unnamed: 9','Discharge Day','Discharge Timestamp','Reason for Visit','Metrics', '# Encs', '# Encs.1', '# Encs.2',
       '# Encs.3', '# Encs.4']

def preprocess_dropChars(number,column,dataframe):
    '''
    Funtion for dropping a specified number of characters from a given dataframe's column.
    
    Input:
      - number: number of chars to drop from right
      - column: column name to to be dropped
      - dataframe: dataframe from which the columns need to be dropped
    Output: 
      - Dataframe
    '''
    try:
      dataframe[column]=dataframe[column].apply(str).str.slice(0, -1*number)
      print(str(number),"Characters dropped")
      return dataframe
    except KeyError:
      print('Error: Invalid column name.')

def drop_columns(columns_list,dataframe):
    '''
    Function for dropping a list of columns from a specified dataframe.

    Input:
      - columns_list: List of all the columns to be dropped
      - dataframe_: dataframe from which the columns need to be dropped
    Output: 
      - Dataframe
    '''
    try:
      dataframe = dataframe.drop(columns_list,axis=1)
      print("Columns dropped")
      return dataframe
    except KeyError:
      print("Error: Invalid column name.")

def concatenate_dfs(dataframe1,dataframe2,left_on,right_on):
    '''
    Function for concatenating two dataframes on specified columns.

    Input:
      - dataframe1 and dataframe2 are the two dataframes to be concatenated
      - left_on and right_on are the respective column names to be used for concatenating
    Output:
      - Dataframe
    '''
    dataframe1[left_on]=dataframe1[left_on].apply(str)
    dataframe2[right_on]=dataframe2[right_on].apply(str)
    dataframe = pd.merge(dataframe1, dataframe2, left_on=left_on, right_on=right_on)
    print("Columns concatenated")
    return dataframe

def ICD_mapping(column,dataframe):
	ICD_group=[]
	G1=['A0{}'.format(i) for i in range(0,10)]+['A{}'.format(i) for i in range(10,100)]+['B0{}'.format(i) for i in range(0,10)]+['B{}'.format(i) for i in range(10,100)]
	G2=['C0{}'.format(i) for i in range(0,10)]+['C{}'.format(i) for i in range(10,100)]+['D0{}'.format(i) for i in range(0,10)]+['D{}'.format(i) for i in range(10,50)]+['C7A','C7B','D3A']
	G3=['D{}'.format(i) for i in range(50,90)]
	G4=['E0{}'.format(i) for i in range(0,10)]+['E{}'.format(i) for i in range(10,90)]
	G5=['F0{}'.format(i) for i in range(1,10)]+['F{}'.format(i) for i in range(10,100)]
	G6=['G0{}'.format(i) for i in range(0,10)]+['G{}'.format(i) for i in range(10,100)]
	G7=['H0{}'.format(i) for i in range(0,10)]+['H{}'.format(i) for i in range(10,60)]
	G8=['H{}'.format(i) for i in range(60,96)]
	G9=['I0{}'.format(i) for i in range(0,10)]+['I{}'.format(i) for i in range(10,100)]
	G10=['J0{}'.format(i) for i in range(0,10)]+['J{}'.format(i) for i in range(10,100)]
	G11=['K0{}'.format(i) for i in range(0,10)]+['K{}'.format(i) for i in range(10,96)]
	G12=['L0{}'.format(i) for i in range(0,10)]+['L{}'.format(i) for i in range(10,100)]
	G13=['M0{}'.format(i) for i in range(0,10)]+['M{}'.format(i) for i in range(10,100)]
	G14=['N0{}'.format(i) for i in range(0,10)]+['N{}'.format(i) for i in range(10,100)]
	G15=['O0{}'.format(i) for i in range(0,10)]+['O{}'.format(i) for i in range(10,100)]+['O9A']
	G16=['P0{}'.format(i) for i in range(0,10)]+['P{}'.format(i) for i in range(10,97)]
	G17=['Q0{}'.format(i) for i in range(0,10)]+['Q{}'.format(i) for i in range(10,100)]
	G18=['R0{}'.format(i) for i in range(0,10)]+['R{}'.format(i) for i in range(10,100)]
	G19=['S0{}'.format(i) for i in range(0,10)]+['S{}'.format(i) for i in range(10,100)]+['T0{}'.format(i) for i in range(0,10)]+['T{}'.format(i) for i in range(10,89)]
	G20=['U0{}'.format(i) for i in range(0,10)]+['U{}'.format(i) for i in range(10,86)]
	G21=['V0{}'.format(i) for i in range(0,10)]+['V{}'.format(i) for i in range(10,100)]+['W0{}'.format(i) for i in range(0,10)]+['W{}'.format(i) for i in range(10,100)]+['X0{}'.format(i) for i in range(0,10)]+['X{}'.format(i) for i in range(10,100)]+['Y0{}'.format(i) for i in range(0,10)]+['Y{}'.format(i) for i in range(10,100)]
	G22=['Z0{}'.format(i) for i in range(0,10)]+['Z{}'.format(i) for i in range(10,100)]
	for index,row in dataframe.iterrows():
	    if(row[column] in G1):
	        ICD_group.append(1)
	    if(row[column]in G2):
	    	ICD_group.append(2)
	    if(row[column] in G3):
	        ICD_group.append(3)
	    if(row[column] in G4):
	    	ICD_group.append(4)
	    if(row[column] in G5):
	        ICD_group.append(5)
	    if(row[column] in G6):
	    	ICD_group.append(6)
	    if(row[column] in G7):
	        ICD_group.append(7)
	    if(row[column] in G8):
	    	ICD_group.append(8)
	    if(row[column] in G9):
	        ICD_group.append(9)
	    if(row[column] in G10):
	    	ICD_group.append(10)
	    if(row[column] in G11):
	        ICD_group.append(11)
	    if(row[column] in G12):
	    	ICD_group.append(12)
	    if(row[column] in G13):
	        ICD_group.append(13)
	    if(row[column] in G14):
	    	ICD_group.append(14)
	    if(row[column] in G15):
	        ICD_group.append(15)
	    if(row[column] in G16):
	    	ICD_group.append(16)
	    if(row[column] in G17):
	        ICD_group.append(17)
	    if(row[column] in G18):
	    	ICD_group.append(18)
	    if(row[column] in G19):
	        ICD_group.append(19)
	    if(row[column] in G20):
	    	ICD_group.append(20)
	    if(row[column] in G21):
	        ICD_group.append(21)
	    if(row[column] in G22):
	    	ICD_group.append(22)
	df['ICD_group']=ICD_group

