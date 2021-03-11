
import matplotlib.pyplot as plt
import pandas as pd
import asyncio
import seaborn as sns
import os
from .csv_functions_pandas import pandas_clean_df_col
from scipy.stats import linregress

async def parse_request(df, method, col1, col2, csv_id):
    if method.lower() == "scatter":
        location = await scatter_plot(df, col1, col2, csv_id)
        return location
    elif method.lower() == "histogram":
        location = await histo_plot(df, col1, col2, csv_id)
        return location

async def scatter_plot(df, col1, col2, csv_id):
    new_df = await pandas_clean_df_col(df, col1)
    new_df = await pandas_clean_df_col(new_df, col2)
    x = new_df[col1]
    y = new_df[col2]
    plt.scatter(x, y)
    plt.xlabel(col1)
    plt.ylabel(col2)
    print(os.getcwd())
    try:
        os.mkdir(os.getcwd() + f"\\graphs\\{str(csv_id)}")
    except FileExistsError:
        pass
    to_save = os.getcwd() + '\\graphs\\' + str(csv_id) + f"\scatter_{col1}_{col2}" + '.png'
    plt.savefig(to_save)
    return to_save

async def histo_plot(df, col1, col2, csv_id):
    try:
        os.mkdir(os.getcwd() + f"\\graphs\\{str(csv_id)}")
    except FileExistsError:
        pass
    new_df = await pandas_clean_df_col(df, col1)
    new_df = await pandas_clean_df_col(df, col2)
    x = new_df[col1]
    y = new_df[col2]
    sns_plot = sns.histplot(data=pd.DataFrame({
        col1: x,
        col2:y
    }), bins=20, alpha=0.2, kde=True)
    to_save = os.getcwd() + '\\graphs\\' + str(csv_id) + f"\hist_{col1}_{col2}" + '.png'
    plt.savefig(to_save)
    return to_save
