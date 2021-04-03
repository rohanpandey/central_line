from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import precision_recall_fscore_support

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
    classifier.fit(X_train,y_train)
    return classifier

def split_data_standardize(df,split):
    X = np.array(df.iloc[:, :-1].values)
    Y = np.array(df.iloc[:, 1].values)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=split, random_state=5)
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)
    return X_train,X_test,Y_train,Y_test

def predict_performance(model,X_test,Y_test):
    Y_pred = model.predict(X_test)
    val=precision_recall_fscore_support(Y_test, Y_pred, average='binary')
    p=val[0]
    r=val[1]
    f=val[2]
    return p,r,f
    