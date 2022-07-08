import requests
from bs4 import BeautifulSoup
import tkinter as tk
from datetime import date

def find_data(str_type):
    
    return_text = ""
    results = soup.find(text=str_type).parent
       
    if results.name != "span":
        results = results.parent

    spans = results.find_next_siblings("span")

    for span in spans:
        return_text += span.text
        
    return return_text

def showPrevDate():
    print("Prev Date")
    
    return


def showNextDate():
    print("Next Date")
    
    return

# URL = "https://www.drikpanchang.com/panchang/month-panchang.html?geoname-id=4684888&date=07/07/2022"

today = date.today().strftime("%d/%m/%Y")

URL = "https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?date=" + today

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

textCurrentDate = soup.find("h2").text

data_items = ["Sunrise","Sunset","Nakshathram","Tithi","Rahu Kalam","Gulikai Kalam","Yamaganda"]
# data_values = []

app = tk.Tk()
app.title("Daily Panchangam")
app.resizable(False, False)

divTamilDate = soup.find("div", {"class": "dpPHeaderLeftTitle"})

textTamilDate = divTamilDate.text

detailDivs = divTamilDate.find_next_siblings("div")

textTamilDateDetails = ""

for div in detailDivs:
    textTamilDateDetails += div.text + " "
                     
#print(textTamilDate)
#print(textTamilDateDetails)

frmDate = tk.Frame(master=app)
frmDate.grid(row=1,column=1, columnspan=4, padx=5, pady=5)
lblDate =  tk.Label(master=frmDate,text=textCurrentDate)
lblDate.config(font=("Helvetica",40))
lblDate.pack()

frmTamilDate = tk.Frame(master=app)
frmTamilDate.grid(row=2,column=1, columnspan=4, padx=5, pady=5)
lblTamilDate =  tk.Label(master=frmTamilDate,text=textTamilDate)
lblTamilDate.config(font=("Helvetica",22))
lblTamilDate.pack()

frmTamilDateDetails = tk.Frame(master=app)
frmTamilDateDetails.grid(row=3,column=1, columnspan=4, padx=5, pady=5)
lblTamilDateDetails =  tk.Label(master=frmTamilDateDetails,text=textTamilDateDetails)
lblTamilDateDetails.config(font=("Helvetica",16))
lblTamilDateDetails.pack()

row_num=4
col_num=0

for item in data_items:
    item_data = find_data(item)
    # data_values.append(find_data(item))
    
    col_num += 1
    frmItem = tk.Frame(master=app,relief=tk.FLAT,borderwidth=1)
    frmItem.grid(row=row_num,column=col_num, padx=5, pady=5)
    lblItem = tk.Label(master=frmItem,text=item)
    lblItem.config(font="Helvetica 12 bold") 
    lblItem.pack()
    
    col_num += 1
    frmItemData = tk.Frame(master=app,relief=tk.FLAT,borderwidth=1)
    frmItemData.grid(row=row_num,column=col_num, padx=5, pady=5)
    lblItemData = tk.Label(master=frmItemData,text=item_data)
    lblItemData.config(font="Helvetica 12") 
    lblItemData.pack()
    
    # row_num += 1
    if col_num == 4:
        row_num += 1
        col_num = 0
    
frmBtnPrev = tk.Frame(master=app)
frmBtnPrev.grid(row=8,column=1,padx=5, pady=5)
btnPrev = tk.Button(master=frmBtnPrev, text="<", command=showPrevDate)
btnPrev.pack()

frmBtnNext = tk.Frame(master=app)
frmBtnNext.grid(row=8,column=2,padx=5, pady=5)
btnNext = tk.Button(master=frmBtnNext, text=">", command=showNextDate)
btnNext.pack()


# print(data_values)
app.mainloop()

  





