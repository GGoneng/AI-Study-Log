"""
Dataset : iris.csv
target : Setosa or else
feature : sepal.length, sepal.width, petal.length, petal.width
algorithm : Binary Classifier
"""

# import module
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torchinfo import summary
from torch.utils.data import DataLoader, Dataset
from torchmetrics.classification import BinaryF1Score

import pandas as pd
import matplotlib.pyplot as plt


def read_file(file_path, exit_header = 0):
    if (file_path.split(".")[-1] == 'csv'):
        dataDF = pd.read_csv(file_path, header = exit_header)

    elif (file_path.split(".")[-1] == 'json'):
        dataDF = pd.read_json(file_path, header = exit_header)
    
    elif (file_path.split(".")[-1] in ["xlsx", "xls"]):
        dataDF = pd.read_excel(file_path, header = exit_header)

    else:
        dataDF = pd.read_table(file_path, header = exit_header)

    return dataDF


def print_df(df):
    print(f"Data : \n{df.head()}\n\n")


def target_encoder(df, target_column):
    df[target_column] = (df[target_column] == 'Setosa')
    df[target_column] = df[target_column].astype('int')


def print_df_info(df):
    print(f"data's corr : \n{df.corr(numeric_only = True)}\n")
    print(f"data's info : \n{df.info()}\n\n")


def check_


def main():
    FILE_PATH = '../../Data/iris.csv'

    # 파일 불러오기
    irisDF = read_file(FILE_PATH)
    print_df(irisDF)

    # 타겟 범주형 => 정수형 인코딩
    target_encoder(irisDF, 'variety')
    print_df(irisDF)

    # 파일 정보 출력
    print_df_info(irisDF)



if __name__ == '__main__':
    main()