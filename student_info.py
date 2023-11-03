import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


URL = "https://www.ugc.ac.in/uni_stuinfo.aspx?id=47"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.findAll('table')


output = {}
for row in table[1].findAll("tr"):
    col = row.findAll("td")
    for i in range (0,len(col)-1,2):
        output[re.sub(":","",col[i].text.strip()).strip()] = col[i+1].text.strip()

print(output)
