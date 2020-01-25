import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from time import sleep
import json

url = 'http://opendata.epa.gov.tw'
browser = webdriver.Chrome()
browser.maximize_window()
browser.get(url)

sleep(1)
browser.find_element_by_link_text("空氣品質指標(AQI)").click() 
#link_text(text)以連結文字查詢符合的元素

sleep(1)
browser.find_element_by_link_text("資料檢視").click()

sleep(1)
browser.find_element_by_link_text('JSON').click()
c_url = browser.current_url #current_url 獲得當前網址
browser.get(c_url) #get 網址
html = browser.page_source #網頁原始碼
df=pd.read_html(html) #list

#將列表變成dataframe形式
df1 = pd.DataFrame(df[3])
#即時資料儲存
location = df1.iloc[74][0]
TIME = df1.iloc[74][17]
O3_8 = float(df1.iloc[74][9])/1000
PM25_avg = float( df1.iloc[74][18])
PM10_avg =  float(df1.iloc[74][19])
CO_8 = float(df1.iloc[74][7])
SO2 = float(df1.iloc[74][5])
NO2 = float(df1.iloc[74][12])

#設定各空氣污染副指標範圍
breakpoint = [0,50,100,150,200,300,400,500]
O3_8_level = [0.000, 0.054,0.070, 0.085,0.105,0.2,0.2,0.2]
# O3_level = [0,0,0.125,0.164,0.204,0.404,0.504,0.604]
PM25_avg_level = [0.0,15.4,35.4,54.4,150.4,250.4,350.4,500.4]
PM10_avg_level = [0,54,125,254,354,424,504,604]
CO_level = [0,4.4,9.4,12.4,15.4,30.4,40.4,50.4]
SO2_level = [0,35,75,185,304,604,804,1004]
NO2_level = [0,53,100,360,649,1249,1649,2049]

#定義各污染副指標範圍
def aqi_sub(c_range, conc):
    if conc >= c_range[0] and conc <= c_range[1]:
        AQI =  breakpoint[0] + (conc-c_range[0])*breakpoint[1]/c_range[1]
    elif conc > c_range[1] and conc <= c_range[2]:
        AQI = breakpoint[1] + (breakpoint[2]-breakpoint[1])*(conc-c_range[1])/(c_range[2]-c_range[1])
    elif conc > c_range[2] and conc <= c_range[3]:
        AQI = breakpoint[2] + (breakpoint[3]-breakpoint[2])*(conc-c_range[2])/(c_range[3]-c_range[2])
    elif conc > c_range[3] and conc <= c_range[4]:
        AQI = breakpoint[3] + (breakpoint[4]-breakpoint[3])*(conc-c_range[3])/(c_range[4]-c_range[3])
    elif conc > c_range[4] and conc <= c_range[5]:
        AQI = breakpoint[4] + (breakpoint[5]-breakpoint[4])*(conc-c_range[4])/(c_range[5]-c_range[4])
    elif conc > c_range[5] and conc <= c_range[6]:
        AQI = breakpoint[5] + (breakpoint[6]-breakpoint[5])*(conc-c_range[5])/(c_range[6]-c_range[5])
    else:
        AQI = breakpoint[6] + (breakpoint[7]-breakpoint[6])*(conc-c_range[6])/(c_range[5]-c_range[4])
    return AQI

#定義計算AQI
def AQI_cal(O3_8,PM25_avg,PM10_avg,CO,SO2,NO2):
    aqi_O3 = aqi_sub(O3_8_level,O3_8)
    aqi_PM25 = aqi_sub(PM25_avg_level, PM25_avg)
    aqi_PM10 = aqi_sub(PM10_avg_level,PM10_avg)
    aqi_CO = aqi_sub(CO_level, CO)
    aqi_SO2 = aqi_sub(SO2_level,SO2)
    aqi_NO2 = aqi_sub(NO2_level,NO2)
    
    AQI = max([aqi_O3,aqi_PM25,aqi_PM10,aqi_CO,aqi_SO2,aqi_NO2])
    return AQI