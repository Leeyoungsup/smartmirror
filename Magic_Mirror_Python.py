import tkinter as tk
from tkinter import *
import time
from urllib.request import urlopen, Request
import urllib
import bs4

startupscreen = tk.Tk()
startupscreen.title('Magic Mirror: Python')
welcometext = tk.Label(startupscreen, font = ('caviar dreams', 40), bg='black', fg='white')
startupscreen.configure(background='black')
startupscreen.overrideredirect(True)
welcometext.config(text='SmartMirror: LYS')
welcometext.pack(side=LEFT, padx= 120, pady=80)
windowWidth = startupscreen.winfo_reqwidth()
windowHeight = startupscreen.winfo_reqheight()
positionRight = int(startupscreen.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(startupscreen.winfo_screenheight()/2 - windowHeight/2)
startupscreen.geometry("+{}+{}".format(positionRight, positionDown))
startupscreen.update()
decrypt = list()
iteration = 0
timecount = 0
repull = 0
sleep = 0
count=0
def calender():
    caly1=''
    f = open("calender.txt", 'r')
    caly=f.readline()
    while(caly!=''):
        caly=f.readline()
        if caly[:8]==time.strftime("%y/%m/%d"):
            caly1=caly1+caly[9:]
        
    calender_frame1.config(text=caly1)
def weather():
    location = '대전'
    enc_location = urllib.parse.quote(location + '+날씨')
    url = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+ enc_location
    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,"html.parser")
    weather1='현재 ' + location + ' 날씨는 '+ soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.'
    weather2=soup.find('p', class_='cast_txt').text+'.'
    weather_frame.config(text=weather1)
    weather_frame2.config(text=weather2)

def tick(time1=''):
    time2 = time.strftime("%H")
    if time2 != time1:
        time1 = time2
        clock_frame.config(text=time2)
        if int(time2)%2==0 and int(time.strftime("%M"))==30 and int(time.strftime("%S"))==30 :
            weather()
            calender()
    clock_frame.after(200, tick)

def tickk(time3=''):
    time4 = time.strftime(":%M:%S")
    if time4 != time3:
        time3 = time4
        clock_frame2.config(text=time4)
    clock_frame2.after(200, tickk)
def tock():
    global timecount
    global repull
    global sleep
    global decrypt
    if timecount < 20:
        timecount +=1
    else:
        timecount = 0
        newsheader()
    if repull < 200:
        repull +=1
    else:
        repull = 0
        payload = headlines
        decrypt = (payload['articles'])
        maxrange = len(decrypt)
    if sleep < 800:
        sleep+=1
    else:
        sleep = 0
def ymdgui(ymd1=0):
    ymd = time.strftime("%y/%m/%d")
    if ymd != ymd1:
        ymd1 = ymd
        ymd_frame.config(text=ymd)
    ymd_frame.after(200, ymdgui)
while True:
    root = tk.Tk()
    root.title('Mirror')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    ymd_frame = tk.Label(root, font = ('caviar dreams', 70), bg='black', fg='white')
    ymd_frame.pack(side=TOP)
    weather_frame = tk.Label(root, font = ('caviar dreams', 30), bg='black', fg='white')
    weather_frame.pack()
    weather_frame2 = tk.Label(root, font = ('caviar dreams', 30), bg='black', fg='white')
    weather_frame2.pack()
    clock_frame = tk.Label(root, font = ('caviar dreams', 70), bg='black', fg='white')
    clock_frame.pack()
    clock_frame.place(x=0,y=0)
    clock_frame2 = tk.Label(root, font = ('caviar dreams', 70), bg='black', fg='white')
    clock_frame2.pack()
    clock_frame2.place(x=110,y=0)
    calender_frame = tk.Label(root, font = ('caviar dreams', 30), bg='black', fg='white')
    calender_frame.pack()
    calender_frame.place(x=screen_width-500,y=0)
    calender_frame1 = tk.Label(root, font = ('caviar dreams', 30), bg='black', fg='white',wraplength=500)
    calender_frame1.pack()
    calender_frame1.place(x=screen_width-500,y=50)
    tick()
    tickk()
    tock()
    ymdgui()
    if count==0:
        weather()
        calender_frame.config(text='오늘 할일')
        calender()
    count+=1
    root.attributes("-fullscreen", True)
    root.configure(background='black')
    startupscreen.destroy()
    root.mainloop()
