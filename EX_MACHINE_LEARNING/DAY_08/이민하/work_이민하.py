import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import ExtraTreesClassifier

def read_file(DATA_FILE):
    with open(DATA_FILE, 'r', encoding = 'utf-8') as f:
        data = f.read()
    
    return data


def make_list(DATA_FILE, name, i):
    data = read_file(DATA_FILE + f"{name}-{i}.txt")
    data = list(data)

    return data


def preprocess(data, name):
    L = []

    for alpha in data:
        if ('a' <= alpha <= 'z') or ('A' <= alpha <= 'Z'):
            L.append(alpha.lower())
    data = dict(sorted(dict(pd.Series(L).value_counts()).items()))
    data['|Country'] = name

    return data


def make_df(data):
    data_list = []
    column_list = []
    alpha_list = list(range(ord('a'), ord('z') + 1))
    
    for i in range(len(alpha_list)):
        column_list.append(chr(alpha_list[i]))
    column_list.append('|Country')

    for i in range(len(data)):
        for j in range(len(column_list)):
            if column_list[j] not in (data[i].keys()):
                data[i][column_list[j]] = 0
                data[i] = dict(sorted(data[i].items()))
        data_list.append(data[i].values())

    df = pd.DataFrame(data = data_list, columns = column_list)

    return df


def split_data(data):
    X = data.iloc[:, :-1]
    y = data['|Country']

    return X, y


def ex_classifier(X_train, X_test, y_train, y_test):
    params = {'max_depth' : range(2, 16),
          'min_samples_leaf' : range(5, 16),
          'criterion' : ['gini', 'entropy', 'log_loss']}
    
    ex_model = ExtraTreesClassifier(n_estimators = 500, random_state = 7)

    searchCV = RandomizedSearchCV(ex_model,
                              param_distributions = params,
                              n_iter = 50,
                              verbose = 4)
    
    searchCV.fit(X_train, y_train)

    print(f'\n\n[ searchCV.best_score_ ] {searchCV.best_score_}')
    print(f'[ searchCV.best_params_ ] {searchCV.best_params_}')
    print(f'[ searchCV.best_estimator_ ] {searchCV.best_estimator_}\n\n')


    cv_resultDF = pd.DataFrame(searchCV.cv_results_)
    print(cv_resultDF)

    model = searchCV.best_estimator_

    print(f"\n\nmodel's score : {model.score(X_test, y_test)}")


def main():
    TRAIN_DATA_FILE = '../Data/language_predict/train/'
    TEST_DATA_FILE = '../Data/language_predict/test/'

    train_list = []
    test_list = []

    for i in range(1, 21):
        if i <= 5:
            train_list.append(preprocess(make_list(TRAIN_DATA_FILE, "en", i), "en"))
        elif i <= 10:
            train_list.append(preprocess(make_list(TRAIN_DATA_FILE, "fr", i), "fr"))
        elif i <= 15:
            train_list.append(preprocess(make_list(TRAIN_DATA_FILE, "id", i), "id"))
        else:
            train_list.append(preprocess(make_list(TRAIN_DATA_FILE, "tl", i), "tl"))     
    
    for i in range(1, 9):
        if i <= 2:
            test_list.append(preprocess(make_list(TEST_DATA_FILE, "en", i), "en"))
        elif i <= 4:
            test_list.append(preprocess(make_list(TEST_DATA_FILE, "fr", i), "fr"))
        elif i <= 6:
            test_list.append(preprocess(make_list(TEST_DATA_FILE, "id", i), "id"))
        else:
            test_list.append(preprocess(make_list(TEST_DATA_FILE, "tl", i), "tl"))

    train_df = make_df(train_list)
    test_df = make_df(test_list)

    X_train, y_train = split_data(train_df)
    X_test, y_test = split_data(test_df)

    ex_classifier(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()