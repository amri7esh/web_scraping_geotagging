import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

#------------------ CONFIGURATION -------------------------------

# Set your output file name here.
output_filename = 'state_private_universities.csv'
# Set your input file here
input_filename = "universities_input.csv"
# Specify the column name in your input data that contains addresses here
state_id_column = "state_id"
state_name_column = "state_name"
universities_state_list_column = "state_priv_univ_state_ids"

#------------------ DATA LOADING --------------------------------

# Read the data to a Pandas Dataframe
data = pd.read_csv(input_filename, encoding='utf8')

if state_id_column not in data.columns:
	raise ValueError("Missing State ID column in input data")
if state_name_column not in data.columns:
	raise ValueError("Missing State Name column in input data")
if universities_state_list_column not in data.columns:
	raise ValueError("Missing list of universities state ids in input data")

# Form a list of Affiliation Number for Scrapping
# Make a big list of all of the Affiliation Number to be processed.
state_ids = data[state_id_column].tolist()
state_names = data[state_name_column].tolist()
univ_state_ids = [int(x) for x in data[universities_state_list_column].tolist() if str(x) != 'nan']
# univ_state_ids = [7, 29]

state = {}
for i in range(0,len(state_ids)):
    state[state_ids[i]] = state_names[i]

#------------------	FUNCTION DEFINITIONS ------------------------

def get_contact_info(c_url):
    URL = c_url
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
    return output

# Set up your State University data scrapping URL:

def get_state_university_data(state_id):
    URL = "https://www.ugc.ac.in/privateuniversitylist.aspx?id={}&Unitype=3".format(state_id)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    output = []
    for tr in soup.findAll('tr')[2:]:
        univ_data = {}
        univ_data['state_id'] = state_id
        for a in tr.findAll('td')[1].findAll('a'):
            if a.text.strip() == "More Details...":
                c_url = "https://www.ugc.ac.in/"+a.get('href')
                contact_data = get_contact_info(c_url)
                univ_data.update(contact_data)
                univ_data['university_id'] = a.get('href')[a.get('href').find("=")+1:]
        output.append(univ_data)
    return output

#------------------ PROCESSING LOOP -----------------------------

# Create a list to hold results
results = []
count = 0

# Go through each Affiliation Number in turn
for state_id in univ_state_ids:
    # While the affiliation data scraping is not finished:
    scraped = False
    while scraped is not True:
        # Scrap the Data From CBSE
        try:
            state_university_data = get_state_university_data(state_id)
        except Exception as e:
            logger.exception(e)
            logger.error("Major error with {}".format(state[state_id]))
            logger.error("Skipping!")
            scraped = True

        logger.debug("Scrapped State: {} data and returned data for : {} universities".format(state[state_id], len(state_university_data)))
        results.extend(state_university_data)
        scraped = True

    # Print status every 100 addresses
    count=count+1
    logger.info("Completed {} of {} states".format(count, len(univ_state_ids)))

    # Every 500 addresses, save progress to file(in case of a failure so you have something!)
    pd.DataFrame(results).to_csv("{}_bak".format(output_filename))

# All done
logger.info("Finished scraping all States Data")
# Write the full results to csv using the pandas library.
pd.DataFrame(results).to_csv(output_filename, encoding='utf8')
