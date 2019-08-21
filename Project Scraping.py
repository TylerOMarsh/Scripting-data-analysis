#Functional approach

#working directory hidden so writing to csv may yield different results

import pandas as pd
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
###Weather scrapping with functions



#Raw_data = get_raw_data()

#Step1_data = convert_to_step1(Raw_data)

#Step2_data = convert_to_step2(step1_data)

#Print(step2_data)



#Raw data
def get_dates(year, months):
    '''

    :param year: what year
    :param months: int > 0 < 13 at what month do you want to stop at?
    :return: a list of dates in a year. Starting at 1 up to certain month
    '''
    dates = [ ]
    for m in range(1, months + 1):
        for d in range(1, 32):
            if (m == 2 and d > 28 ):
                break
            elif (m in [4, 6, 9, 11] and d > 30):
                break
            date =str(year) + "-" + str(m) +"-"+str(d)
            dates.append(date)
    return dates



def empty_df():
    '''
    creates an empty data frame with the desired columns
    :return: a dataframe with columns of desired information and no rows
    '''
    name = pd.DataFrame(columns=['Date', 'HighTemp', 'LowTemp', 'AverageTemp', 'Precipitation', 'NauticalTwilightRise', 'NauticalTwilightSet'])
    return name




#make a list of values
def insert_data(base_url, the_xpath, dates,):
    '''
    returns a list of lists to insert into the dataframe.
    :param empty_df:
    :param base_url: url that has dates added to it from the dates list
    :param the_xpath: xpath for the tables the data is coming from
    :param dates: the list of dates made from above functions
    :return: data_list = the values obtained here
    '''
    count = 0
    master_list = [['apple']]
    driver = webdriver.Firefox()
    for day in range(0, len(dates)):
        url = base_url + dates[day]
        try:
            driver.get(url)
            table = driver.find_element_by_xpath(the_xpath)
            table_list = table.text.split()
            list1 = [dates[day], table_list[10], table_list[15],table_list[21], table_list[31], table_list[176], table_list[178]]
            master_list.append(list1)
        except Exception:
            print("exception")
        count += 1
        print(str(count))
    master_list.remove(['apple'])
    return master_list


#set up selenium
driver = webdriver.Firefox()

driver.implicitly_wait(15) # wait 15 seconds to get data if needed.

driver.get(base_url) #in this instance the base is still a functional page. get selenium running before first command


#get variables for selenium
#xpath
the_xpath1 = '/html/body/app/city-history/city-history-layout/div/div[2]/section/div[2]/div[2]/div/div[1]/div'

#base url to add dates to
base_url1 = "https://www.wunderground.com/history/daily/us/ca/burbank/KBUR/date/"

#create desired dates

dates17 = get_dates(2017, 12) #make dates list

#create container for data
df17 = empty_df() #make data frame

#get the data into a list of lists
data_points = insert_data(base_url1, the_xpath1, dates17)

df17 = df17.append(pd.DataFrame(data_points, columns=df17.columns))

#get working directory
my_cwd = os.getcwd()


df17.to_csv(my_cwd,'/2017weather.csv', index=False)



dates18 = get_dates(2018, 12)    #put the desired dates into list

df18 = empty_df() #make empty data frame

data_points_18 = insert_data(base_url1, the_xpath1, dates18) #put desired information into list of lists

df18 = df18.append(pd.DataFrame(data_points, columns=df18.columns)) #insert data into data frame

df18.to_csv(my_cwd, '/2018weather.csv', index=False) #write to a csv

dates19 = get_dates(2019, 8) #put the desired dates into list

df19 = empty_df() #make empty data frame

data_points_19 = insert_data(base_url1, the_xpath1, dates19)#put desired information into list of lists

df19 = df19.append(pd.DataFrame(data_points_19, columns=df19.columns))#insert data into data frame

df19.to_csv(my_cwd, '/2019weather.csv', index=False)
