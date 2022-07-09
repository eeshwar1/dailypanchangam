import tkinter as tk
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

class Panchangam(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
       tk.Tk.__init__(self, *args, **kwargs)
       
       self.geometry("760x360")
       self.date = date.today()
       
       self.container = dayFrame(self, self.date)

       self.container.grid(row=1,column=1,columnspan=4)
       
       self.title("Daily Panchangam")
       self.resizable(False, False) # disable resizing
    
       frmBtnPrev = tk.Frame(master=self, borderwidth=1)
       frmBtnPrev.grid(row=8,column=1,padx=5, pady=5, sticky=tk.W)
       btnPrev = tk.Button(master=frmBtnPrev, text="<", command=self.showPrevDate)
       btnPrev.pack()
       
       frmBtnToday = tk.Frame(master=self, borderwidth=1)
       frmBtnToday.grid(row=8,column=3,padx=5, pady=5, sticky=tk.W)
       btnToday = tk.Button(master=frmBtnToday, text="Today", command=self.showToday)
       btnToday.pack()
       
       frmBtnNext = tk.Frame(master=self, borderwidth=1)
       frmBtnNext.grid(row=8,column=4,padx=5, pady=5, sticky=tk.E)
       btnNext = tk.Button(master=frmBtnNext, text=">", command=self.showNextDate)
       btnNext.pack()
        
        
    def showPrevDate(self):
        
        self.date -= timedelta(days = 1)
        
        self.container.set_date(self.date)
       
        return

    def showNextDate(self):
        
        self.date += timedelta(days = 1)
     
        self.container.set_date(self.date)
        
        return
    
    def showToday(self):
        
        self.date = date.today()
        
        self.container.set_date(self.date)
        
        return
    
class dayFrame(tk.Frame):

    frmDate = None
    lblDate = None
    
    frmTamilDate = None
    lblTamilDate = None
    
    frmTamilDateDetails = None
    lblTamilDateDetails = None
   
    dataItems = ["Sunrise","Sunset","Nakshathram","Tithi",
                 "Rahu Kalam","Gulikai Kalam","Yamaganda"]
    dataValues = []
    dataLabels = []
    
    def __init__(self, parent, day):
        
        tk.Frame.__init__(self, parent)
        
        self.date = day
        
        self.frames = []
        
        self.show_fields()
        
        self.fetch_data()
        
        self.show_data()
        
        
    def show_fields(self):
        
        self.grid_columnconfigure(0, minsize=40, weight=1)
        self.grid_columnconfigure(1, minsize=250, weight=1)
        
        self.grid_columnconfigure(2, minsize=40, weight=1)
        self.grid_columnconfigure(3, minsize=250, weight=1)
        
        self.grid_rowconfigure(4, minsize=30, weight=1)
        
        self.grid_rowconfigure(5, minsize=50, weight=1)
        self.grid_rowconfigure(6, minsize=30, weight=1)
        self.grid_rowconfigure(7, minsize=20, weight=1)
        
        textCurrentDate = "Date"
        textTamilDate = "Tamil Date"
        textTamilDateDetails = "Tamil Date Details"
        
        frmDate = tk.Frame(master=self)
        frmDate.grid(row=0,column=0, columnspan=4, padx=5, pady=5)
        lblDate =  tk.Label(master=frmDate,text=textCurrentDate, justify=tk.LEFT)
        lblDate.config(font=("Helvetica",40))
        lblDate.pack()
        
        self.lblDate = lblDate

        frmTamilDate = tk.Frame(master=self)
        frmTamilDate.grid(row=1,column=0, columnspan=4, padx=5, pady=5)
        lblTamilDate =  tk.Label(master=frmTamilDate,text=textTamilDate, justify=tk.LEFT)
        lblTamilDate.config(font=("Helvetica",20))
        lblTamilDate.pack()
        
        self.lblTamilDate = lblTamilDate

        frmTamilDateDetails = tk.Frame(master=self)
        frmTamilDateDetails.grid(row=2,column=0, columnspan=4, padx=5, pady=5)
        lblTamilDateDetails =  tk.Label(master=frmTamilDateDetails,text=textTamilDateDetails, justify=tk.LEFT)
        lblTamilDateDetails.config(font=("Helvetica",16))
        lblTamilDateDetails.pack()
        
        self.lblTamilDateDetails = lblTamilDateDetails
        
        row_num=3
        col_num=-1
        
        for item in self.dataItems:
                  
            col_num += 1
            frmItem = tk.Frame(master=self,relief=tk.FLAT,borderwidth=1)
            frmItem.grid(row=row_num,column=col_num, padx=5, pady=5, sticky=tk.W)
            lblItem = tk.Label(master=frmItem,text=item, justify=tk.LEFT, wraplength=120)
            lblItem.config(font="Helvetica 12 bold") 
            lblItem.pack()
            
            col_num += 1
            frmItemData = tk.Frame(master=self,relief=tk.FLAT,borderwidth=1)
            frmItemData.grid(row=row_num,column=col_num, padx=5, pady=5, sticky=tk.W)
            lblItemData = tk.Label(master=frmItemData,text="", justify=tk.LEFT, wraplength=250)
            lblItemData.config(font="Helvetica 12") 
            lblItemData.pack()
            
            self.dataLabels.append(lblItemData)
            
            if col_num == 3:
                row_num += 1
                col_num = -1
            
    def set_date(self,date):
        
        self.date = date
        self.fetch_data_for_date(date)
        self.show_data()
        
    def fetch_data(self):
        
        self.fetch_data_for_date(self.date)
        
    def fetch_data_for_date(self, date):
        
        dateValue = date.strftime("%d/%m/%Y")
        
        URL = "https://www.drikpanchang.com/tamil/tamil-month-panchangam.html?geoname-id=4684888&date=" + dateValue

        page = requests.get(URL)

        self.soup = BeautifulSoup(page.content, "html.parser")
        
        self.textCurrentDate = self.date.strftime("%a %b %d, %Y")
        
        divTamilDate = self.soup.find("div", {"class": "dpPHeaderLeftTitle"})

        self.textTamilDate = divTamilDate.text

        detailDivs = divTamilDate.find_next_siblings("div")

        self.textTamilDateDetails = ""

        for div in detailDivs:
            self.textTamilDateDetails += div.text + " "
        
        self.dataValues = []
        
        for item in self.dataItems:
            item_data = self.find_data(item)
            self.dataValues.append(item_data)
                
    def find_data(self, str_type):
    
        return_text = ""
        results = self.soup.find(text=str_type).parent
        
        if results.name != "span":
            results = results.parent

        spans = results.find_next_siblings("span")

        for span in spans:
            return_text += span.text
            
        return return_text


    def show_data(self):
        
        self.lblDate.configure(text=self.textCurrentDate)
        self.lblTamilDate.configure(text=self.textTamilDate)
        self.lblTamilDateDetails.configure(text=self.textTamilDateDetails)
                            
        for idx, item in enumerate(self.dataItems):
        
            self.dataLabels[idx].configure(text=self.dataValues[idx])
        
            
app = Panchangam()
app.mainloop()
