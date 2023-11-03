import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


URL = "https://www.ugc.ac.in/uni_faculty.aspx?id=45"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
tr = soup.find('table').findAll("tr")[2:]
print(len(tr))

output = {}
for row in tr:
    col = row.findAll("td")
    output[re.sub(":","",col[0].text.strip()).strip()] = col[1].text.strip()

print(output)
