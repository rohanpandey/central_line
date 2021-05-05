import pandas as pd 
import numpy as np
import os
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors

def embed_column_avg(dataframe,column,model_name,dimensions,tokens):
	'''
	Function to apply embedding to the specified column of a dataframe using the specified model
	Input:
      - dataframe
      - column
      - model_name ='glove' or 'biovec'
      - dimensions
      - tokens
    Output: 
      - dataframe with embedding column added

	'''
  if(model_name='glove'):
  	model=load_glove(tokens,dimensions)
  if(model_name='biovec'):
  	model=load_biovec(dimensions)
  value_array=[]
  for index,row in dataframe.iterrows():
    note_as_vec=[]
    preprocessed_text=apply_all(dataframe[column])
    for word in preprocessed_text:
      try:
        vec_word = model[word]
      except:
        vec_word = [0.0]*dimensions
      note_as_vec.append(vec_word)
    value=np.average(note_as_vec, axis=0)
    value_array.append(value)
  dataframe[column+'_avg']=value_array
  return dataframe

def load_biovec(dimensions):
	 '''
    Funtion for loading specified biovec model.
    
    Input:
      - dimensions: number of dimensions of the biovec model
    Output: 
      - loaded model
    '''
	file_path="/BioWordVec_d{}.vec.bin".format(dimensions)
	biovecpath = os.path.expanduser(file_path)
	biovec = gensim.models.KeyedVectors.load_word2vec_format(biovecpath, binary=True)
	return biovec

def load_glove(tokens,dimensions):
	'''
    Funtion for loading specified glove model.
    
    Input:
      - dimensions: number of dimensions of the glove model
      - tokens: number of tokens of the glove model 
    Output: 
      - loaded model
    '''
  file_path="/glove.{}B.{}d.txt".format(tokens,dimensions)
  glovepath = os.path.expanduser(file_path)
  temp_file = "/tmp/glove.840B.300d.w2v.txt"
  glove2word2vec(glovepath, temp_file)
  glove = KeyedVectors.load_word2vec_format(temp_file)
  return glove