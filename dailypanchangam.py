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
    
    locations = []
    location_ids = []
    location_id = "4684888"

    def stop_refresh_timer(self):
        
        self.rt.stop()
        self.destroy()
    
    def __init__(self, *args, **kwargs):
        
       tk.Tk.__init__(self, *args, **kwargs)
       
       self.date = date.today()
       
       self.set_window_size()
       
       self.showing_today = True
       
       self.container = dayFrame(self, self.date, self.win_width, self.win_height, self.size_ratio)

       self.container.grid(row=0,column=0, columnspan=5)

       self.title("Daily Panchangam")
       self.resizable(False, False) # disable resizing
    
       frmBtnPrev = tk.Frame(master=self, borderwidth=1)
       frmBtnPrev.grid(row=1,column=0,padx=5, pady=5, sticky=tk.W)
       btnPrev = tk.Button(master=frmBtnPrev, text="<", command=self.showPrevDate, height=1, width=3)
       btnPrev.config(font=("Helvetica Bold", int(12 * self.size_ratio)))
       btnPrev.pack()

       # Create a Tkinter variable
       location = StringVar(self)
       locations=[]

       locationPopupStyle = ttk.Style()
       locationPopupStyle.configure("my.TMenubutton",font=("Helvetica",int(16 * self.size_ratio)),width=min(30,int(22 * self.size_ratio)))
       frmLocationPopup = tk.Frame(master=self)
       frmLocationPopup.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky=tk.EW)
       locationPopup = ttk.OptionMenu(frmLocationPopup, location, *locations, style="my.TMenubutton", command=self.set_location)
       locationPopup.pack()
        
       self.locationPopup = locationPopup
        
       locationPopup["menu"].config(font=("Helvetica",int(14 * self.size_ratio)))
       
       location_ids={}
       location_names={}
       locations = []
       for location in json.loads(panchangam.get_locations())["locations"]:
           locations.append(location["name"])
           location_ids[location["name"]] = location["id"]
           location_names[location["id"]] = location["name"]
        
       self.locations = locations
       self.location_ids = location_ids
       
       self.locationPopup.set_menu(location_names[self.location_id], *self.locations)

       frmBtnToday = tk.Frame(master=self, borderwidth=1)
       frmBtnToday.grid(row=1,column=2,padx=5, pady=5)
       btnToday = tk.Button(master=frmBtnToday, text="Today", command=self.showToday, height=1, width=10)
       btnToday.config(font=("Helvetica Bold", int(12 * self.size_ratio)))
       btnToday.pack()
       
       self.btnToday = btnToday
       self.originalButtonColor = self.btnToday.cget("background")  

       frmBtnDate = tk.Frame(master=self, borderwidth=1)
       frmBtnDate.grid(row=1,column=3,padx=5, pady=5)
       btnDate = tk.Button(master=frmBtnDate, text="\u2317", command=self.showToday, height=1, width=4)
       btnDate.config(font=("Helvetica Bold", int(10 * self.size_ratio)))
       btnDate.pack()

       frmBtnNext = tk.Frame(master=self, borderwidth=1)
       frmBtnNext.grid(row=1,column=4,padx=5, pady=5, sticky=tk.E)
       btnNext = tk.Button(master=frmBtnNext, text=">", command=self.showNextDate, height=1, width=3)
       btnNext.config(font=("Helvetica Bold",int(12 * self.size_ratio)))
       btnNext.pack()
        
       self.rt = RepeatedTimer(5, self.refresh)
       
       self.protocol("WM_DELETE_WINDOW",self.stop_refresh_timer)
   
       
    def set_window_size(self):
        
        SCREEN_WIDTH, SCREEN_HEIGHT = self.winfo_screenwidth(), self.winfo_screenheight()
        
        if DEBUG == True:
            print("Screen Size: {}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))
        
        if SCREEN_WIDTH == 800 and SCREEN_HEIGHT == 480: # screen size that we designed for
            
            self.win_width = SCREEN_WIDTH
            self.win_height = int(SCREEN_HEIGHT * 0.9)
        else:
            self.win_width = int(SCREEN_WIDTH)
            self.win_height = int(SCREEN_WIDTH * 0.6)
         
            if self.win_height > SCREEN_HEIGHT:
                self.win_height = int(SCREEN_HEIGHT * 0.8)
                self.win_width = int(self.win_height * 2.2)
        
        self.geometry("{}x{}".format(self.win_width,self.win_height))
        
        if DEBUG == True:
            print("Window Size: {}x{}".format(self.win_width, self.win_height))
        
        self.size_ratio = self.win_width/800
        
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
    
    def set_location(self, location):
        
        self.location_id = self.location_ids[location]

        self.container.set_location(self.location_id)

    def refresh(self):
        
        # print("date = {}, showing today = {}".format(self.date, self.showing_today))
        if self.date != date.today() and self.showing_today == True:
            self.showToday()
            
    
class dayFrame(ttk.Frame):

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
    
    def __init__(self, parent, day, win_width, win_height, size_ratio):
        
        self.frame = ttk.Frame.__init__(self, parent)

         # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)
        
        hscrollbar = ttk.Scrollbar(self, orient=HORIZONTAL)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=TRUE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, width=win_width * 0.98, height=win_height * 0.8,
                           yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        self.canvas.configure(scrollregion=(0, 0, win_width, win_height))

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvas

        self.interior = interior = ttk.Frame(master=self.canvas, width=win_width, height=win_height)
        interior_id = self.canvas.create_window(0, 0, window=self.interior,
                                           anchor=NW)     
        self.date = day
        self.size_ratio = size_ratio
        
        self.frames = []
        
        self.show_fields()
        
        self.fetch_data_json()
        
        self.show_json_data()
        
        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                self.canvas.config(width=interior.winfo_reqwidth())
            self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
            self.canvas.bind('<Configure>', _configure_canvas)

    def show_fields(self):
        
        self.grid_columnconfigure(0, minsize=360 * self.size_ratio, weight=1)
        self.grid_columnconfigure(1, minsize=150 * self.size_ratio, weight=1)
        
        self.grid_columnconfigure(2, minsize=200 * self.size_ratio, weight=1)
        
        textCurrentDate = "Date"
        textTamilDate = "Tamil Date"
        textTamilDateDetails = "Tamil Date Details"
        textTamilYearDetails = "Tamil Year Details"
        
        frmDate = tk.Frame(master=self.interior)
        frmDate.grid(row=0,column=0, columnspan=1, rowspan=1, padx=5, pady=20)
        lblDate = tk.Label(master=frmDate,text=textCurrentDate, justify=tk.CENTER, wraplength=350 * self.size_ratio)
        lblDate.config(font=("Helvetica",int(32 * self.size_ratio),"bold"))
        lblDate.pack()
        
        self.lblDate = lblDate

        frmTamilDate = tk.Frame(master=self.interior)
        frmTamilDate.grid(row=0,column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        lblTamilDate = tk.Label(master=frmTamilDate,text=textTamilDate, justify=tk.CENTER, wraplength=420 * self.size_ratio)
        lblTamilDate.config(font=("Helvetica",int(48 * self.size_ratio),"bold"))
        lblTamilDate.pack()
        
        self.lblTamilDate = lblTamilDate

        frmTamilDateDetails = tk.Frame(master=self.interior)
        frmTamilDateDetails.grid(row=1,column=1, columnspan=1, rowspan=1, padx=5, pady=10)
        lblTamilDateDetails = tk.Label(master=frmTamilDateDetails,text=textTamilDateDetails, justify=tk.CENTER, wraplength=400 * self.size_ratio)
        lblTamilDateDetails.config(font=("Helvetica",int(30 * self.size_ratio)))
        lblTamilDateDetails.pack()
        
        self.lblTamilDateDetails = lblTamilDateDetails

        frmTamilYearDetails = tk.Frame(master=self.interior)
        frmTamilYearDetails.grid(row=2,column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        lblTamilYearDetails = tk.Label(master=frmTamilYearDetails,text=textTamilYearDetails, justify=tk.CENTER, wraplength=400 * self.size_ratio)
        lblTamilYearDetails.config(font=("Helvetica",int(24 * self.size_ratio)))
        lblTamilYearDetails.pack()
        
        self.lblTamilYearDetails = lblTamilYearDetails

        
        textDateDetails1 = "Date Details 1"

        frmDateDetails1 = tk.Frame(master=self.interior)
        frmDateDetails1.grid(row=1,column=0, columnspan=1, rowspan=1, padx=5, pady=10)
        lblDateDetails1 = tk.Label(master=frmDateDetails1,text=textDateDetails1, justify=tk.CENTER, wraplength=400 * self.size_ratio)
        lblDateDetails1.config(font=("Helvetica",int(20 * self.size_ratio)))
        lblDateDetails1.pack()
        
        self.lblDateDetails1 = lblDateDetails1

        textDateDetails2 = "Date Details 2"

        frmDateDetails2 = tk.Frame(master=self.interior)
        frmDateDetails2.grid(row=2,column=0, columnspan=1, rowspan=3, padx=5, pady=10)
        lblDateDetails2 = tk.Label(master=frmDateDetails2,text=textDateDetails2, justify=tk.LEFT, wraplength=400 * self.size_ratio)
        lblDateDetails2.config(font=("Helvetica",int(22 * self.size_ratio)))
        lblDateDetails2.pack()
        
        self.lblDateDetails2 = lblDateDetails2
    
        frmRefreshTime = tk.Frame(master=self.interior)
        frmRefreshTime.grid(row=3,column=1, columnspan=1, padx=5, pady=5)
        lblRefreshTime = tk.Label(master=frmRefreshTime,text="", justify=tk.LEFT)
        lblRefreshTime.config(font=("Helvetica",int(10 * self.size_ratio)))
        lblRefreshTime.pack()
        
        self.lblRefreshTime = lblRefreshTime

    def set_location(self, location_id):
        
        self.location_id = location_id

        # print("Location changed to " + location + " location id set to " + self.location_id)
        self.fetch_json_data_for_date(self.date)
        self.show_json_data()
        
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
            
    def show_json_data(self):
        
        self.lblDate.configure(text=self.json_data["date_text"])
        self.lblTamilDate.configure(text=self.json_data["date_tamil"])
        self.lblTamilYearDetails.configure(text=self.json_data["year_tamil"])
        self.lblTamilDateDetails.configure(text=self.json_data["tamil_date_details"])
            
        sunrise = self.json_data["Sunrise"]
        sunset = self.json_data["Sunset"]
        nakshathram = self.json_data["Nakshathram"]
        textDateDetails1 = " \u263c\u2191 " + sunrise + " " + " \u263c\u2193 " + sunset \
            + "\n \u2605 " + nakshathram
        
        self.lblDateDetails1.configure(text=textDateDetails1)

        rahu = self.json_data["Rahu Kalam"]
        guli = self.json_data["Gulikai Kalam"]
        yama = self.json_data["Yamaganda"]

        textDateDetails2 = "Rahu: " + rahu + " " + "Guli: " + guli + \
           "\nYama: " + yama
        
        self.lblDateDetails2.configure(text=textDateDetails2)

        self.location_id = self.json_data["geo_location"]

        self.lblRefreshTime.configure(text="Last refreshed at {0}".format(self.json_data["last_refresh"]))
    
app = PanchangamView()

app.mainloop()

