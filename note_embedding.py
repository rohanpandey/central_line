import pandas as pd 
import numpy as np

def avg_weighting(dataframe,column):
	'''
	Function to average the specified column of vector in a dataframe
	
	Input:
      - dataframe
      - column
    Output: 
      - average value

	'''
  val=0
  for index,row in dataframe.iterrows():
    val+=row[column]
  val=val/len(dataframe.index)
  return val

def exp_weighting(dataframe,column,date_column,procedure_date,gap):
	'''
	Function to exponential weighted average of the specified column of vector in a dataframe
	
	Input:
      - dataframe
      - column
    Output: 
      - average value

	'''
	val=0
	for index,row in dataframe.iterrows():
		delta=procedure_date-row[date_column]-gap
		val+=exp(-(delta**2))*row[column]
	val=val/len(dataframe.index) 
	return val