import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

URL = "https://www.ugc.ac.in/uni_contactinfo.aspx?id=49"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.findAll('table')

output = {}

output['Name'] = soup.findAll('font')[0].find('b').text.strip()
output['Full Address'] = soup.findAll('font')[1].text.strip()
tr = table[1].findAll('tr')
u_contact = tr[0].findAll('td')[2].text.strip().split('\n')
vc_contact = tr[1].findAll('td')[2].text.strip().split('\n')
r_contact = tr[2].findAll('td')[2].text.strip().split('\n')

output['univ_phone'] = re.sub('Phone No:','',u_contact[0]).strip()
output['univ_email'] = re.sub('E-mail:','',u_contact[1]).strip()
output['univ_website'] = re.sub('Website:','',u_contact[2]).strip()

output['vc_name'] = re.sub('VC Name:','',vc_contact[0]).strip()
v_ph_r = vc_contact[1].find('Phone No (R):')
v_fax = vc_contact[1].find('Fax No:')
v_mob = vc_contact[1].find('Mob No:')
output['vc_phone(o)'] = re.sub('Phone No O:',"",re.sub(r'[\(\)]','',vc_contact[1][:v_ph_r])).strip()
output['vc_phone(r)'] = re.sub('Phone No R:',"",re.sub(r'[\(\)]','',vc_contact[1][v_ph_r:v_fax])).strip()
output['vc_fax'] = re.sub("Fax No:",'',vc_contact[1][v_fax:v_mob]).strip()
output['vc_mobile'] = re.sub('\s+',' ',re.sub(",",", ",re.sub("Mob No:",'',vc_contact[1][v_mob:]))).strip()
output['vc_email'] = re.sub('E-mail:','',vc_contact[2]).strip()

output['reg_name'] = re.sub('Reg. Name:','',r_contact[0]).strip()
r_ph_r = r_contact[1].find('Phone No (R):')
r_fax = r_contact[1].find('Fax No:')
r_mob = r_contact[1].find('Mob No:')
output['reg_phone(o)'] = re.sub('Phone No O:',"",re.sub(r'[\(\)]','',r_contact[1][:r_ph_r])).strip()
output['reg_phone(r)'] = re.sub('Phone No R:',"",re.sub(r'[\(\)]','',r_contact[1][r_ph_r:r_fax])).strip()
output['reg_fax'] = re.sub("Fax No:",'',r_contact[1][r_fax:r_mob]).strip()
output['reg_mobile'] = re.sub('\s+',' ',re.sub(",",", ",re.sub("Mob No:",'',r_contact[1][r_mob:]))).strip()
output['reg_email'] = re.sub('E-mail:','',r_contact[2]).strip()
print(output)
