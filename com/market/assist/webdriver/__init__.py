from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#"E:\Python_works\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome('E:\\Python_works\\chromedriver.exe')
driver.get("http://www.nseindia.com/all-reports-derivatives")
time.sleep(15)
link = driver.find_element_by_link_text('Archives')
link.click()
time.sleep(10)
driver.execute_script('document.getElementById( "cr_deriv_equity_archives_date" ).value = "05-Aug-2020"');
time.sleep(5)
driver.execute_script('fileDownload([{"name":"F&O - Bhavcopy(csv)","type":"archives","category":"derivatives","section":"equity"}],"equity","#cr_deriv_equity_archives","single")');
time.sleep(5)

#driver.find_element_by_xpath("(//a[@onclick="SingledownloadReports('#cr_deriv_equity_archives', 'equity', this)"])[12]").click()
# driver.close()