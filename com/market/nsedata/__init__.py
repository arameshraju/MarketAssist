import sys

import requests
import csv

url_oc = "https://www.nseindia.com/option-chain"
# url = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
url = f"https://www.nseindia.com/api/option-chain-equities?symbol=SBIN"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
session = requests.Session()
request = session.get(url_oc, headers=headers, timeout=5)
cookies = dict(request.cookies)
stockdata=[]

def getStockData(names):
    for name in names:
        try:
            # print(name)
            url = f"https://www.nseindia.com/api/option-chain-equities?symbol=" +name
            response = session.get(url, headers=headers, timeout=5, cookies=cookies)
            # print(response.json())
            # print(mydata['records']['strikePrices'])
            mydata=response.json()
            price=mydata['records']['underlyingValue']
            stikes=mydata['records']['strikePrices']
            strikeChange=stikes[1]-stikes[0]
            # print(price)
            atmL = round(price - (price % strikeChange))
            atmH = round(price - (price % strikeChange))+strikeChange

            atm=round(price-(price % strikeChange))
            atmup=(atm+(10*strikeChange))
            atmdown=(atm-(10*strikeChange))
            # print(atm)
            curData=mydata['filtered']['data']
            totalCe=mydata['filtered']['CE']
            totalPe=mydata['filtered']['PE']
            putData={"oi":0,"oi_chg":0,"volume":0}
            callData={"oi":0,"oi_chg":0,"volume":0}
            putAMT = {"oi": 0, "oi_chg": 0, "volume": 0}
            callAMT = {"oi": 0, "oi_chg": 0, "volume": 0}
            supportAMT = {"strikePrice":0,"oi": 0, "oi_chg": 0, "volume": 0,"underlyingValue":0}
            resistanceAMT = {"strikePrice":0,"oi": 0, "oi_chg": 0, "volume": 0,"underlyingValue":0}

            for d in curData:
                strk=d['strikePrice']
                # print(d)

                ce=d['CE'] if d.__contains__('CE') else []
                pe=d['PE'] if d.__contains__('PE') else []


                if( pe!=[] and  pe['openInterest'] > supportAMT['oi']):
                   supportAMT['strikePrice']=strk
                   supportAMT['oi']=pe['openInterest']
                   supportAMT['oi_chg']=pe['changeinOpenInterest']
                   supportAMT['underlyingValue']=pe['underlyingValue']
                if(  ce!=[] and  ce['openInterest'] > resistanceAMT['oi']):
                   resistanceAMT['strikePrice']=strk
                   resistanceAMT['oi']=ce['openInterest']
                   resistanceAMT['oi_chg']=ce['changeinOpenInterest']
                   resistanceAMT['underlyingValue']=ce['underlyingValue']


                if strk== atmL or strk==atmH:
                    ce = d['CE']
                    callAMT['oi'] += ce['openInterest']
                    callAMT['oi_chg'] += ce['changeinOpenInterest']
                    callAMT['volume'] += ce['totalTradedVolume']
                    ce=d['PE']
                    putAMT['oi']+=ce['openInterest']
                    putAMT['oi_chg']+=ce['changeinOpenInterest']
                    putAMT['volume']+=ce['totalTradedVolume']

                if strk >= atm   and strk <= atmup :
                    # print(str(strk)  + " call")
                    ce=d['CE']
                    callData['oi']+=ce['openInterest']
                    callData['oi_chg']+=ce['changeinOpenInterest']
                    callData['volume']+=ce['totalTradedVolume']

                if strk <= atm  and strk >= atmdown :
                    # print(str(strk)  + " put")
                    ce=d['PE']
                    putData['oi']+=ce['openInterest']
                    putData['oi_chg']+=ce['changeinOpenInterest']
                    putData['volume']+=ce['totalTradedVolume']

            # print(callData)
                # print(putData)
            tempdata={"name":name,"PutCall_Diff":(totalPe['totOI']-totalCe['totOI']) ,"PutCall_Diff_vol": (totalPe['totVol']-totalCe['totVol']) ,
                      "otm_PutCall_Diff":(putData['oi']-callData['oi']),"otm_PutCall_Diff_chng":(putData['oi_chg']-callData['oi_chg']),"otm_PutCall_Diff_net_volume":(putData['volume']-callData['volume']),
                      "ATM_PUT_OI":putAMT['oi'] , "ATM_CALL_OI_": callAMT['oi'],"ATM_PUT_OI_CH":putAMT['oi_chg'] , "ATM_CALL_OI_CH": callAMT['oi_chg'],"amt_PutCall_Diff":(putAMT['oi']-callAMT['oi']),"amt_PutCall_Diffchng":(putAMT['oi_chg']-callAMT['oi_chg']),"atm_PutCall_Diff_volume":(putAMT['volume']-callAMT['volume']),
                     "Support":supportAMT['strikePrice'],"Support_oi":supportAMT['oi'],"Support_oi_ch":supportAMT['oi_chg'],"Resistance":resistanceAMT['strikePrice'],"Resistance_oi":resistanceAMT['oi'],"Resistance_oi_chg":resistanceAMT['oi_chg']
                      ,'Price':resistanceAMT['underlyingValue']
                      }
            stockdata.append(tempdata)
        except KeyError:
            print(name + "a/b result error in  " + str(sys.exc_info()[0]) )

namesList=['AARTIIND','ABFRL','ACC','ADANIENT','ADANIPORTS','ALKEM','AMARAJABAT','AMBUJACEM','APLLTD','APOLLOHOSP',
           'APOLLOTYRE','ASHOKLEY','ASIANPAINT','ASTRAL','AUBANK','AUROPHARMA','AXISBANK','BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE',
           'BALKRISIND','BANDHANBNK','BANKBARODA','BATAINDIA','BEL','BERGEPAINT','BHARATFORG','BHARTIARTL','BHEL',
           'BIOCON','BOSCHLTD','BPCL','BRITANNIA','CADILAHC','CANBK','CANFINHOME','CHOLAFIN','CIPLA','COALINDIA','COFORGE',
           'COLPAL','CONCOR','COROMANDEL','CUB','CUMMINSIND','DABUR','DEEPAKNTR','DIVISLAB','DIXON','DLF','DRREDDY','EICHERMOT',
           'ESCORTS','EXIDEIND','FEDERALBNK','GAIL','GLENMARK','GMRINFRA','GODREJCP','GODREJPROP','GRANULES','GRASIM','GUJGASLTD',
           'HAL','HAVELLS','HCLTECH','HDFC','HDFCBANK','HDFCLIFE','HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','IBULHSGFIN',
           'ICICIBANK','ICICIGI','ICICIPRULI','IDEA','IDFCFIRSTB','IEX','IGL','INDHOTEL','INDIAMART','INDIGO','INDUSINDBK',
           'INDUSTOWER','INFY','IOC','IRCTC','ITC','JINDALSTEL','JSWSTEEL','JUBLFOOD','KOTAKBANK','L%26TFH','LALPATHLAB',
           'LICHSGFIN','LT','LTI','LTTS','LUPIN','M%26M','M%26MFIN','MANAPPURAM','MARICO','MARUTI','MCDOWELL-N','MCX','METROPOLIS',
           'MFSL','MGL','MINDTREE','MOTHERSUMI','MPHASIS','MRF','MUTHOOTFIN','NAM-INDIA','NATIONALUM','NAUKRI','NAVINFLUOR','NESTLEIND',
           'NMDC','NTPC','OFSS','ONGC','PAGEIND','PEL','PETRONET','PFC','PFIZER','PIDILITIND','PIIND','PNB','POLYCAB','POWERGRID','PVR',
           'RAMCOCEM','RBLBANK','RECLTD','RELIANCE','SAIL','SBILIFE','SBIN','SHREECEM','SIEMENS','SRF','SRTRANSFIN','STAR','SUNPHARMA','SUNTV','SYNGENE','TATACHEM','TATACONSUM','TATAMOTORS','TATAPOWER','TATASTEEL','TCS','TECHM','TITAN','TORNTPHARM','TORNTPOWER','TRENT','TVSMOTOR','UBL','ULTRACEMCO','UPL','VEDL','VOLTAS','WIPRO','ZEEL'];
getStockData(namesList)
# getStockData("IEX")
# getStockData("SBIN")
print("-----------")
data_file = open('C:\\my_data\\testlogs\\optiondata.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
count = 0
for s in stockdata:
    if count == 0:
        # Writing headers of CSV file
        header = s.keys()
        # print(header)
        csv_writer.writerow(header)
        count += 1

        # Writing data of CSV file
    csv_writer.writerow(s.values())
    # print(s.values())
data_file.close()