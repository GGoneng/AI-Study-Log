import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier


def load_data(DATA_FILE):
    data = pd.read_csv(DATA_FILE)
    
    return data


def print_info(data):
    print(f'{data.info()}\n\n')


def print_head(data):
    print(f"Data's head : \n{data.head()}\n\n")


def check_null(data):
    print((data[data.columns] == '?').sum())
    data['stalk-root'] = data['stalk-root'].replace('?', np.NAN)
    data.fillna(method = 'ffill')

    return data


def encoding(data):
    LEncoder = LabelEncoder()
    LEncoder.fit(data['class'])

    encoded_data = pd.get_dummies(data.iloc[:, 1:])
    encoded_data = encoded_data.replace({True : 1, False : 0})
    encoded_data['class'] = LEncoder.transform(data['class'])
    
    return encoded_data


def split_data(feature, target):
    X_train, X_test, y_train, y_test = train_test_split(feature, target,
                                                        stratify = target,
                                                        random_state = 10
                                                        )
    
    return X_train, X_test, y_train, y_test


def best_param(model, param, X_train, y_train):
    searchCV = GridSearchCV(model, param, cv = 5, verbose = True, return_train_score = True)
    searchCV.fit(X_train, y_train)
    
    return searchCV.best_estimator_, searchCV.best_score_

def best_model(model, X_train, y_train):
    result = cross_validate(model, X_train, y_train,
                   return_train_score = True,
                   return_estimator = True)

    resultDF = pd.DataFrame(result)
    resultDF['diff'] = abs(resultDF['test_score'] - resultDF['train_score'])
    resultDF.sort_values(by = 'diff', inplace = True)

    print(resultDF, "\n\n")

    b_model = resultDF['estimator'][0]
    
    return b_model

def print_score(name, model, X_test, y_test):
    print(f"{name}'s score : {model.score(X_test.values, y_test.values)}\n")


def main():
    DATA_FILE = '../Data/mushrooms.csv'
    data = load_data(DATA_FILE)
    
    print_head(data)
    print_info(data)

    data = check_null(data)

    encoded_data = encoding(data)

    print_head(encoded_data)

    feature = encoded_data.iloc[:, :-1]
    target = encoded_data['class']

    print_head(feature)

    X_train, X_test, y_train, y_test = split_data(feature, target)

    l_model = LogisticRegression(max_iter = 1000)
    d_model = DecisionTreeClassifier(random_state = 10)
    k_model = KNeighborsClassifier()
    v_model = VotingClassifier(estimators = [('l_model', l_model), 
                                             ('d_model', d_model),
                                             ('k_model', k_model)]
                                            )   
    
    l_params = {
        'penalty' : ['l1', 'l2', 'elasticnet'],
        'C' : [0.5, 1.0, 10.0, 100.0],
    }

    d_params = {
        'max_depth' : [None, 10, 20, 30],
        'min_samples_split' : [2, 5, 10, 20],
        'min_samples_leaf' : [1, 3, 5, 10],
    }

    v_params = {
        'voting' : ['hard', 'soft']
    }


    l_model = best_param(l_model, l_params, X_train, y_train)
    l_model = best_model(l_model, X_train, y_train)

    d_model = best_param(d_model, d_params, X_train, y_train)
    d_model = best_model(d_model, X_train, y_train)

    v_model = best_param(v_model, v_params, X_train.values, y_train.values)
    v_model = best_model(v_model, X_train.values, y_train.values)

    print_score("LogisticRegression", l_model, X_test, y_test)
    print_score("DecisionTreeClassifier", d_model, X_test, y_test)
    print_score("VotingClassifier", v_model, X_test, y_test)


if __name__ == "__main__":
    main()