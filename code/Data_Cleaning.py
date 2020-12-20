# Author: Arun Thomas Varughese
# Date: 12/09/2020
# Version: 1.3
# Name: Data_Cleaning.py
# input:  1) raw_data:csv file  2)args: json file
# output: 1) updated_data: csv file in zip 2) feature list: csv file
# example: python /content/Data_Cleaning.py 'houston_data_master2.csv' '/content/data_updated.csv' 'args.json' 'features_cleaned.csv'
# raw data is houston_data_master2.csv and args file is args.json and we get updated data in 'data_updated.csv' in '/content/data_updated.zip'


# import libraries
import sys
import pandas as pd
import numpy as np
import json
import csv

# convert name to name: category name format
def convert_name(original_name,name):
  return original_name+":"+name

# Append line to a csv file
def move_to_csv(file,x,y):
    with open(file, mode='a',newline='') as data_file:
        data_writer = csv.writer(data_file, delimiter=',')
        data_writer.writerow([x,y])

# Function to convert a categorical column to numerical column using OHE
def convert_categorical_to_numerical(raw_input_data,input_data_updated,col_name):
    if col_name in input_data_updated.columns:
        dummy_type=pd.get_dummies(raw_input_data[col_name])
        dummy_type=dummy_type.rename(columns={x: convert_name(col_name,x) for x in dummy_type.columns})
        input_data_updated=pd.concat([input_data_updated, dummy_type], axis=1)
        del dummy_type
        input_data_updated = input_data_updated.drop([col_name], axis=1)
    return input_data_updated

# Function to create first updated dataframe using given column name
def create_updated_df(raw_data,column_name):

    dummy_secondary_type = pd.get_dummies(raw_data[column_name])

    dummy_secondary_type = dummy_secondary_type.rename(
        columns={x: convert_name(column_name, x) for x in dummy_secondary_type.columns})

    input_data_updated = pd.concat([raw_data, dummy_secondary_type], axis=1)
    input_data_updated = input_data_updated.drop([column_name], axis=1)
    del dummy_secondary_type
    return input_data_updated

# Function to read json file and set variables for different lists such as columns to be dropped
def read_json(arg_json_file):
    with open(arg_json_file) as f:
        arg_data = json.load(f)

    column_name=arg_data['column_name']
    columns_drop=arg_data['columns_drop']
    columns_ohe = arg_data['columns_ohe']
    columns_01 = arg_data['columns_01']
    columns_drop_corr = arg_data['columns_drop_corr']
    primary_id = arg_data['primary_id']

    return primary_id,column_name,columns_drop,columns_ohe,columns_01,columns_drop_corr

# clean data function
def clean_data(raw_data,arg_json_file):
    primary_id, column_name, columns_drop, columns_ohe, columns_01, columns_drop_corr = read_json(arg_json_file)
    raw_data_updated = create_updated_df(raw_data, column_name)

    raw_data_updated = raw_data_updated.drop(columns_drop, axis=1)

    for name in columns_ohe:
        raw_data_updated = convert_categorical_to_numerical(raw_data, raw_data_updated, name)

    for name in columns_01:
        raw_data_updated[name] = raw_data_updated[name].replace('N', 0)
        raw_data_updated[name] = raw_data_updated[name].replace('Y', 1)

    raw_data_updated = raw_data_updated.drop(columns_drop_corr, axis=1)

    return raw_data_updated

# write features to a csv file given path and dataframe
def write_features(data,path):

    pos=1
    for feat in data.columns:
        move_to_csv(path,pos,feat)
        pos+=1

# write dataframe to a csv file
def write_data(data,path):
    fname=path.split('/')[-1]
    compression_opts = dict(method='zip',
                        archive_name=fname)
    semi_path=path.strip('.csv').strip('.zip')
    zip_path=semi_path+'.zip'
    data.to_csv(zip_path, index=False,compression=compression_opts)

# read data from a csv file
def read_data(raw_data_csv_path):
    return pd.read_csv(raw_data_csv_path,low_memory=False)


def get_updated_data(raw_data_csv_path,arg_json_file):
  raw_data = read_data(raw_data_csv_path)

  raw_data_updated = clean_data(raw_data,arg_json_file)
  return raw_data_updated


# sample call: python /content/Data_Cleaning.py 'master csv file' 'new csv path' 'args.json' 'newfeatureslist csv path' 
if __name__ == '__main__':
    raw_data_csv_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    arg_json_file = sys.argv[3]
    feature_output_path = sys.argv[4]


    raw_data = read_data(raw_data_csv_path)

    raw_data_updated = clean_data(raw_data,arg_json_file)

    write_features(raw_data_updated,feature_output_path)
    write_data(raw_data_updated,output_csv_path)












