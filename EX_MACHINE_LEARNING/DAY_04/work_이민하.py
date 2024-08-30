"""
titanic 데이터셋 생존자 예측
- Predicted Algorithm : KNN Classifier
- Predicted Features : pclass, sex, age, class
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


def load_data(file_path):
    data = pd.read_csv(file_path)
    
    return data


def print_head(data):
    print(f"Data's head : \n{data.head()}\n\n")


def print_info(data):
    print(f"{data.info()}\n\n")


def fill_na(data):
    data['Age'].fillna(data["Age"].mean(), inplace = True)
    data['Cabin'].fillna('N', inplace = True)
    data['Embarked'].fillna('N', inplace = True)

    print(f"Data's Null Count : \n{data.isnull().sum().sum()}\n\n")


def print_value_counts(data, column1, column2, column3):
    print(f"Sex 값 분포 : \n{data[column1].value_counts()}\n")
    print(f"Cabin 값 분포 : \n{data[column2].value_counts()}\n")
    print(f"Embarked 값 분포 : \n{data[column3].value_counts()}\n\n")


def change_cabin(data):
    data['Cabin'] = data['Cabin'].str[:1]
    print(f"Cabin's alphabet : \n{data['Cabin'].head()}\n\n")


def sex_count(data):
    print(f"Sex Group Survived Count : \n{data.groupby(['Sex', 'Survived'])['Survived'].count()}\n\n")


def draw_sex_survived(data):
    sns.barplot(x = 'Sex', y = 'Survived', data = data)
    plt.show()

    sns.barplot(x = "Pclass", y = "Survived", hue = "Sex", data = data)
    plt.show()


def get_category(age):
    cat = ""
    if age <= -1 : cat = 'Unknown'
    elif age <= 5 : cat = 'Baby'
    elif age <= 12 : cat = "Child"
    elif age <= 18 : cat = "Teenager"
    elif age <= 25 : cat = "Student"
    elif age <= 35 : cat = "Young Adult"
    elif age <= 60 : cat = "Adult"
    else: cat = "Elderly"

    return cat


def draw_age_survived(data):
    plt.figure()
    group_names = ["Unknown", "Baby", "Child", "Teenager", "Student", "Young Adult", "Adult", "Elderly"]

    data["Age_cat"] = data["Age"].apply(lambda x: get_category(x))
    sns.boxplot(x = "Age_cat", y = "Survived", hue = "Sex", data = data, order = group_names)
    data.drop('Age_cat', axis = 1, inplace = True)
    plt.tight_layout()
    plt.show()


def encode_features(data):
    data['Cabin'] = data['Cabin'].str[:1]
    features = ['Cabin', 'Sex', 'Embarked']
    for feature in features:
        le = LabelEncoder()
        le.fit(data[feature])
        data[feature] = le.transform(data[feature])

    return data

def fillna(data):
    data['Age'].fillna(data["Age"].mean(), inplace = True)
    data['Cabin'].fillna('N', inplace = True)
    data['Embarked'].fillna('N', inplace = True)
    data['Fare'].fillna(0, inplace = True)
    
    return data

def drop_features(data):
    data.drop(['PassengerId', 'Name', 'Ticket'], axis = 1, inplace = True)
    
    return data


def transform_features(data):
    data = fillna(data)
    data = drop_features(data)
    data = encode_features(data)
    
    return data

def preprocess(data):
    y_titanic_df = data["Survived"]
    X_titanic_df = data.drop('Survived', axis = 1)

    X_titanic_df = transform_features(X_titanic_df)

    return X_titanic_df, y_titanic_df

def make_class():
    dt_clf = DecisionTreeClassifier(random_state = 11)
    rf_clf = RandomForestClassifier(random_state = 11)
    lr_clf = LogisticRegression(solver = 'liblinear')

    return dt_clf, rf_clf, lr_clf

def decision_tree(dt_clf, X_train, X_test, y_train, y_test):
    dt_clf.fit(X_train, y_train)
    dt_pred = dt_clf.predict(X_test)
    print("DecisionTreeClassifier 정확도 : {0:4f}".format(accuracy_score(y_test, dt_pred)))

    return dt_clf


def random_forest(rf_clf, X_train, X_test, y_train, y_test):
    rf_clf.fit(X_train, y_train)
    rf_pred = rf_clf.predict(X_test)
    print("RandomForestClassifier 정확도 : {0:4f}".format(accuracy_score(y_test, rf_pred)))

    return rf_clf


def logistic_regression(lr_clf, X_train, X_test, y_train, y_test):
    lr_clf.fit(X_train, y_train)
    lr_pred = lr_clf.predict(X_test)
    print("LogisticRegression 정확도 : {0:4f}\n\n".format(accuracy_score(y_test, lr_pred)))

    return lr_clf


def exec_kfold(clf, X_titanic_df, y_titanic_df, folds = 5):
    kfold = KFold(n_splits = folds)
    scores = []

    for iter_count, (train_index, test_index) in enumerate(kfold.split(X_titanic_df)):
        X_train, X_test = X_titanic_df.values[train_index], X_titanic_df.values[test_index]
        y_train, y_test = y_titanic_df.values[train_index], y_titanic_df.values[test_index]

        clf.fit(X_train, y_train)
        predictions = clf.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        scores.append(accuracy)
        print("교차 검증 {0} 정확도 : {1:.4f}".format(iter_count, accuracy))

    mean_score = np.mean(scores)
    print("평균 정확도 : {0:.4f}\n\n".format(mean_score))
    

def exec_cvs(dt_clf, X_titanic_df, y_titanic_df):
    scores = cross_val_score(dt_clf, X_titanic_df, y_titanic_df, cv = 5)

    for iter_count, accuracy in enumerate(scores):
        print("교차 검증 {0} 정확도 : {1:.4f}".format(iter_count, accuracy))
    
    print("평균 정확도 : {0:.4f}\n\n".format(np.mean(scores)))


def main():
    DATA_FILE = '../Data/titanic.csv'
    data = load_data(DATA_FILE)
    
    print_head(data)
    print_info(data)

    fill_na(data)

    print_value_counts(data, 'Sex', 'Cabin', 'Embarked')

    change_cabin(data)

    sex_count(data)

    draw_sex_survived(data)

    draw_age_survived(data)

    data = encode_features(data)
    print_head(data)

    data = load_data(DATA_FILE)

    X_titanic_df, y_titanic_df = preprocess(data)

    X_train, X_test, y_train, y_test = train_test_split(X_titanic_df, y_titanic_df,
                                                        test_size = 0.2, random_state = 11)

    dt_clf, rf_clf, lr_clf = make_class()
    
    dt_clf = decision_tree(dt_clf, X_train, X_test, y_train, y_test)
    rf_clf = random_forest(rf_clf, X_train, X_test, y_train, y_test)
    lr_clf = logistic_regression(lr_clf, X_train, X_test, y_train, y_test)

    exec_kfold(dt_clf, X_titanic_df, y_titanic_df, folds = 5)
    exec_cvs(dt_clf, X_titanic_df, y_titanic_df)


if __name__ == "__main__":
    main()

