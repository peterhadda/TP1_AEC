from io import StringIO

import pandas as pd

with open("src/sales.html", "r", encoding="utf-8") as f:
    html = f.read()

tables = pd.read_html(StringIO(html))
df = tables[0]

result = df[["Province", "Total Tax Rate"]]
print(result)
