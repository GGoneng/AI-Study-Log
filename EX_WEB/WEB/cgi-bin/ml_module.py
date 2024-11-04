import pandas as pd
import pickle

def preprocessing_ml(dataDF, column):

    with open(r'C:\Users\KDP-2\OneDrive\바탕 화면\Python\EX_WEB\WEB\ML\mmScaler.pkl', 'rb') as f:
        mmScaler = pickle.load(f)

    dataDF_scaled = mmScaler.transform(dataDF)

    dataDF_scaled = pd.DataFrame(dataDF_scaled, columns = column)

    return dataDF_scaled

def predict_ml(model, dataframe):

    y = model.predict(dataframe)

    return y[0]


