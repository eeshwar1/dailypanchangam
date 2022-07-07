import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import tkinter as tk

URL = "https://www.drikpanchang.com/panchang/month-panchang.html?geoname-id=4684888&date=06/07/2022"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

current_date_txt = soup.find("h2").text

data_items = ["Sunrise","Sunset","Nakshatra","Tithi","Rahu Kalam","Gulikai Kalam","Yamaganda"]

window = tk.Tk()
greeting =  tk.Label(text=current_date_txt)
greeting.pack()


def find_data(str_type):
    
    return_text = ""
    results = soup.find(text=str_type).parent
       
    if results.name != "span":
        results = results.parent

    spans = results.find_next_siblings("span")

    for span in spans:
        return_text += span.text
        
    return return_text


for item in data_items:
    #print(item + " " + find_data(item))
    data_lbl = item + " " + find_data(item)
    label = tk.Label(text=data_lbl)
    label.pack()
    
    
window.mainloop()
  





