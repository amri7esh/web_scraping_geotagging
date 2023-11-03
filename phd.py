import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


URL = "https://www.ugc.ac.in/uni_phd.aspx?id=46"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
tr = soup.find('tbody').findAll("tr")[1:]

output = {}

output['Total No of M.Phils Awarded'] = tr[0].findAll("td")[1].text.strip()
output['Total No of Ph.Ds Awarded'] = tr[1].findAll("td")[1].text.strip()
output['mphil_phd_as_on_date'] = tr[2].find("td").find('b').text.strip()

print(output)
