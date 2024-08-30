"""
Predict mpg from auto_mpg 
"""

import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def load_data(data_path, test_path):    
    data = pd.read_csv(data_path)
    test_data = pd.read_csv(test_path)

    return data, test_data


def print_data(data, test_data):
    print(f"Train Data : \n{data}\n\n")
    print(f"Test Data : \n{test_data}\n\n")


def view_info(data, test_data):
    print(f"Data's info : \n{data.info()}\n\n")
    print(f"Test data's info : \n{test_data.info()}\n\n")


def columns_name(data, test_data):
    print(f"Data columns name : {data.columns}")
    print(f"Test data columns name : {test_data.columns}")


def delete_column(data, test_data, column):
    data.drop(column, axis = 1, inplace = True)
    test_data.drop(column, axis = 1, inplace = True)


def drop_NA(data, test_data):
    data.dropna(inplace = True)
    test_data.dropna(inplace = True)


def count_null(data, test_data):
    print(f"Data's Null : \n{data.isnull().sum()}\n")
    print(f"Test's Null : \n{test_data.isnull().sum()}\n")


def change_column(data, test_data, column, type):
    data[column] = [d.split(" ")[0] for d in data[column]]
    data = data[data[column] != "null"]
    data[column] = data[column].astype(type)

    test_data[column] = [d.split(" ")[0] for d in test_data[column]]
    test_data = test_data[test_data[column] != "null"]
    test_data[column] = test_data[column].astype(type)

    return data, test_data


def draw_boxplot(data):
    plt.boxplot(data)
    plt.title("Data의 이상치 조사")
    plt.show()


def print_corr(data, test_data):
    print(f"Data's Corr : \n{data.corr()}\n\n")
    print(f"Test Data's Corr : \n{test_data.corr()}\n\n")


def split_data(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        target,
                                                        test_size = 0.2,
                                                        random_state = 10)    

    return X_train, X_test, y_train, y_test


def Linear_model_score(model, X, y):
    
    pre_score = model.predict(X)

    mse = mean_squared_error(y, pre_score)
    rmse = mean_squared_error(y, pre_score, squared = False)
    mae = mean_absolute_error(y, pre_score)

    r2 = r2_score(y, pre_score)

    print(f"model.coef_ : {len(model.coef_)}개, {model.coef_}")
    print(f"model.intercept_ : {model.intercept_}\n\n")

    score = model.score(X, y)

    print(f"model score : {score}\n\n")

    print(f"mse : {mse}")
    print(f"rmse : {rmse}")
    print(f"mae : {mae}")
    print(f"r2 : {r2}\n\n")

    return score


# def predict_compare(model, X, y):
#     predict_score = pd.Series(model.predict(X).tolist())
#     score = y.reset_index()

#     compare_frame = pd.DataFrame(score, predict_score, columns = ["Price", "Predicted Price"])

#     return compare_frame

def add_new_price(model, features, data):
    data["New_Price"] = model.predict(features).tolist()


def save_csv(data):
    data.to_csv("result.csv", index = False)


def main():
    DATA_FILE = "../Data/train_car_price_data.csv"
    TEST_FILE = "../Data/test_car_price_data.csv"

    data, test_data = load_data(DATA_FILE, TEST_FILE)
    
    columns_name(data, test_data)
    
    delete_column(data, test_data, 'Unnamed: 0')
    delete_column(data, test_data, 'New_Price')
    delete_column(data, test_data, 'Name')
    delete_column(data, test_data, 'Location')
    delete_column(data, test_data, 'Fuel_Type')
    delete_column(data, test_data, 'Transmission')
    delete_column(data, test_data, 'Owner_Type')
        
    print_data(data, test_data) 
    
    drop_NA(data, test_data)
    
    count_null(data, test_data)

    data, test_data = change_column(data, test_data, "Mileage", "float64")
    data, test_data = change_column(data, test_data, "Engine", "int64")
    data, test_data = change_column(data, test_data, "Power", "float64")
    
    print_data(data, test_data)

    view_info(data, test_data)

    print_corr(data, test_data)

    features = data[["Engine", "Power"]]
    target = data["Price"]

    test_features = test_data[["Engine", "Power"]]

    draw_boxplot(data[["Engine", "Power", "Price"]])

    X_train, X_test, y_train, y_test = split_data(features, target)

    model = LinearRegression()
    
    model.fit(X_train, y_train)
    Linear_model_score(model, X_train, y_train)
    Linear_model_score(model, X_test, y_test)
        
    add_new_price(model, test_features, test_data)

    print_data(data, test_data)

    save_csv(test_data)


if __name__ == "__main__":
    main()