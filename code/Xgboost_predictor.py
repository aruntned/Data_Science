# Author: Arun Thomas Varughese
# Date: 12/09/2020
# Version: 1.0
# Name: Xgboost_predictor.py

# import libraries
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score
import joblib
import sys
import pandas as pd
import numpy as np
import json
import csv
import zipfile


# write predictions into csv file
def write_predictions(output_prediction_path, prediction):
    np.savetxt(output_prediction_path, prediction, delimiter=',')


# load model
def load_model(model_drive_path):
    model_loaded = joblib.load(model_drive_path)
    return model_loaded

# predict output
def predict(X, model):
    y_pred = model.predict(X)
    return y_pred

# read zip file
def read_zip(zip_path, file_name):
    zf = zipfile.ZipFile(zip_path)
    updated_data = pd.read_csv(zf.open(file_name))
    return updated_data

# get predictions function can be used to get predictions as a numpy array
def get_predictions(updated_data_zip_path, updated_data_csv_name, stored_model_path, target):
    model = load_model(stored_model_path)
    # print('load done')
    updated_data = read_zip(updated_data_zip_path, updated_data_csv_name)
    # print('read done')
    if target in updated_data.columns:
        data_labels = updated_data[target]
        data_features = updated_data.drop(target, axis=1)
    else:
        data_features = updated_data

    # get predictions from model
    predictions = predict(data_features, model)
    # convert negative predictions to 0 as -ve values are invalid
    predictions = np.where(predictions < 0, 0, predictions)

    return predictions

# !python  /content/Xgboost_predictor.py 'cleaneddatapath in zip' 'new csv name' 'output:predictions path' 'load model path' 'target column name'
if __name__ == '__main__':
    updated_data_zip_path = sys.argv[1]
    updated_data_csv_name = sys.argv[2]
    output_prediction_path = sys.argv[3]
    stored_model_path = sys.argv[4]
    target = sys.argv[5]

    predictions = get_predictions(updated_data_zip_path,updated_data_csv_name,stored_model_path,target)
    write_predictions(output_prediction_path, predictions)






