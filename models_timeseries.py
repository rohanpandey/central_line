from keras.layers import Layer
import keras.backend as K
from keras.layers import Input, LSTM, concatenate, Dense, Lambda, Flatten,Dropout, BatchNormalization
from keras.models import Model


class attention(Layer):
    def __init__(self,**kwargs):
        super(attention,self).__init__(**kwargs)

    def build(self,input_shape):
        self.W=self.add_weight(name="att_weight",shape=(input_shape[-1],1),initializer="normal")
        self.b=self.add_weight(name="att_bias",shape=(input_shape[1],1),initializer="zeros")        
        super(attention, self).build(input_shape)

    def call(self,x):
        et=K.squeeze(K.tanh(K.dot(x,self.W)+self.b),axis=-1)
        at=K.softmax(et)
        at=K.expand_dims(at,axis=-1)
        output=x*at
        return output
        #return K.sum(output,axis=1)

    def compute_output_shape(self,input_shape):
        return (input_shape[0],input_shape[-1])

    def get_config(self):
        return super(attention,self).get_config()


def LSTM_model_simple(features,demo_features,dimension,output_classes,no_of_groups,dense,BN,attn,dropout_lstm,dropout_dense):
  input_list={}
  lstm_list={}
  input_demo=Input(shape=(demo_features,1),name="input_demographics")
  for i in range(1,no_of_groups+1):
    input_list['input_{0}'.format(i)]=Input(shape=(features, dimension), name='input_'+str(i))
    lstm_list['lstm{0}'.format(i)]=LSTM(1, name='lstm'+str(i),return_sequences=True,dropout=dropout_lstm, recurrent_dropout=dropout_lstm)(input_list['input_'+str(i)])
    if attn==True:
      lstm_list['lstm{0}'.format(i)]=attention()(lstm_list['lstm{0}'.format(i)])
  concat=concatenate(list(lstm_list.values())+[input_demo],axis=1)
  concat=Flatten()(concat)
  dropout_layer=Dropout(dropout_dense)(concat)
  if(dense==True):
    dropout_layer=Dense(int(dropout_layer.shape[1]/2))(dropout_layer)
    dropout_layer=Dropout(dropout_dense)(dropout_layer) 
  if(BN==True):
    dropout_layer = BatchNormalization()(dropout_layer)
  output = Dense(output_classes)(dropout_layer)
  model = Model(inputs=[input_demo]+list(input_list.values()), outputs=output)
  return model

def LSTM_model_combined(features,demo_features,dimension,output_classes,no_of_groups,dense,BN,attn,dropout_lstm,dropout_dense):
  input_list={}
  lstm_list={}
  flatten_list={}
  dense_list={}
  input_demo=Input(shape=(demo_features,1),name="input_demographics")
  for i in range(1,no_of_groups+1):
    input_list['input_{0}'.format(i)]=Input(shape=(features, dimension), name='input_'+str(i))
    lstm_list['lstm{0}'.format(i)]=LSTM(1, name='lstm'+str(i),return_sequences=True,dropout=dropout_lstm, recurrent_dropout=dropout_lstm)(input_list['input_'+str(i)])
  concat=concatenate(list(lstm_list.values()))
  for i in range(concat.shape[1]):
    #flatten_list['flatten{0}'.format(i)]=Flatten()(concat[:,i:i+1,:])
    dense_list['dense{0}'.format(i)]=Dense(1,activation='relu')(concat[:,i:i+1,:])#['lstm{0}'.format(i)])
  concat2=concatenate(list(dense_list.values()),axis=1)
  if attn==True:
      concat2=attention()(concat2)
  concat2=concatenate([concat2]+[input_demo],axis=1)
  concat2=Flatten()(concat2)
  dropout_layer=Dropout(dropout_dense)(concat2)
  if(dense==True):
    dropout_layer=Dense(int(dropout_layer.shape[1]/2))(dropout_layer)
    dropout_layer=Dropout(dropout_dense)(dropout_layer) 
  if(BN==True):
    dropout_layer = BatchNormalization()(dropout_layer)
  output = Dense(output_classes)(dropout_layer)
  model = Model(inputs=[input_demo]+list(input_list.values()), outputs=output)
  return model