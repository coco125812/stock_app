import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_date_range(option):
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    if option == '7':
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    elif option == '30':
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    elif option == '365':
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    else:
        raise ValueError("Invalid option. Please provide a valid integer for days, months, or years.")
    
    return start_date, end_date

def validate_positive_int(value):
    try:
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError("Value must be a positive integer.")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid input. Please provide a valid integer.")

def get_info(dataframe):
    stock_info = pd.DataFrame({
                       'Datatype' : dataframe.dtypes,
                       'Total_Element': dataframe.count(),
                       'Null_Count': dataframe.isnull().sum(),
                       'Null_Percentage': dataframe.isnull().sum()/len(dataframe) * 100
                           })
    return stock_info
