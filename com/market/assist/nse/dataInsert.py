import os
import csv
import psycopg2



# Please replace with your user name password if it is not correct
conn = psycopg2.connect(database = "postgres", user = "admin", password = "admin", host = "localhost", port = "5432")
print("Opened database successfully")


def sqlCovert(row):
    # return "insert into market.rawdata(script,dt,open_price,high_price,low_price,close_price) values('{0[0]}',TO_TIMESTAMP('{0[1]} {0[2]}','YYYYMMDD HH24:MI' ),{0[3]},{0[4]},{0[5]},{0[5]});".format(row)
    return "insert into  market.rawfnodata  (INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_OI,trandate) values ('{0[0]}','{0[1]}','{0[2]}',{0[3]},'{0[4]}',{0[5]},{0[6]},{0[7]},{0[8]},{0[9]},{0[10]},{0[11]},{0[12]},'{0[13]}','{0[14]}');".format(row)

cur = conn.cursor()

def insertRecord(param):
    cur.execute(param)
    # print(param)

# Please enter folder path here
entries = os.listdir('E:\\data\\historicaldata\\extract')
for entry in entries:
    with open('E:\\data\\historicaldata\\extract\\' + entry , newline='') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        isFirst = 0
        for row in reader:
            if isFirst !=0:
                insertRecord(sqlCovert(row))
            else:
                isFirst=1

        print(entry)
        conn.commit()


conn.commit()
conn.close()