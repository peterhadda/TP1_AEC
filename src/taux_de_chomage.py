import re
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "http://roberthalf.com/ca/en/insights/research/november-2025-labour-force-survey#:~:text=The%20latest%20Statistics%20Canada%20Labour,2025%20compared%20to%20November%202024."

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
page_text=soup.get_text("",strip=True)
pattern = r"(British Columbia|Alberta|Saskatchewan|Manitoba|Ontario|Quebec|New Brunswick|Prince Edward Island|Nova Scotia|Newfoundland and Labrador):\s*([\d.]+)\s*per cent"


matches=re.findall(pattern,page_text)

provinces=[]

for province,rate in matches:
    provinces.append({"provinces":province,"rate":rate})

