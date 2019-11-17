# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime
from dateutil.relativedelta import relativedelta


#function to fetch data
def fetch_data(delta):
    endate = d + delta    
##    print('End Date:'+str(endate))
    
    end_date = datetime.datetime.strptime(str(endate), '%Y-%m-%d')
    end_date = end_date.strftime('%d/%m/%Y')
    print('End Date:'+str(end_date))
    
    #input end date on the webpage
    inputenddate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"(//input[@class='dijitReset dijitInputInner'])[last()]")))
    inputenddate.clear()    
    inputenddate.send_keys(str(end_date))
    
    time.sleep(1)

    #Click the refresh button on the webpage    
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='form-submit'][@value='REFRESH']"))).click()
    WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"table#taboa")))
        
    time.sleep(3)

    # parse the table using beautiful soup
    soup=BeautifulSoup(driver.page_source,"html.parser")
    table=soup.find("table", id="taboa")
    time.sleep(1)

    # save to pandas dataframe
    df=pd.read_html(str(table))
    print(df)
    time.sleep(1)
    
    # write to csv
    df[0].to_csv('test_sot.csv', mode='a', header=False)
    time.sleep(1)
    return

# specify the url
urlpage = 'http://www.sotaventogalicia.com/en/real-time-data/historical'
print(urlpage)

# run Chrome webdriver from executable path of your choice
driver = webdriver.Chrome('C:/Users/Shresth Suman/Downloads/chromedriver_win32/chromedriver.exe')

# get web page
driver.get(urlpage)

# execute script

startdate = datetime.date(2012,5,1)

enddate = datetime.date.today()

delta = relativedelta(months=+1)

d = startdate

WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"frame_historicos")))

#Loop for fetching data from 1st Jan 2005 to today
while d <= enddate:
    
##    print ('Start Date:'+str(d))
    in_date = datetime.datetime.strptime(str(d), '%Y-%m-%d')
    in_date = in_date.strftime('%d/%m/%Y')
    print('Start Date:'+str(in_date))

    #input start date on the webpage
    inputstartdate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"(//input[@class='dijitReset dijitInputInner'])[1]")))
    inputstartdate.clear()
    inputstartdate.send_keys(str(in_date))
    time.sleep(1)
    d += delta

    # For month October, fetch data from 1st to 30th and then 31st Oct
    if(d.month == 11):
        delta2 = relativedelta(days=-2)
        time.sleep(1)

        fetch_data(delta2)
        
                
        delta_start = relativedelta(days=-1)
        start_date = d + delta_start
##        print ('Start Date:'+str(start_date))
        in_date = datetime.datetime.strptime(str(start_date), '%Y-%m-%d')
        in_date = in_date.strftime('%d/%m/%Y')
        print('Start Date:'+str(in_date))

        #input start date on the webpage
        inputstartdate = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"(//input[@class='dijitReset dijitInputInner'])[1]")))
        inputstartdate.clear()
        inputstartdate.send_keys(str(in_date))
        time.sleep(1)
        
        #Input start and end date as 31st Oct
        delta_end = relativedelta(days=-1)
        fetch_data(delta_end)
      
    #Fetch data from remaining months of the year
    else:
        time.sleep(1)
        delta2 = relativedelta(days=-1)
        fetch_data(delta2)


print('data written to csv file')

# close driver
driver.quit()
