import os
import csv
import psycopg2



# Please replace with your user name password if it is not correct
conn = psycopg2.connect(database = "postgres", user = "postgres", password = "postgresn", host = "localhost", port = "5432")
print("Opened database successfully")


def sqlCovert(row):
    # return "insert into market.rawdata(script,dt,open_price,high_price,low_price,close_price) values('{0[0]}',TO_TIMESTAMP('{0[1]} {0[2]}','YYYYMMDD HH24:MI' ),{0[3]},{0[4]},{0[5]},{0[5]});".format(row)
    return "insert into raw_equity (tdate,symbol,series,open,high,low,close,last,preclose,tottrdqty,tottrdval) values (to_date('{0[10]}','DD-MON-YY'),'{0[0]}','{0[1]}',{0[2]},{0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{0[8]},{0[9]});".format(row)
    # return row

cur = conn.cursor()

def insertRecord(param):
    cur.execute(param)
    # print(param)

# Please enter folder path here
entries = os.listdir('/my_data/bhav/eq-data')
for entry in entries:
    with open('/my_data/bhav/eq-data/' + entry , newline='') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        isFirst = 0
        for row in reader:
            if isFirst !=0:
                print(sqlCovert(row))
                insertRecord(sqlCovert(row))
            else:
                isFirst=1

        print(entry)
        conn.commit()


conn.commit()
conn.close()