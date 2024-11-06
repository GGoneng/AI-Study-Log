from flask import Flask, render_template, request

from selenium import webdriver
from bs4 import BeautifulSoup

import time
import pickle

import pandas as pd

import torch

from .models.RNNmodel import RNNModel


app = Flask(__name__)

MODEL_PATH = r'C:\Users\KDP-2\OneDrive\바탕 화면\FLASK_AI\Project\WEB\models'

def load_model(model_path, model):
    model.load_state_dict(torch.load(model_path, map_location = torch.device('cpu')))
    model.eval()

    return model


def load_scaler(scaler_path):
    with open(scaler_path, 'rb') as f:
        rb_scaler = pickle.load(f)
    
    return rb_scaler


def crawling(code, page):
    etf_price = []
    closing_price = []
    market_price = []
    high_price = []
    low_price = []
    volume = []

    driver = webdriver.Chrome()
    driver.get(f'https://finance.naver.com/item/sise_day.naver?code={code}&page={page}') 

    html = driver.page_source

    bs = BeautifulSoup(html, 'html.parser')
    rows = bs.find_all('span', {'class' : 'tah'})

    time.sleep(3)

    for i in range(len(rows) - 1, 6, -1):
        if i % 7 == 0:
            pass
        elif i % 7 == 1:
            closing_price.append(rows[i].text)
        elif i % 7 == 2:
            pass
        elif i % 7 == 3:
            market_price.append(rows[i].text)
        elif i % 7 == 4:
            high_price.append(rows[i].text)
        elif i % 7 == 5:
            low_price.append(rows[i].text)
        elif i % 7 == 6:
            volume.append(rows[i].text)
    
    etf_price.extend(market_price)
    etf_price.extend(high_price)
    etf_price.extend(low_price)
    etf_price.extend(volume)
    etf_price.extend(closing_price)

    columns_name = []
    list_name = ['market_price', 'high_price', 'low_price', 'volume', 'closing_price']

    for i in range(5):
        for j in range(1, 10):
            columns_name.append(f'{list_name[i]}_{j}')

    data = dict(zip(columns_name, etf_price))

    stock_df = pd.DataFrame(data, index = [0])

    return stock_df, columns_name


def del_punctuation(dataframe):
    for name in dataframe.columns:
        dataframe[name] = dataframe[name].str.replace(',', '')

    return dataframe


def preprocessing(dataframe, columns_name):
    dataframe = del_punctuation(dataframe)
    dataframe = dataframe.astype('int')
    
    rb_scaler = load_scaler(MODEL_PATH + '/robust_scaler.pkl')

    scaled_df = rb_scaler.transform(dataframe)

    scaled_ts = torch.FloatTensor(scaled_df)

    return scaled_ts

def predict_price(model, data_tensor):
    pre_val = model(data_tensor)

    return pre_val

@app.route('/', methods = ['GET', 'POST'])

def index():
    output = 0

    if request.method == 'POST':
        stock = int(request.form.get('stock'))
        page = int(request.form.get('page'))

        stock_df, columns = crawling(stock, page)

        scaled_ts = preprocessing(stock_df, columns)
        
        input_size_1 = 45
        hidden_dim_1 = 1024
        n_layer_1 = 2
        dropout_1 = 0.9

        input_size_2 = 45
        hidden_dim_2 = 2048
        n_layer_2 = 2
        dropout_2 = 0.9

        input_size_3 = 45
        hidden_dim_3 = 512
        n_layer_3 = 2
        dropout_3 = 0.9

        # 104, stock_model == 1
        # 18 == 2
        # 3, 4, 5 == 3

        model_1 = RNNModel(input_size = input_size_1,
                         hidden_dim = hidden_dim_1,
                         n_layers = n_layer_1,
                         dropout = dropout_1,
                         bidirectional = True,
                         model_type = 'lstm').to('cpu')
        
        model_1 = load_model(MODEL_PATH + '/stock_model.pth', model_1)

        model_2 = RNNModel(input_size = input_size_1,
                         hidden_dim = hidden_dim_1,
                         n_layers = n_layer_1,
                         dropout = dropout_1,
                         bidirectional = True,
                         model_type = 'lstm').to('cpu')
        
        model_2 = load_model(MODEL_PATH + '/model_weights_104.pth', model_2)

        model_3 = RNNModel(input_size = input_size_2,
                         hidden_dim = hidden_dim_2,
                         n_layers = n_layer_2,
                         dropout = dropout_2,
                         bidirectional = True,
                         model_type = 'lstm').to('cpu')

        model_3 = load_model(MODEL_PATH + '/model_weights_18.pth', model_3)

        model_4 = RNNModel(input_size = input_size_3,
                         hidden_dim = hidden_dim_3,
                         n_layers = n_layer_3,
                         dropout = dropout_3,
                         bidirectional = False,
                         model_type = 'lstm').to('cpu')

        model_4 = load_model(MODEL_PATH + '/model_weights_6.pth', model_4)

        model_5 = RNNModel(input_size = input_size_3,
                         hidden_dim = hidden_dim_3,
                         n_layers = n_layer_3,
                         dropout = dropout_3,
                         bidirectional = False,
                         model_type = 'lstm').to('cpu')

        model_5 = load_model(MODEL_PATH + '/model_weights_20.pth', model_5)

        model_6 = RNNModel(input_size = input_size_3,
                         hidden_dim = hidden_dim_3,
                         n_layers = n_layer_3,
                         dropout = dropout_3,
                         bidirectional = False,
                         model_type = 'lstm').to('cpu')

        model_6 = load_model(MODEL_PATH + '/model_weights_5.pth', model_6)
        


        pre_val_1 = predict_price(model_1, scaled_ts)
        pre_val_2 = predict_price(model_2, scaled_ts)
        pre_val_3 = predict_price(model_3, scaled_ts)
        pre_val_4 = predict_price(model_4, scaled_ts)
        pre_val_5 = predict_price(model_5, scaled_ts)
        pre_val_6 = predict_price(model_6, scaled_ts)


        output = format(int(pre_val_5), ',')

    return render_template('index.html', output = output)

if __name__ == '__main__':
    app.run(debug = True)
    