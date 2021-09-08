import requests
from datetime import timedelta, date
import time

# url = 'https://www1.nseindia.com/content/historical/DERIVATIVES/2020/AUG/fo14AUG2020bhav.csv.zip'
# r = requests.get(url, allow_redirects=True)
# open('1.zip', 'wb').write(r.content)
# "https://www1.nseindia.com/content/historical/DERIVATIVES/2020/AUG/fo14AUG2020bhav.csv.zip"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36'}
headers = {'User-Agent': 'Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36'}

start_date = date(2015, 1, 1)
end_date = date(2016, 1, 1)
for single_date in daterange(start_date, end_date):
    strDate=( single_date.strftime("%d%b%Y")).upper()
    strYear=( single_date.strftime("%Y")).upper()
    strMonth=( single_date.strftime("%b")).upper()
    dayOfWeek=int(single_date.strftime("%w"))
    if dayOfWeek>0 and dayOfWeek<6 :
        url = "https://www1.nseindia.com/content/historical/DERIVATIVES/"+strYear+"/"+strMonth+"/fo"+ strDate +"bhav.csv.zip"
        r = requests.get(url, headers=headers,allow_redirects=True )
        print(r)
        open("/my_data/" + strDate+".zip" , 'wb').write(r.content)
        print(url + " : " + single_date.strftime("%w"))
        time.sleep(40)



