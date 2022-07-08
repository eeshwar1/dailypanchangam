import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import tkinter as tk

def find_data(str_type):
    
    return_text = ""
    results = soup.find(text=str_type).parent
       
    if results.name != "span":
        results = results.parent

    spans = results.find_next_siblings("span")

    for span in spans:
        return_text += span.text
        
    return return_text

URL = "https://www.drikpanchang.com/panchang/month-panchang.html?geoname-id=4684888&date=07/07/2022"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

textCurrentDate = soup.find("h2").text

data_items = ["Sunrise","Sunset","Nakshatra","Tithi","Rahu Kalam","Gulikai Kalam","Yamaganda"]
data_values = []

app = tk.Tk()
app.title("Daily Panchangam")

frmDate = tk.Frame(master=app)
frmDate.grid(row=1,column=1, columnspan=4)
lblDate =  tk.Label(master=frmDate,text=textCurrentDate)
lblDate.config(font=("Helvetica",44))
lblDate.pack()

row_num=2
col_num=0

for item in data_items:
    item_data = find_data(item)
    data_values.append(find_data(item))
    
    col_num += 1
    frmItem = tk.Frame(master=app,relief=tk.FLAT,borderwidth=1)
    frmItem.grid(row=row_num,column=col_num)
    lblItem = tk.Label(master=frmItem,text=item)
    lblItem.config(font="Helvetica 10 bold") 
    lblItem.pack()
    
    col_num += 1
    frmItemData = tk.Frame(master=app,relief=tk.FLAT,borderwidth=1)
    frmItemData.grid(row=row_num,column=col_num)
    lblItemData = tk.Label(master=frmItemData,text=item_data)
    lblItemData.pack()
    
    # row_num += 1
    if col_num == 4:
        row_num += 1
        col_num = 0
    
    
        
print(data_values)
app.mainloop()

  





