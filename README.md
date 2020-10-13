# MarketAssist
Stock market related tools


#Database 

### Sql Commnads

###Create schema market;
------------
CREATE TABLE   rawdata (
   rawid serial PRIMARY KEY,
   script varchar(50),
   dt TIMESTAMP,
   open_price decimal,
   high_price decimal,
   low_price decimal,
   close_price decimal
);
-------------------
### tabel for fno bhav copy
create table market.rawfnodata (
INSTRUMENT varchar,
SYMBOL varchar,
EXPIRY_DT date,
STRIKE_PR decimal,
OPselect count(*)  from market.rawfnodata
TION_TYP varchar,
OPEN decimal,HIGH decimal ,LOW decimal ,CLOSE decimal ,
SETTLE_PR decimal ,CONTRACTS decimal,VAL_INLAKH decimal ,OPEN_INT decimal ,CHG_IN_OI decimal ,trandate date)
)
### Queries
--to create sub table for a synbol
create table  market.bankniftyfnodata as select d.instrument,d.symbol,d.expiry_dt,d.strike_pr,d.option_typ,d.open,d.high,low,d.close,d.settle_pr,d.contracts,d.val_inlakh,d.open_int,d.chg_in_oi,d.trandate,x.close as f_close
 from market.rawfnodata d
 join (select trandate,symbol,expiry_dt,close from market.rawfnodata  x where   x.instrument='FUTIDX' and x.option_typ='XX') x
 on (d.symbol=x.symbol and d.expiry_dt=x.expiry_dt and d.trandate=x.trandate )
 where d.symbol='BANKNIFTY';

-- to get the ATM Strike
select   instrument,symbol,expiry_dt,strike_pr,option_typ,open,high,low,close,settle_pr,contracts,val_inlakh,open_int,chg_in_oi,trandate,f_close
 from bankniftyfnodata 
where  instrument='OPTIDX' and strike_pr=f_close-mod(f_close,100);

-- this query buy on first day of the month and wait till expiry
select   d.instrument,d.symbol,d.expiry_dt,d.strike_pr,d.option_typ,round((d.open+d.close)/2,0) as buy,ed.high as sell,d.settle_pr,d.contracts,d.val_inlakh,d.open_int,d.chg_in_oi,d.trandate,d.f_close
,ed.trandate,ed.high
 from bankniftyfnodata d
JOIN (select   MIN(trandate) as STARTDATE,MAX(expiry_dt) as ENDDATE 
 from bankniftyfnodata 
where  instrument='OPTIDX' and strike_pr=f_close-mod(f_close,100)  
group by to_char(trandate,'YYYYMM')) dt
on (dt.STARTDATE= d.trandate)
left join bankniftyfnodata ed 
on (d.expiry_dt=ed.trandate and d.symbol=ed.symbol and d.expiry_dt=ed.expiry_dt and d.strike_pr=ed.strike_pr and d.option_typ=ed.option_typ ) 
where  d.instrument='OPTIDX' and d.strike_pr=d.f_close-mod(d.f_close,100) 
order by d.expiry_dt


