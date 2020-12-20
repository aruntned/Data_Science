# Data_Science

Update1:
A simple work on using Data Science libraries.
Added jupyter/colab notebook to 
1) perform EDA on a csv file.
2) clean the master table by converting data from categorical to numerical, Y/N to binary and removing unwanted columns.
3) Create and train an XGBoost model in GPU.


Update 2:
Added python scripts to clean data and get predictions from cleaned data using a saved xgboost model in pkl format.

Using DataCleaner and Predictor:

We have two files DataCleaner and Predictor that can be used to directly use data and receive cleaned data and predictions as output.

A. DataCleaner:

In the DataCleaner folder, we have Data_Cleaning.py that can be used such that once we input raw data as input with a json file with arguments, we get cleaned data as output and list of features in updated data.

We have 5 keys in json file that can be filled as needed. 
Primary_id: can be filled with primary key of data
Column_name: one of the columns to be converted to ohe (same column not included in columns_ohe)
Columns_drop: filled with columns to be dropped from raw data
Columns_ohe: columns to be converted to OHE
Columns_01: columns that have Y,N values to be converted to 0/1
Columns_drop_corr: additional columns to be dropped 

We can call the python file as:

python /content/Data_Cleaning.py 'master csv file' 'new csv path' 'args.json' 'newfeatureslist csv path'

Here we have four arguments:

Arg1: raw data to be cleaned (input)
Arg2: updated data after cleaning in zip (output)
Arg3: json file with arguments (input)
Arg4: features of updated data (output)

B. Predictor:

We have a Predictor folder with trained XGBoost predictor. In this folder there are 2 items. The saved xgboost model in pkl format (xgb_model.pkl) and python code to run the model (Xgboost_predictor).

We run the model as shown below:

python  /content/Xgboost_predictor.py 'cleaneddatapath in zip' 'new csv name' 'output:predictions path' 'load model path' 'target column name'

We have five arguments for the code:

Arg1: path of cleaned data in zip format (input)
Arg2: name of cleaned data csv file (input)
Arg3: Output predictions after using model (output)
Arg4: path of saved xgboost model (input)
Arg5: Target column name (input)

Note 1: Please note that for using cleaner functionalities, the raw data used for data cleaning should be similar to data used initially and if data used is different then the json file needs to be adjusted.
Note 2: Please note that for using predictor functionalities, the cleaned data columns should be same as that we get after passing through cleaner function. Any additional columns or lack of columns will lead to errors.
