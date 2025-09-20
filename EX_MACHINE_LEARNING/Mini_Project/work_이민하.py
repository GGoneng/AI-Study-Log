import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler


def read_txt(PATH):
    with open(PATH, 'r', encoding = "utf-8") as f:
        file = f.read()

    return file


def make_df(X, y, features, subject):
    
    data = pd.DataFrame(X, columns = features)
    data["activity"] = y
    data['person'] = subject
    print(data, "\n\n")
    
    return data


def check_linear(df):
    col = 4
    row = (len(df.columns) + col -1) // col

    plt.figure(figsize = (12, 7))

    for i,column in enumerate(df.columns, 1):
        plt.subplot(row, col, i)
        
        plt.title(f'[{column}]', fontsize=12)
        plt.hist(df[column], bins = 15)
        plt.xticks(fontsize=12)
        
    plt.tight_layout()
    plt.show()


def scaling(X_train, X_test):

    mmScaler = MinMaxScaler()
    mmScaler.fit(X_train)

    X_train_scaled = mmScaler.transform(X_train)
    X_test_scaled = mmScaler.transform(X_test)

    X_train_scaled = pd.DataFrame(X_train_scaled, columns = X_train.columns)
    
    X_test_scaled =pd.DataFrame(X_test_scaled, columns = X_test.columns)

    print(f"X_train_scaled's min : \n{X_train_scaled.min()}\n")
    print(f"X_test_scaled's min : \n{X_test_scaled.min()}\n\n")
    
    return X_train_scaled, X_test_scaled


def find_features(df):
    X_train = pd.DataFrame(df.iloc[:, :-2], columns = df.columns[:-2])
    y_train = df.iloc[:, -2]

    lf_model = RandomForestClassifier(random_state = 10,
                                      oob_score = True)

    lf_model.fit(X_train, y_train)

    feature_names = np.array(lf_model.feature_names_in_)    
    feature_importances = np.array(lf_model.feature_importances_)

    best_features = []
    best_importances = []

    for i in range(25):
        best_idx = np.argmax(feature_importances)
        best_features.append(feature_names[best_idx])
        best_importances.append(feature_importances[best_idx])
        feature_names = np.delete(feature_names, best_idx)
        feature_importances = np.delete(feature_importances, best_idx)

    print(best_features)

    X_train = X_train[best_features]

    plt.figure()
    plt.barh(np.arange(len(best_features)), best_importances)
    plt.yticks(np.arange(len(best_features)), best_features)
    plt.tight_layout()
    plt.show()

    return best_features


def train_model(train_df, test_df, feature_names):
    X_train = train_df[feature_names]
    y_train = train_df['activity']

    X_test = test_df[feature_names]
    y_test = test_df['activity']

    X_train, X_test = scaling(X_train, X_test)

    ex_model = ExtraTreesClassifier(n_estimators = 1000, random_state = 10)
    
    ex_params = {
        'criterion' : ["gini", "entropy",  "log_loss"],
        'max_depth' : range(0, 20),
        'min_samples_split' : range(0, 20),
        'min_samples_leaf' : range(0, 20)
    }

    searchCV = RandomizedSearchCV(ex_model,
                              param_distributions = ex_params,
                              n_iter = 100,
                              cv = 5,
                              verbose = 4)

    searchCV.fit(X_train, y_train)

    print(f'[ searchCV.best_score_ ] {searchCV.best_score_}')
    print(f'[ searchCV.best_params_ ] {searchCV.best_params_}')
    print(f'[ searchCV.best_estimator_ ] {searchCV.best_estimator_}')

    cv_resultDF = pd.DataFrame(searchCV.cv_results_)
    print(cv_resultDF, "\n\n")

    model = searchCV.best_estimator_

    print(f"model's train score : {model.score(X_train, y_train):.6f}")
    print(f"model's test score : {model.score(X_test, y_test):.6f}") 


def main():
    PATH = "../Data/human+activity+recognition+using+smartphones (1)/UCI HAR Dataset/"

    X_train_path = PATH + "train/X_train.txt"
    y_train_path = PATH + "train/y_train.txt"
    subject_train_path = PATH + "train/subject_train.txt"
    
    X_test_path = PATH + "test/X_test.txt"
    y_test_path = PATH + "test/y_test.txt"
    subject_test_path = PATH + "test/subject_test.txt"
    
    features_path = PATH + "features.txt"
    
    train_inertial_path = PATH + "train/Inertial Signals/"
    test_inertial_path = PATH + "test/Inertial Signals/"


    X_train = read_txt(X_train_path)
    y_train = read_txt(y_train_path)
    subject_train = read_txt(subject_train_path)
   
    X_test = read_txt(X_test_path)
    y_test = read_txt(y_test_path)
    subject_test = read_txt(subject_test_path)
    
    features = read_txt(features_path)
    features = features.split('\n')

    X_train = np.array(X_train.split()).reshape(-1, 561)
    y_train = np.array(y_train.split()).reshape(-1, 1)
    subject_train = np.array(subject_train.split()).reshape(-1, 1)
    
    X_test = np.array(X_test.split()).reshape(-1, 561)
    y_test = np.array(y_test.split()).reshape(-1, 1)
    subject_test = np.array(subject_test.split()).reshape(-1, 1)

    for i in range(9):
        features[i] = features[i][2:]

    for i in range(9, 99):
        features[i] = features[i][3:]
    
    for i in range(99, len(features)):
        features[i] = features[i][4:]

    features.pop()
    features = np.array(features)

    train_df = make_df(X_train, y_train, features, subject_train)
    test_df = make_df(X_test, y_test, features, subject_test)

    best_features = find_features(train_df)    

    train_model(train_df, test_df, best_features)


if __name__ == "__main__":
    main()