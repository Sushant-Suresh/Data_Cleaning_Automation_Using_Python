# Importing Required Libraries:
import pandas as pd
import numpy as np
import os

try:
    import openpyxl
    import xlrd
except ImportError:
    print("Make sure 'openpyxl' and 'xlrd' are installed to handle .xlsx files")

def data_cleaner(data_path, data_name):
    # Checking if Path Exists:
    if not os.path.exists(data_path):
        print('Error: The specified path does not exist. Please enter the correct path.')
        return

    # Loading the Dataset:
    if data_path.endswith('.csv'):
        print('Dataset provided is in .csv format')
        data = pd.read_csv(data_path, encoding_errors = 'ignore')
    elif data_path.endswith('.xlsx'):
        print('Dataset provided is in .xlsx format')
        data = pd.read_excel(data_path)
    else:
        print('Error: File type not supported! Only .csv and .xlsx are supported.')
        return

    # Displaying Initial Rows and Columns:
    print(f'Total Rows: {data.shape[0]}\nTotal Columns: {data.shape[1]}')

    # Checking for Duplicate Records & Saving them in a .CSV File:
    total_duplicates = data.duplicated().sum()
    print(f'Dataset has {total_duplicates} duplicate records')
    if total_duplicates > 0:
        duplicate_records = data[data.duplicated()]
        duplicate_records.to_csv(f'{data_name}_duplicates.csv', index = False)
        print(f'Duplicate records saved as {data_name}_duplicates.csv')

    # Removing Duplicates:
    df = data.drop_duplicates()

    # Checking for NULL Values:
    total_missing_values = df.isnull().sum().sum()
    missing_value_columns = df.isnull().sum()
    print(f'Dataset has {total_missing_values} missing values')
    print(f'Missing values per column:\n{missing_value_columns}')

    # Filling or Dropping NULL Values:
    for col in df.columns:
        if df[col].dtype in (float, int):
            df.loc[:, col] = df[col].fillna(df[col].mean())  # Fill numeric columns with mean
        else:
            df.dropna(subset = [col], inplace = True)  # Drop rows with missing values in non-numeric columns

    # Saving the Cleaned Data:
    print(f'Your Dataset is cleaned. It now has {df.shape[0]} rows & {df.shape[1]} columns')
    df.to_csv(f'{data_name}_clean_data.csv', index = False)
    print(f'Cleaned dataset saved as {data_name}_clean_data.csv')

if __name__ == '__main__':
    data_path = input('Please enter dataset path: ')
    data_name = input('Please enter dataset name: ')
    
    # Calling the Function:
    data_cleaner(data_path, data_name)
