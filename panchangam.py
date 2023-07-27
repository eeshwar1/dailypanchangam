
from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

DEBUG = False

def get_details():
    
    return json.dumps(fetch_data_from_web(date.today()))
        
def get_details_for_date(date):

    return json.dumps(fetch_data_from_web(date))

def fetch_data_from_web(date):

    dataItems = ["Sunrise","Sunset","Nakshathram","Tithi",
                "Rahu Kalam","Gulikai Kalam","Yamaganda"]

    URL = "https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?geoname-id=4684888&date="

    dateValue = date.strftime("%d/%m/%Y")

    dateStr = date.strftime("%Y-%m-%d")

    response = {}

    URL_string = URL + dateValue

    try: 
        page = requests.get(URL_string)
    except requests.exceptions.Timeout:
        sleep(1)
        page = requests.get(URL_string)
        

    soup = BeautifulSoup(page.content, "html.parser")

    response["str_date"] = dateStr

    response["date_text"] = date.strftime("%a %b %d, %Y")

    prevDate = date - timedelta(days = 1)
    nextDate = date + timedelta(days = 1)

    response["prev_date_text"] = prevDate.strftime("%a %b %d, %Y")
    response["next_date_text"] = nextDate.strftime("%a %b %d, %Y")


    divTamilDate = soup.find("div", {"class": "dpPHeaderLeftTitle"})

    response["date_tamil"]= divTamilDate.text

    detailDivs = divTamilDate.find_next_siblings("div")

    textTamilDateDetails = ""

    for div in detailDivs:
        textTamilDateDetails += div.text + " "
        
    response["tamil_date_details"] = textTamilDateDetails
    response["refreshed_date"] = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")

    for item in dataItems:
        item_data = find_data_web(soup, item)
        
        response[item] = item_data
        
    return response
            
def find_data(soup, str_type):

    return_text = ""
    results = soup.find(text=str_type).parent

    if results.name != "span":
        results = results.parent

    spans = results.find_next_siblings("span")

    for span in spans:
        return_text += span.text
        
    return return_text

        
def find_data_web(soup, str_type):

    return_text = ""
    results = soup.find(string=str_type).parent

    if results.name != "span":
        results = results.parent

    spans = results.find_next_siblings("span")

    for span in spans:
        return_text += span.text
        
    return return_text


if __name__ == "__main__":
  data = fetch_data_from_web(date.today())
  print(data)
