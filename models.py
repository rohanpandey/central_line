from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.models import Sequential
from keras.layers import Dense
import xgboost as xgb
import numpy as np
from models_timeseries import *

def model_LSTM1(X_train,Y_train,epochs,bs,features,demo_features,dimension,output_classes,no_of_groups,dense,BN,attn,dropout_lstm,dropout_dense):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=5, min_lr=1e-9)
    model=LSTM_model_simple(features,demo_features,dimension,output_classes,no_of_groups,dense,BN,attn,dropout_lstm,dropout_dense)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    #Set the inputs 
    model.fit(X_train, Y_train, epochs=epochs, batch_size=bs,callbacks=[early_stopping,reduce_lr])
    return model
    
def model_LSTM2(X_train,Y_train,epochs,bs,features,demo_features,dimension,output_classes,no_of_groups,dense,BN,attn,dropout_lstm,dropout_dense):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=5, min_lr=1e-9)
    model=LSTM_model_combined(features,demo_features,dimension,output_classes,no_of_groups,dense,BN,attn,dropout_lstm,dropout_dense)
    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(X_train, Y_train, epochs=epochs, batch_size=bs,callbacks=[early_stopping,reduce_lr])
    return model

def model_NN(X_train, Y_train,epochs,bs):
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2,patience=5, min_lr=1e-9)
    early_stopping = EarlyStopping(monitor='loss', patience=10)
    model = Sequential()
    model.add(Dense(50, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=epochs, batch_size=bs,callbacks=[early_stopping,reduce_lr])
    return model

def model_XGB(X_train, Y_train):
    xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=5)
    xgb_model.fit(X_train, Y_train)
    return xgb_model

def model_GB(X_train,Y_train):
    gbk = GradientBoostingClassifier()
    gbk.fit(X_train, Y_train)
    return gbk

def model_DT(X_train,Y_train):
    classifier=DecisionTreeClassifier(criterion="entropy",random_state=5)
    classifier.fit(X_train, Y_train)
    return classifier

def model_NB(X_train,Y_train,category):
    if(category=='g'):
        classifier=GaussianNB()
    if(category=='b'):
        classifier=BernoulliNB()
    classifier.fit(X_train, Y_train)
    return classifier

def model_LR(X_train,Y_train,iterations):
    model = LogisticRegression(max_iter = iterations)
    model.fit(X_train, Y_train)
    return model
    
def model_SVC(X_train,Y_train,kernel_type):
    classifier = SVC(kernel = kernel_type, random_state = 5)
    classifier.fit(X_train, Y_train)
    return classifier

def model_RF(X_train,Y_train,n_estimators,max_depth):
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=5)
    model.fit(X_train, Y_train)
    return model
    
def model_adaboost(X_train,Y_train):
    classifier=AdaBoostClassifier(random_state=0)
    classifier.fit(X_train,Y_train)
    return classifier

def split_data_standardize(df,split):
    X = np.array(df.drop(['Y'],axis=1).values)#df.iloc[:, :-1].values)
    Y = np.array(df.Y.values)#df.iloc[:, 1].values)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=split, random_state=5)
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)
    label_enc=LabelEncoder()
    Y_train=label_enc.fit_transform(Y_train)
    Y_test=label_enc.transform(Y_test)
    return X_train,X_test,Y_train,Y_test

def predict_performance(model,X_test,Y_test):
    Y_pred = model.predict(X_test)
    a=accuracy_score(Y_test,Y_pred)
    val=precision_recall_fscore_support(Y_test, Y_pred, average='binary')
    p=val[0]
    r=val[1]
    f=val[2]
    return a,p,r,f

def predict_performance_NN(model,X_test,Y_test):
    Y_pred = (model.predict(X_test) > 0.5).astype("int32")
    a=accuracy_score(Y_test,Y_pred)
    val=precision_recall_fscore_support(Y_test, Y_pred, average='binary')
    p=val[0]
    r=val[1]
    f=val[2]
    return a,p,r,f
    
    