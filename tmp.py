import pandas as pd
import numpy as np
df = pd.read_csv('upload_files/120022.csv')
print(np.count_nonzero(df.duplicated()))
