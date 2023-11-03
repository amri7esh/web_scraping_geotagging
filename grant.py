import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


URL = "https://www.ugc.ac.in/uni_grantinfo.aspx?id=46"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

output = {}

output['new_plan_period'] = soup.find('span', id="lblplanperiod").text.strip()
output['new_plan_as_on_date'] = soup.find('span', id="lblasondate1").text.strip()
output['N_Grant_Allocation (in Rs. Lacs)'] = soup.find('span', id="lblgrantallocation1").text.strip()
output['N_Grant Released (in Rs. Lacs)'] = soup.find('span', id="lblgrantrelease1").text.strip()
output['N_UC Amount (in Rs. Lacs)'] = soup.find('span', id="lblucamount1").text.strip()
output['N_Additional Grant Allocation (in Rs. Lacs)'] = soup.find('span', id="lblgrantallocation2").text.strip()
output['N_Additional Grant Released (in Rs. Lacs)'] = soup.find('span', id="lblgrantrelease2").text.strip()
output['N_Additional UC Amount (in Rs. Lacs)'] = soup.find('span', id="lblucamount2").text.strip()
output['N_Total Grant Allocation (in Rs. Lacs)'] = soup.find('span', id="lblgrantallocation3").text.strip()
output['N_Total Grant Released (in Rs. Lacs)'] = soup.find('span', id="lblgrantrelease3").text.strip()
output['N_Total UC Amount (in Rs. Lacs)'] = soup.find('span', id="lblucamount3").text.strip()

output['old_plan_period'] = soup.find('span', id="lblplan_priod").text.strip()
output['old_plan_as_on_date'] = soup.find('span', id="lblasondate").text.strip()
output['O_Grant Allocation (Under all Schemes) (in Rs. Lacs)'] = soup.find('span', id="lblgrantallocation").text.strip()
output['O_Grant Released (in Rs. Lacs)'] = soup.find('span', id="lblgrantrelease").text.strip()
output['O_UC Amount (in Rs. Lacs)'] = soup.find('span', id="lblucamount").text.strip()

print(output)
