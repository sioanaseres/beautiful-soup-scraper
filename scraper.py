import requests
from bs4 import BeautifulSoup
import csv
import re
import time

NAME = "Test"
EMAIL = "test@gmail.com"
HEADERS = { "User-Agent" : f"{NAME} ({EMAIL})"}
BASE_URL = 'https://ariannedee.pythonanywhere.com'
URL = BASE_URL +'/Member_states_of_the_United_Nations'
SECS = 1

def run_scraper():
  
  soup = get_soup_from_url(URL)
  countries = list(get_country_dicts(soup))
  
  for country_dict in countries[:3]:
    get_country_detail_data(country_dict)
    time.sleep(SECS)

  write_to_csv(countries)

def get_soup_from_url(url):
  response  = requests.get(url, headers=HEADERS, verify=False)
  assert response.status_code == 200, f"Response was {response.status_code} for {url}"
  html_doc = response.text
  return BeautifulSoup(html_doc, "html.parser")

def get_country_dicts(soup):
  table= soup.find("table", class_="wikitable")

  countries = []
  for row in table.find_all("tr"):
    
    if row.td:
      country_data = {}
      tds = row.find_all("td")
      links = tds[0].find_all("a")
      country_name = links[1].string
      # countries.append(country_name)
      url = BASE_URL + links[1]['href']
        
      date_joined = tds[1].span.string
      country_data = {
        "Name" : country_name, 
        "Date Joined" : date_joined,
        "URL" : url
      }
      
      countries.append(country_data)
  return countries
       
  
def get_country_detail_data(country_dict):
    soup = get_soup_from_url(country_dict["URL"])
    table = soup.find("table", class_="geography")
    
    def get_detail_data(table, name):
      tr_header = table.find('tr', string=re.compile(name) )
      data_text = tr_header.next_sibling.td.text
      data = data_text.split()[0].split("[")[0]
      return data
  
    country_dict["Area"] = get_detail_data(table, "Area")
    country_dict["Population"] = get_detail_data(table, "Population")   
    
    
def write_to_csv(country_dicts):
  with open("countries.csv", "w", encoding='utf-8', newline="" ) as file:
    fieldnames = ["Name", "Date Joined", "Area", "Population"]
    writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(country_dicts)


      
if __name__== "__main__":
  run_scraper()    
  
  
  
  # with open("countries.txt", "w", encoding='utf-8') as file:
  #   for country in countries:
  #     file.write(f"{country}\n")  
  