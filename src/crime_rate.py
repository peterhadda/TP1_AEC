import pandas as pd
url="https://www150.statcan.gc.ca/n1/daily-quotidien/250722/t003a-eng.htm"

df=pd.read_html(url)[0]

df_columns=[
    "_".join([str(x) for x in col if str(x)!="nan"]).strip("_")
    if isinstance(col,tuple) else str(col)
    for col in df.columns
]

df=df.rename(columns={df.columns[0]:"province"})

df=df[df["province"] !="Canada"]

crime_rate=[col for col in df.columns if "rate" in col.lower()]

crime_rate_col=crime_rate[0]

df_final=df[['province',crime_rate_col]]

df_final=df_final.rename(columns={crime_rate_col:"crime_rate"})

