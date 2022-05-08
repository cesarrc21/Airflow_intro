#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd


exec_path = ''  #insert your driver path here
driver = webdriver.Firefox(exec_path)


driver.get("https://www.timeanddate.com/weather/mexico")  # webpage to get the weather forecasts


WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "input[class='picker-city__input']"))).send_keys('Mérida')  #to select city


WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "button[class='picker-city__button']"))).click()


WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[6]/section[1]/div/section[2]/div[1]/div/table/tbody/tr[1]/td[1]/a'))).click()


WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[6]/main/section/nav/div/a[2]'))).click()


WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                      '//*[@id="weatherContainer"]'))).click()  


columnsText = driver.find_element(By.XPATH, '//*[@id="weatherContainer"]')  #to get data  
columnsText = columnsText.text


print(columnsText)


current_weather = columnsText.split('\n')  #format


print(current_weather)


# verify date(s) according to the time

date = list()


ind=[]
for i in range(0,len(current_weather)):
    if len(current_weather[i])>5:
        date.append(current_weather[i])
        ind.append(i)


if len(date)==2:
    d1 =list()
    d2= list()
    d1.append(date[0])
    d2.append(date[1])
    date = (d1*round(ind[1]/3)) + (d2*round((len(current_weather)-(ind[1]+1))/3))
    current_weather.pop(ind[0])
    current_weather.pop(ind[1]-1)
elif len(date)==1:
    date = date*((len(current_weather))/3)
    current_weather.pop(ind[0])


# split data into different list

time = list()
temperature = list()
wind = list()


for i in range(0, len(current_weather),3):
    time.append(current_weather[i])
    temperature.append(current_weather[i+1])
    wind.append(current_weather[i+2])


# dataframe
df = pd.DataFrame({'Date':date,'Time(h)': time, 'Temperature(F)': temperature, 'Wind(Mph)':wind})
print(df)


# export as csv
df.to_csv('todays_weather.csv', index=False)

#end Selenium driver
driver.quit()

