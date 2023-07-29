
from datetime import date, timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

__DEBUG = False

__DEFAULT_LOCATION="4684888"

__locations = [ {"id": "5128581", "name": "New York, United States"},
                {"id": "4684888", "name": "Dallas, United States"},
                {"id": "5419384", "name": "Denver, United States"},
                {"id": "5368361", "name": "Los Angeles, United States"},
                {"id": "1254163", "name": "Thiruvananthapuram, India"},
                {"id": "2643743", "name": "London, United Kingdom"} ]

def get_details(location=__DEFAULT_LOCATION):
    
    return json.dumps(__fetch_data_from_web(date.today(), location))
        
def get_details_for_date(date, location=__DEFAULT_LOCATION):

    return json.dumps(__fetch_data_from_web(date, location))

def __fetch_data_from_web(date, location):

    dataItems = ["Sunrise","Sunset","Nakshathram","Tithi",
                "Rahu Kalam","Gulikai Kalam","Yamaganda"]

    URL_BASE = "https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?"

    URL = URL_BASE + "geoname-id="+ location + "&date="

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

    

    detailDivs = divTamilDate.find_next_siblings("div")

    textTamilDateDetails = ""

    for div in detailDivs:
        textTamilDateDetails += div.text + " "
        
    (response["tamil_date_details"], yugam) = __edit_tamil_date_details(textTamilDateDetails)
    response["last_refresh"] = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")

    response["geo_location"] = location
    response["locations"] = __locations

    response["num_locations"] = len(__locations)

    for item in dataItems:
        item_data = __find_data_web(soup, item)
        
        response[item] = item_data
    
    shaka_samvat = __find_data_web(soup, "Shaka Samvat")
    response["date_tamil"]= divTamilDate.text + ", " + shaka_samvat + ", " + yugam

    return response
        
def __find_data_web(soup, str_type):

    return_text = ""
    results = soup.find(string=str_type).parent

    if results.name != "span":
        results = results.parent

    spans = results.find_next_siblings("span")

    for span in spans:
        return_text += span.text
        
    return return_text

def __edit_tamil_date_details(detail_text):

    idx = detail_text.find("Shaka Samvata")
    
    pos_last_comma = detail_text.rindex(",")
    yugam = detail_text[pos_last_comma + 2:].strip()

    if idx > 0:
        edited_detail_text = detail_text[:idx - 5] + (detail_text[idx + 13:pos_last_comma - 1])
    else:
        edited_detail_text = detail_text

    return (edited_detail_text.strip(), yugam)

if __name__ == "__main__":
  data = get_details()
  print(data)
