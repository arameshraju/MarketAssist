import psycopg2

# Variable

# Actual code
conn = psycopg2.connect(database="postgres", user="admin", password="admin", host="localhost", port="5432")
cur = conn.cursor()
cur2 = conn.cursor()
def getSrikePrice(srike,expiry,optType,tranDate):
    QRY_STR= "select close from market.bankniftyfnodata  where strike_pr=" + srike +" and expiry_dt='"+ expiry+"' and  option_typ='"+optType+"' AND trandate='"+tranDate+"'"
    # print(QRY_STR)
    cur2.execute(QRY_STR)
    # cur2.execute("select close from market.bankniftyfnodata  where strike_pr=35400  and expiry_dt='2020-01-30' and  option_typ='CE' AND trandate='2020-01-16'")
    data = cur2.fetchall()
    for x in data:
        return  x[0]

def getATM(expiry,optType,trndt ):
    QRY_STR="select to_char(trandate,'YYYY-MM-DD') as trandate,to_char(expiry_dt,'YYYY-MM-DD') as expiry_dt,cast(strike_pr as text) as strike_pr,option_typ,cast(close as text) as close,cast(f_close as text) as f_close from  market.bankniftyfnodata  where   expiry_dt='"+expiry+"' and  option_typ='"+optType+"' AND trandate='"+trndt+"'  and strike_pr=(f_close - mod(f_close,100))"
    # print(QRY_STR)
    cur2.execute(QRY_STR)
    data = cur2.fetchall()
    for x in data:
        return  x

def getFuturePrice(expiry,tranDate):
    QRY_STR= "select close from market.bankniftyfnodata  where   expiry_dt='"+ expiry+"' and  option_typ='XX' AND trandate='"+tranDate+"'"
    # print(QRY_STR)
    cur2.execute(QRY_STR)
    # cur2.execute("select close from market.bankniftyfnodata  where strike_pr=35400  and expiry_dt='2020-01-30' and  option_typ='CE' AND trandate='2020-01-16'")
    data = cur2.fetchall()
    for x in data:
        return  x[0]


Query_expireDates  ="select to_char(max(trandate),'YYYY-MM-DD') as ed, to_char(expiry_dt,'YYYY-MM-DD') AS ex from market.bankniftyfnodata f where  f.trandate <=expiry_dt  group by expiry_dt order by  expiry_dt"
cur.execute(Query_expireDates)
ex_reords = cur.fetchall()
isFirst=0
print('TransDate', ',', 'Expiry', ',', 'Stike', ',', 'OptType', ',', 'Opt_Price', ',', 'FutureStart', ',', 'Opt_Close',
      ',', 'Future_close')

for ex in ex_reords:
    if isFirst== 0:
        preDt=ex[0]
        isFirst=1
    else:
        # print( preDt," ", ex[0], " ", ex[1], " ")
        entry = getATM(ex[1]+'', 'CE', preDt+'')
        print(entry[0],',',entry[1],',',entry[2],',',entry[3],',',entry[4],',',entry[5],',',getSrikePrice(entry[2], ex[1], entry[3], ex[0]),',',getFuturePrice(ex[1],ex[0]))
        entry = getATM(ex[1]+'', 'PE', preDt+'')
        print(entry[0],',',entry[1],',',entry[2],',',entry[3],',',entry[4],',',entry[5],',',getSrikePrice(entry[2], ex[1], entry[3], ex[0]),',',getFuturePrice(ex[1],ex[0]))
        # print(getSrikePrice(entry[2], ex[1], entry[3], ex[0]))
        preDt = ex[0]



# print(getSrikePrice('35400','2020-01-30','CE','2020-01-16'))
# print(getATM('2020-01-30','CE','2020-01-16'))




