"""
Find Fishes' Species

File : fish.csv
Target : Species
Feature : Weight, Length, Diagonal, Height, Width
Algorithm : KNN Classifier
Scaling : MinMaxScaler
"""

# 모듈 로딩
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold


# 데이터 로딩 함수
def load_csv_file(DATA_FILE, column, fish1, fish2, fish3):
    data = pd.read_csv(DATA_FILE)
    mask = (data[column] == fish1) | (data[column] == fish2) | (data[column] == fish3)

    data = data[mask]
    data.reset_index(drop = True, inplace = True)

    return data


# 데이터 출력 함수
def print_data(data):
    print(f'Data : \n{data}\n\n')


# 데이터 정보 출력 함수
def print_data_info(data):
    print(f"{data.info()}\n\n")


# 이상치 체크 (박스 플롯) 함수
def box_plot(data, columns):
    plt.boxplot(data[columns])
    plt.show()


# 이상치 제거 함수:
def drop_outlier(data):
    print(data[(data["Weight"] == 0) | (data["Length"] == 0) | (data["Diagonal"] == 0) | (data["Height"] == 0) | (data["Width"] == 0)])
    data.drop(40, axis = 0, inplace = True)


# 인코더 (라벨 인코딩 사용) 함수
def encoding(data, column, name):
    lencoder = LabelEncoder()
    lencoder.fit(data[column])
    l_items = lencoder.transform(data[column])
    data[name] = l_items    


# 상관관계 출력 함수
def print_corr(data):
    print(f"Data's corr :\n{data.corr(numeric_only = True)}\n\n")


# 데이터 셋 나누는 함수
def split_dataset(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        target,
                                                        test_size = 0.2,
                                                        stratify = target,
                                                        random_state = 10)

    print(f"X_train : {X_train.shape}, {X_train.ndim}D")
    print(f"X_test : {X_test.shape}, {X_test.ndim}D")
    
    print(f"y_train : {y_train.shape}, {y_train.ndim}D")
    print(f"y_test : {y_test.shape}, {y_test.ndim}D\n\n")

    return X_train, X_test, y_train, y_test


def scaler(X_train, X_test):
    mmScaler = MinMaxScaler()
    mmScaler.fit(X_train)

    X_train_scaled = mmScaler.transform(X_train)
    X_test_scaled = mmScaler.transform(X_test)

    print(f"X_train_scaled : {X_train_scaled.shape}, {X_train_scaled.min()}, {X_train_scaled.max()}")
    print(f"X_test_scaled : {X_test_scaled.shape}, {X_test_scaled.min()}, {X_test_scaled.max()}\n\n")

    return X_train_scaled, X_test_scaled, mmScaler

def knn_classifier(X_train, y_train): # features는 2D, target은 1D
    model = KNeighborsClassifier()

    # kf = KFold(n_splits = 3) 

    result = cross_validate(model, X_train, y_train,
                            cv = 3,
                            scoring = ['neg_mean_squared_error', 'r2'],
                            return_train_score = True,
                            return_estimator = True)

    resultDF = pd.DataFrame(result)[['test_r2', 'train_r2']]
    resultDF['diff'] = resultDF['test_r2'] - resultDF['train_r2']
    resultDF['diff'].sort_values()[0]

    print(resultDF, "\n\n")

    model = result['estimator'][0]

    return model

def draw_scatter(model, data, X_train_scaled):
    distance, index = model.kneighbors(data)
    print(distance)
    neighbors = index.reshape(-1).tolist()
    print(X_train_scaled[neighbors])
    k_weight = X_train_scaled[neighbors][:, 0]
    k_height = X_train_scaled[neighbors][:, 1]
    
    print(f"[{k_weight}, {k_height}]\n")

    plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], color = 'y')
    plt.plot(data[0, 0], data[0, 1], 'r^')
    plt.scatter(k_weight, k_height, color = 'b')
    plt.show()


# 메인 함수
def main():
    # 데이터 파일 경로 설정
    DATA_FILE = '../Data/fish.csv'
    
    fishDF = load_csv_file(DATA_FILE, 'Species', 'Bream', 'Smelt', 'Perch')
    print_data(fishDF)
    
    print_data_info(fishDF)
    # 겉으로 보이는 결측치 X, 타겟은 범주형 => 수치형으로 바꿔줄 생각,
    # OneHotEncoder, LabelEncoder, OrdinalEncoder 상황에 맞게 사용 

    box_plot(fishDF, ["Weight", "Length", "Diagonal", "Height", "Width"])

    # 0인 값이 있어서 제거
    drop_outlier(fishDF)

    # 제거 확인 (데이터 수 159 -> 158)
    print_data_info(fishDF)

    encoding(fishDF, "Species", "Species_num")
    print_data(fishDF)

    print_corr(fishDF)

    target = fishDF["Species_num"]

    for i in range(len(fishDF.columns[1:6]) - 1):
        for j in range(i + 1, len(fishDF.columns[1:6])):
            print(f"features : [{fishDF.columns[1:6][i]}, {fishDF.columns[1:6][j]}]")
            features = fishDF[[fishDF.columns[1:6][i], fishDF.columns[1:6][j]]]

            X_train, X_test, y_train, y_test = split_dataset(features, target)
            X_train_scaled, X_test_scaled, mmScaler = scaler(X_train, X_test)

            model = knn_classifier(X_train_scaled, y_train)

    features = fishDF[['Weight', 'Height']]
    
    X_train, X_test, y_train, y_test = split_dataset(features, target)
    X_train_scaled, X_test_scaled, mmScaler = scaler(X_train, X_test)

    model = knn_classifier(X_train_scaled, y_train)
    # model.fit(X_train_scaled, y_train)
    print(f"model's score : \n{model.score(X_test_scaled, y_test)}")

    new_data = pd.DataFrame([[200, 8]], columns = ['Weight', 'Height'])
    new_data_scaled = mmScaler.transform(new_data)
    
    
    print(f"model's prediction : {model.predict(new_data_scaled)}")

    draw_scatter(model, new_data_scaled, X_train_scaled)

if __name__ == '__main__':
    main()