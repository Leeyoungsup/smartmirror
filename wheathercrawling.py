import time
from urllib.request import urlopen, Request
import urllib
import bs4
import Magic_Mirror_Python
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
