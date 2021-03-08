import pandas as pd

df = pd.read_csv('upload_files/120022.csv')


df["Value"] = df["Value"].str.extract('(\d+)', expand=False)
 
        
df["Value"] = df["Value"].apply(lambda x: float(x))
print(df["Value"].median())
