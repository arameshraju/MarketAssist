import os
import csv
import psycopg2



# Please replace with your user name password if it is not correct
conn = psycopg2.connect(database = "postgres", user = "postgres", password = "postgresn", host = "localhost", port = "5432")
print("Opened database successfully")


def sqlCovert(row):
    # return "insert into market.rawdata(script,dt,open_price,high_price,low_price,close_price) values('{0[0]}',TO_TIMESTAMP('{0[1]} {0[2]}','YYYYMMDD HH24:MI' ),{0[3]},{0[4]},{0[5]},{0[5]});".format(row)
    return "insert into rawfnodata (instrument,symbol,expiry_dt,strike_pr,option_typ,open,high,low,close,settle_pr,contracts,val_inlakh,open_int,chg_in_oi,trandate) values ('{0[0]}','{0[1]}',to_date('{0[2]}','DD-MON-YY'),{0[3]},'{0[4]}',{0[5]},{0[6]},{0[7]},{0[8]},{0[9]},{0[10]},{0[11]},{0[12]},{0[13]},to_date('{0[14]}','DD-MON-YY'));".format(row)
    # return row

cur = conn.cursor()

def insertRecord(param):
    cur.execute(param)
    # print(param)
def executeQuery(param):
    cur.execute(param)


executeQuery("delete from rawfnodata")

# Please enter folder path here
entries = os.listdir('/my_data/fno/fno-data')
for entry in entries:
    with open('/my_data/fno/fno-data/' + entry , newline='') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        isFirst = 0
        for row in reader:
            if isFirst !=0:
                # print(sqlCovert(row))
                insertRecord(sqlCovert(row))
            else:
                isFirst=1

        print(entry)
        conn.commit()

# https://www.nseindia.com/api/option-chain-equities?symbol=IRCTC

# Insert into fnodata tables
sqlInsertfnodata="insert into market.fnodata " \
                 " select distinct  instrument,symbol,expiry_dt,strike_pr,option_typ,open,high,low,close,settle_pr,contracts,val_inlakh,open_int,chg_in_oi,trandate " \
                 " from rawfnodata"
insertRecord(sqlInsertfnodata)



conn.commit()
conn.close()