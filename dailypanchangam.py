#!/usr/bin/python3.11
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
from datetime import date, timedelta, datetime
from threading import Timer
import time

import json

from panchangam import panchangam

DEBUG = False
            

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        
        
class PanchangamView(tk.Tk):
    
    def stop_refresh_timer(self):
        
        self.rt.stop()
        self.destroy()
    
    def __init__(self, *args, **kwargs):
        
       tk.Tk.__init__(self, *args, **kwargs)
       
       self.date = date.today()
       
       self.set_font_sizes()
       
       self.showing_today = True
       
       self.container = dayFrame(self, self.date, self.size_ratio)

       self.container.grid(row=1,column=1,columnspan=4)
       
       self.title("Daily Panchangam")
       self.resizable(False, False) # disable resizing
    
       frmBtnPrev = tk.Frame(master=self, borderwidth=1)
       frmBtnPrev.grid(row=8,column=1,padx=5, pady=5, sticky=tk.W)
       btnPrev = tk.Button(master=frmBtnPrev, text="<", command=self.showPrevDate, height=1, width=3)
       btnPrev.config(font=("Helvetica Bold", int(12 * self.size_ratio)))
       btnPrev.pack()
       
       frmBtnToday = tk.Frame(master=self, borderwidth=1)
       frmBtnToday.grid(row=8,column=2,padx=5, pady=5)
       btnToday = tk.Button(master=frmBtnToday, text="Today", command=self.showToday, height=1, width=10)
       btnToday.config(font=("Helvetica Bold", int(12 * self.size_ratio)))
       btnToday.pack()
       
       self.btnToday = btnToday
       self.originalButtonColor = self.btnToday.cget("background")  

       frmBtnNext = tk.Frame(master=self, borderwidth=1)
       frmBtnNext.grid(row=8,column=3,padx=5, pady=5, sticky=tk.E)
       btnNext = tk.Button(master=frmBtnNext, text=">", command=self.showNextDate, height=1, width=3)
       btnNext.config(font=("Helvetica Bold",int(12 * self.size_ratio)))
       btnNext.pack()
        
       self.rt = RepeatedTimer(5, self.refresh)
       
       self.protocol("WM_DELETE_WINDOW",self.stop_refresh_timer)
   
       
    def set_font_sizes(self):
        
        SCREEN_WIDTH, SCREEN_HEIGHT = self.winfo_screenwidth(), self.winfo_screenheight()
        
        if DEBUG == True:
            print("Screen Size: {}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if SCREEN_WIDTH == 800 and SCREEN_HEIGHT == 480: # screen size that we designed for
            
            win_width = SCREEN_WIDTH
            win_height = int(SCREEN_HEIGHT * 0.9)
        else:
            win_width = int(SCREEN_WIDTH)
            win_height = int(SCREEN_WIDTH * 0.6)
         
            if win_height > SCREEN_HEIGHT:
                win_height = int(SCREEN_HEIGHT * 0.8)
                win_width = int(win_height * 2.2)
        
        self.geometry("{}x{}".format(win_width,win_height))
        
        if DEBUG == True:
            print("Window Size: {}x{}".format(win_width, win_height))
        
        self.size_ratio = win_width/800
        
        if DEBUG == True:
            print("size ratio: {}".format(self.size_ratio))
    
    def showPrevDate(self):
        
        self.date -= timedelta(days = 1)
        
        self.showing_today = False
        
        self.check_today()
        
        self.container.set_date(self.date)
        
        return

    def showNextDate(self):
        
        self.date += timedelta(days = 1)
     
        self.showing_today = False
        
        self.check_today()
        
        self.container.set_date(self.date)
        
        return
    
    def showToday(self):
        
        self.date = date.today()
        
        self.showing_today = True
        
        self.check_today()
        
        self.container.set_date(self.date)
        
        return
    
    def check_today(self):
        
        if self.showing_today == False:
            self.btnToday.configure(bg="blue", fg="white")
        else:
            self.btnToday.configure(bg=self.originalButtonColor, fg="black")
            
    def refresh(self):
        
        # print("date = {}, showing today = {}".format(self.date, self.showing_today))
        if self.date != date.today() and self.showing_today == True:
            self.showToday()
            
    
class dayFrame(tk.Frame):

    frmDate = None
    lblDate = None
    
    frmTamilDate = None
    lblTamilDate = None
    
    frmTamilDateDetails = None
    lblTamilDateDetails = None
    
    locationPopup = None
   
    dataItems = ["Sunrise","Sunset","Nakshathram","Tithi",
                 "Rahu Kalam","Gulikai Kalam","Yamaganda"]
    dataValues = []
    dataLabels = []
    
    locations = []
    location_ids = []
    location_id = "4684888"
    
    def __init__(self, parent, day, size_ratio):
        
        tk.Frame.__init__(self, parent)
        
        self.date = day
        self.size_ratio = size_ratio
        
        self.frames = []
        
        self.show_fields()
        
        self.fetch_data_json()
        
        self.show_json_data()
        
    def show_fields(self):
        
        self.grid_columnconfigure(0, minsize=360 * self.size_ratio, weight=1)
        self.grid_columnconfigure(1, minsize=150 * self.size_ratio, weight=1)
        
        self.grid_columnconfigure(2, minsize=200 * self.size_ratio, weight=1)
        
        textCurrentDate = "Date"
        textTamilDate = "Tamil Date"
        textTamilDateDetails = "Tamil Date Details"
        textTamilYearDetails = "Tamil Year Details"
        
        frmDate = tk.Frame(master=self)
        frmDate.grid(row=0,column=0, columnspan=1, rowspan=2, padx=5, pady=20)
        lblDate = tk.Label(master=frmDate,text=textCurrentDate, justify=tk.CENTER, wraplength=350 * self.size_ratio)
        lblDate.config(font=("Helvetica",int(48 * self.size_ratio),"bold"))
        lblDate.pack()
        
        self.lblDate = lblDate

        frmTamilDate = tk.Frame(master=self)
        frmTamilDate.grid(row=0,column=1, columnspan=1, rowspan=2, padx=5, pady=5)
        lblTamilDate = tk.Label(master=frmTamilDate,text=textTamilDate, justify=tk.CENTER, wraplength=420 * self.size_ratio)
        lblTamilDate.config(font=("Helvetica",int(48 * self.size_ratio),"bold"))
        lblTamilDate.pack()
        
        self.lblTamilDate = lblTamilDate

        frmTamilDateDetails = tk.Frame(master=self)
        frmTamilDateDetails.grid(row=2,column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        lblTamilDateDetails = tk.Label(master=frmTamilDateDetails,text=textTamilDateDetails, justify=tk.CENTER, wraplength=400 * self.size_ratio)
        lblTamilDateDetails.config(font=("Helvetica",int(24 * self.size_ratio)))
        lblTamilDateDetails.pack()
        
        self.lblTamilDateDetails = lblTamilDateDetails

        frmTamilYearDetails = tk.Frame(master=self)
        frmTamilYearDetails.grid(row=3,column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        lblTamilYearDetails = tk.Label(master=frmTamilYearDetails,text=textTamilYearDetails, justify=tk.CENTER, wraplength=400 * self.size_ratio)
        lblTamilYearDetails.config(font=("Helvetica",int(24 * self.size_ratio)))
        lblTamilYearDetails.pack()
        
        self.lblTamilYearDetails = lblTamilYearDetails

        
        textDateDetails1 = "Date Details 1"

        frmDateDetails1 = tk.Frame(master=self)
        frmDateDetails1.grid(row=2,column=0, columnspan=1, rowspan=1, padx=5, pady=5)
        lblDateDetails1 = tk.Label(master=frmDateDetails1,text=textDateDetails1, justify=tk.CENTER, wraplength=800 * self.size_ratio)
        lblDateDetails1.config(font=("Helvetica",int(20 * self.size_ratio)))
        lblDateDetails1.pack()
        
        self.lblDateDetails1 = lblDateDetails1

        textDateDetails2 = "Date Details 2"

        frmDateDetails2 = tk.Frame(master=self)
        frmDateDetails2.grid(row=3,column=0, columnspan=1, rowspan=1, padx=5, pady=5)
        lblDateDetails2 = tk.Label(master=frmDateDetails2,text=textDateDetails2, justify=tk.CENTER, wraplength=800 * self.size_ratio)
        lblDateDetails2.config(font=("Helvetica",int(20 * self.size_ratio)))
        lblDateDetails2.pack()
        
        self.lblDateDetails2 = lblDateDetails2

        textDateDetails3 = "Date Details 3"

        frmDateDetails3 = tk.Frame(master=self)
        frmDateDetails3.grid(row=4,column=0, columnspan=2, rowspan=1, padx=10, pady=5)
        lblDateDetails3 = tk.Label(master=frmDateDetails3,text=textDateDetails3, justify=tk.CENTER, wraplength=800 * self.size_ratio)
        lblDateDetails3.config(font=("Helvetica",int(14 * self.size_ratio)))
        lblDateDetails3.pack()
        
        self.lblDateDetails3 = lblDateDetails3

        # Create a Tkinter variable
        location = StringVar(self)
        locations=[]

        locationPopupStyle = ttk.Style()
        locationPopupStyle.configure("my.TMenubutton",font=("Helvetica",int(11 * self.size_ratio)),width=min(30,int(22 * self.size_ratio)))
        frmLocationPopup = tk.Frame(master=self)
        frmLocationPopup.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        locationPopup = ttk.OptionMenu(frmLocationPopup, location, *locations, style="my.TMenubutton", command=self.set_location)
        locationPopup.pack()
        
        self.locationPopup = locationPopup
        
        locationPopup["menu"].config(font=("Helvetica",int(11 * self.size_ratio)))
        
        # frmdatePicker = tk.Frame(master=self)
        # frmdatePicker.grid(row=10, column=1, padx=5, pady=5)
        # datePicker = DateEntry(master=frmdatePicker, width=8, background='darkblue', foreground='white', borderwidth=2)
        # datePicker.config(font=("Helvetica Bold", int(10 * self.size_ratio)))
        # datePicker.pack()
        # datePicker.bind("<<DateEntrySelected>>", self.set_new_date)

        # self.datePicker = datePicker 
    
        frmRefreshTime = tk.Frame(master=self)
        frmRefreshTime.grid(row=12,column=0, columnspan=2, padx=5, pady=5)
        lblRefreshTime = tk.Label(master=frmRefreshTime,text="", justify=tk.LEFT)
        lblRefreshTime.config(font=("Helvetica",int(10 * self.size_ratio)))
        lblRefreshTime.pack()
        
        self.lblRefreshTime = lblRefreshTime

    def set_new_date(self, date):

        new_date = self.datePicker.get_date()
        print(f"new date set: {self.datePicker.get_date()}")
        self.set_date(new_date)
        
    def set_date(self,date):
        
        self.date = date
        self.fetch_json_data_for_date(date)
        self.show_json_data()
        
    def fetch_data_json(self):
        
        self.fetch_json_data_for_date(self.date)
        
    def fetch_json_data_for_date(self, date):
        
        self.json_data = json.loads(panchangam.get_details_for_date(date, self.location_id))
        
    def set_location(self, location):
        
        self.location_id = self.location_ids[location]
        # print("Location changed to " + location + " location id set to " + self.location_id)
        self.fetch_json_data_for_date(self.date)
        self.show_json_data()
            
    def show_json_data(self):
        
        self.lblDate.configure(text=self.json_data["date_text"])
        self.lblTamilDate.configure(text=self.json_data["date_tamil"])
        self.lblTamilYearDetails.configure(text=self.json_data["year_tamil"])
        self.lblTamilDateDetails.configure(text=self.json_data["tamil_date_details"])
            
        sunrise = self.json_data["Sunrise"]
        sunset = self.json_data["Sunset"]
        nakshathram = self.json_data["Nakshathram"]
        textDateDetails1 = " \u263c\u2191 " + sunrise + " " + " \u263c\u2193 " + sunset
        
        self.lblDateDetails1.configure(text=textDateDetails1)
        
        textDateDetails2 = " \u2605 " + nakshathram
        self.lblDateDetails2.configure(text=textDateDetails2)

        rahu = self.json_data["Rahu Kalam"]
        guli = self.json_data["Gulikai Kalam"]
        yama = self.json_data["Yamaganda"]

        textDateDetails3 = "Rahu: " + rahu + " " + "Gulikai: " + guli + \
            " Yama: " + yama
        
        self.lblDateDetails3.configure(text=textDateDetails3)

        location_ids={}
        location_names={}
        locations = []
        for location in self.json_data["locations"]:
            locations.append(location["name"])
            location_ids[location["name"]] = location["id"]
            location_names[location["id"]] = location["name"]
        
        self.locations = locations
        self.location_ids = location_ids
        self.location_id = self.json_data["geo_location"]
        
        self.locationPopup.set_menu(location_names[self.location_id], *self.locations)
                            
        # datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        self.lblRefreshTime.configure(text="Last refreshed at {0}".format(self.json_data["last_refresh"]))
    
app = PanchangamView()

app.mainloop()

