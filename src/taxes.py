from io import StringIO

import pandas as pd
from config import CONFIG

sales_path = CONFIG["raw_dir"] / "sales.html"

with open(sales_path, "r", encoding="utf-8") as f:
    html = f.read()

tables = pd.read_html(StringIO(html))
df = tables[0]

result = df[["Province", "Total Tax Rate"]]

