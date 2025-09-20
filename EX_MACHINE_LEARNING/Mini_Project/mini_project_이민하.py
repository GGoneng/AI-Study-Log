import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.tree import plot_tree


def read_data(DATA_FILE):
    data = pd.read_csv(DATA_FILE)

    return data


def print_info(data):
    print(data.info(), "\n\n")


def check_null(data):
    print(f"Data's null : \n{(data[data.columns] == 0.).sum()}\n\n")
    data[data[data.columns] == 0.] = np.NAN

    data.dropna(inplace = True)


def print_corr(data):
    print(F"Data's corr : \n{data.corr(numeric_only = True)}\n\n")


def encoding(data):
    data = pd.get_dummies(data)
    data.replace(True, 1, inplace = True)
    data.replace(False, 0, inplace = True)

    return data


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


def draw_hist(X_train):
    col = 3
    row = (len(X_train.columns) + col -1) // col

    plt.figure(figsize = (12, 7))

    for i,column in enumerate(X_train.columns, 1):
        plt.subplot(row, col, i)
        
        plt.title(f'[{column}]', fontsize=12)
        plt.hist(X_train[column], bins = 15)
        plt.xticks(fontsize=12)
        
    plt.tight_layout()
    plt.show()


def split_data(data):

    data[:2] = np.square(data[:2])
    data[3:7] = np.log(data[3:7] + 1)

    data['Rings'] = data['Rings'] + 1.5
    feature = data.iloc[:, [4, 5, 6]]
    target = data.iloc[:, 7]

    X_train, X_test, y_train, y_test = train_test_split(feature, target,
                                                        test_size= 0.2,
                                                        random_state = 12)
    
    return X_train, X_test, y_train, y_test


# def dt_regress(X_train, X_test, y_train, y_test):
#     dt_model = DecisionTreeRegressor(random_state = 12, max_depth = 4)
#     dt_model.fit(X_train, y_train)
     
#     print(dt_model.score(X_train, y_train))
#     print(dt_model.score(X_test, y_test))


def find_best_model(X_train, y_train):
    dt_model = DecisionTreeRegressor(random_state = 12)
    d_params = {
        'criterion' : ["squared_error", "friedman_mse",  "poisson"],
        'splitter' : ['best', 'random'],
        'max_depth' : range(0, 10),
        'min_samples_split' : range(0, 10),
        'min_samples_leaf' : range(0, 15),
    }
    searchCV = RandomizedSearchCV(dt_model,
                              param_distributions = d_params,
                              n_iter = 100,
                              cv = 5,
                              verbose = 4)
    
    searchCV.fit(X_train, y_train)

    print(f'[ searchCV.best_score_ ] {searchCV.best_score_}')
    print(f'[ searchCV.best_params_ ] {searchCV.best_params_}')
    print(f'[ searchCV.best_estimator_ ] {searchCV.best_estimator_}')

    cv_resultDF = pd.DataFrame(searchCV.cv_results_)
    print(cv_resultDF, "\n\n")

    return searchCV.best_estimator_

def main():
    DATA_FILE = '../Data/abalone_train.csv'
 

    train_data = read_data(DATA_FILE)

    print(train_data)

    print_info(train_data)

    check_null(train_data)

    print_info(train_data)

    print_corr(train_data)

    train_data = encoding(train_data)

    X_train, X_test, y_train, y_test = split_data(train_data)
    X_train_scaled, X_test_scaled = scaling(X_train, X_test)


    print(X_train_scaled.min())
    print(X_test_scaled.min())

    draw_hist(X_train_scaled)

    best_model = find_best_model(X_train_scaled, y_train)

    print(f"model's train score : {best_model.score(X_train_scaled, y_train)}")
    print(f"model's test score : {best_model.score(X_test_scaled, y_test)}")

    y = best_model.predict(X_test)

    plt.figure(figsize=(10, 6))
    plot_tree(best_model, feature_names=['Shucked_weight', 'Viscera_weight', 'Shell_weight'], filled=True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plot_tree(best_model, feature_names=['Shucked_weight', 'Viscera_weight', 'Shell_weight'], max_depth = 2, filled=True)
    plt.tight_layout()
    plt.show()


    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    print(f'\n\nmse      : {mean_squared_error(y_test, y)}')
    print(f'rmse      : {mean_squared_error(y_test, y, squared=False)}')
    print(f'mae      : {mean_absolute_error(y_test, y)}')
    print(f'r2_score : {r2_score(y_test, y)}')

    print("비교 : ")
    for i in range(len(y_test)):
        print(f'\n{np.array(y_test)[i]} : {np.array(y)[i]}')


if __name__ == "__main__":
    main()