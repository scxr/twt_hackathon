import pandas as pd
from pandas.core.frame import DataFrame

async def pandas_clean_df_col(df: pd.DataFrame, column):
    df[column] = df[column].str.extract('(\d+)', expand=False)    
    df[column] = df[column].apply(lambda x: float(x))
    return df

async def pandas_get_column_names(df:pd.DataFrame) -> list:
    return df.columns

async def pandas_get_column_mean(df:pd.DataFrame, column:str) -> float:
    clean_df = await pandas_clean_df_col(df, column)
    return clean_df[column].mean()

async def pandas_get_column_median(df:pd.DataFrame, column:str) -> float:
    clean_df = await pandas_clean_df_col(df, column)
    return clean_df[column].median()

async def pandas_get_column_mode(df:pd.DataFrame, column:str) -> float:
    clean_df = await pandas_clean_df_col(df, column)
    return clean_df[column].mode()

async def pandas_get_max(df:pd.DataFrame, column:str) -> int:
    clean_df = await pandas_clean_df_col(df, column)
    max_pos = clean_df[column].argmax()
    max_val = clean_df[column].loc(max_pos)
    return max_pos, max_val

async def pandas_get_min(df:pd.DataFrame, column:str) -> int:
    clean_df = await pandas_clean_df_col(df, column)
    min_pos = clean_df[column].argmin()
    min_val = clean_df[column].loc(min_pos)
    return min_pos, min_val