import pandas as pd

url = "https://www150.statcan.gc.ca/n1/daily-quotidien/250722/t003a-eng.htm"

df = pd.read_html(url)[0]

df_columns = [
    "_".join([str(x) for x in col if str(x) != "nan"]).strip("_")
    if isinstance(col, tuple) else str(col)
    for col in df.columns
]

df.columns = df_columns

df = df.rename(columns={df.columns[0]: "province"})

df = df[df["province"] != "Canada"]

severity_cols = [col for col in df.columns if "severity" in col.lower()]

if not severity_cols:
    raise ValueError("No severity index column found in crime_rate source table")

severity_col = severity_cols[0]

df_final = df[["province", severity_col]].rename(columns={severity_col: "severity_index"})
