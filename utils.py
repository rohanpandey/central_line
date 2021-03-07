import pandas as pd 
import numpy as np

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