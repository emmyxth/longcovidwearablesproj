import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

file_path = "/labs/mpsnyder/long-covid-study-data/additional_src_files"
os.chdir(file_path)

id_mapping = pd.read_csv(os.path.join(file_path, "idmapping.csv"))
metadata = pd.read_csv(os.path.join(file_path, "covid_metadata.csv"))

df_new = pd.DataFrame()
for index, row in metadata.iterrows():
    id = str(row["numeric_id"])
    df = id_mapping[id_mapping["id"] == id]
    if not df.empty:
        df_new = df_new.append(df)