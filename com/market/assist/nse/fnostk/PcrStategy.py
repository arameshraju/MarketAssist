# PCR Stategy
import psycopg2

conn = psycopg2.connect(database = "postgres", user = "postgres", password = "postgresn", host = "localhost", port = "5432")
print("Opened database successfully")
fnocur = conn.cursor()
stkcur = conn.cursor()
# List of fno Stocks
fnolist="select distinct symbol from market.fnodata d where instrument='FUTSTK' and symbol='ACC'"
stkdata="with fno as (select " \
       "instrument,symbol,expiry_dt,strike_pr,option_typ,open,high,low,close,open_int,chg_in_oi,trandate" \
       ",(SELECT SUM(open_int) FROM market.fnodata s where s.INSTRUMENT= d.INSTRUMENT and d.expiry_dt >= s.expiry_dt and   s.symbol=d.symbol and s.trandate=d.trandate) as coi" \
       ",(SELECT SUM(open_int) FROM market.fnodata s where s.INSTRUMENT= 'OPTSTK' and s.option_typ='CE' and d.expiry_dt  >= s.expiry_dt and    s.symbol=d.symbol and s.trandate=d.trandate) as CE_OI" \
       ",(SELECT SUM(open_int) FROM market.fnodata s where s.INSTRUMENT= 'OPTSTK' and s.option_typ='PE' and d.expiry_dt >= s.expiry_dt and   s.symbol=d.symbol and s.trandate=d.trandate) as PE_OI" \
       ",(SELECT SUM(chg_in_oi) FROM market.fnodata s where s.INSTRUMENT= d.INSTRUMENT and d.expiry_dt >= s.expiry_dt and    s.symbol=d.symbol and s.trandate=d.trandate) as coi_ch" \
       ",(SELECT SUM(chg_in_oi) FROM market.fnodata s where s.INSTRUMENT= 'OPTSTK' and d.expiry_dt >= s.expiry_dt and s.option_typ='CE' and   s.symbol=d.symbol and s.trandate=d.trandate) as CE_OI_ch" \
       ",(SELECT SUM(chg_in_oi) FROM market.fnodata s where s.INSTRUMENT= 'OPTSTK' and d.expiry_dt >= s.expiry_dt  and s.option_typ='PE' and   s.symbol=d.symbol and s.trandate=d.trandate) as PE_OI_ch" \
       ",(SELECT SUM(open_int) FROM market.fnodata s where s.INSTRUMENT= 'OPTSTK' and s.option_typ='CE' and d.expiry_dt  >= s.expiry_dt and    s.symbol=d.symbol and s.trandate=d.trandate and s.strike_pr between d.close*0.8 and d.close*1.2  ) as CE_OI_30" \
       ",(SELECT SUM(open_int) FROM market.fnodata s where s.INSTRUMENT= 'OPTSTK' and s.option_typ='PE' and d.expiry_dt >= s.expiry_dt and   s.symbol=d.symbol and s.trandate=d.trandate  and s.strike_pr between d.close*0.8 and d.close*1.2   ) as PE_OI_30" \
       " from market.fnodata d " \
       "where instrument='FUTSTK'   AND expiry_dt='2021-05-27'and trandate>'2021-04-29')  " \
       "select  trandate,symbol,expiry_dt,open,high,low,close " \
       ",round(pe_oi/ce_oi,2) as pcr ,round(pe_oi_30/ce_oi_30,2) as pcr30  " \
       "from fno WHERE symbol='{0}'"

fnocur.execute(fnolist)
data = fnocur.fetchall()
for x in data:
    # print( x[0] )
    # print(stkdata.format( x[0]))
    stkcur.execute(stkdata.format( x[0]))
    stk = stkcur.fetchall()
    action=""
    preaction=""
    for s in stk:
        preaction=action
        if(s[8]>s[7] and s[7] > 0.8 ):
            action="buy"
        elif (s[8]< s[7] and s[7] < 0.8):
            action = "sell"
        else:
            action = ""
        if(preaction=="buy" and (s[8]<s[7] or s[7]<=0.8)):
            action="exit"
        if(preaction=="sell" and (s[8]>s[7] or s[7]>0.8)):
            action="exit"

        if(preaction!=action):
            print(str(s[0]) + "," + s[1] + "," +  str(s[3]) + "," +  str(s[6]) + "," + str(s[7])+ "," + str(s[8])+","+action )

