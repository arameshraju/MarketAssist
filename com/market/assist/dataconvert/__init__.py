import os
import csv
import psycopg2

conn = psycopg2.connect(database = "postgres", user = "admin", password = "admin", host = "localhost", port = "5432")
print("Opened database successfully")


def sqlCovert(row):
    return "insert into market.rawdata(script,dt,open_price,high_price,low_price,close_price) values('{0[0]}',TO_TIMESTAMP('{0[1]} {0[2]}','YYYYMMDD HH24:MI' ),{0[3]},{0[4]},{0[5]},{0[5]});".format(row)

cur = conn.cursor()

def insertRecord(param):
    cur.execute(param)
    #print(param)

entries = os.listdir('D:\\marketData\\Consolidated/')
for entry in entries:
    with open('D:\\marketData\\Consolidated\\' + entry , newline='') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            insertRecord(sqlCovert(row))

        print(entry)
        conn.commit()


conn.commit()
conn.close()