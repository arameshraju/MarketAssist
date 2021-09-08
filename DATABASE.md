# DATABASE 

###CREATE TABLES
it also has history table as fnodata_HIST

create table  market.fnodata (
INSTRUMENT varchar,
SYMBOL varchar,
EXPIRY_DT date,
STRIKE_PR decimal,
OPTION_TYP varchar,
OPEN decimal,HIGH decimal ,LOW decimal ,CLOSE decimal ,
SETTLE_PR decimal ,CONTRACTS decimal,VAL_INLAKH decimal ,OPEN_INT decimal ,CHG_IN_OI decimal ,trandate date,
PRIMARY KEY (INSTRUMENT, SYMBOL, EXPIRY_DT,STRIKE_PR,OPTION_TYP,trandate)
)
### contracts table
create table market.active_contract as 
 SELECT symbol,trandate,min(expiry_dt) as curr_expiry FROM market.fnodata_hisT
group by  symbol,trandate;

### temporty fno table for specific symbol
--create table market.temp_fnodata as 

delete from market.temp_fnodat;

insert into market.temp_fnodat
select f.trandate,f.instrument,f.symbol,f.expiry_dt,f.strike_pr,f.option_typ,f.open,f.high,f.low,f.close,f.settle_pr,f.contracts,f.val_inlakh,f.open_int,
f.chg_in_oi 
 from  market.fnodata_hist f
where f.symbol='SBIN'

### Temporory fno table with oi
create table market._temp_fno as
select f.trandate,f.instrument,f.symbol,f.expiry_dt,f.strike_pr,f.option_typ,f.open,f.high,f.low,f.close,f.settle_pr,f.contracts,f.val_inlakh,f.open_int,
f.chg_in_oi,c.curr_expiry
,(select SUM(x.open_int) from  market.temp_fnodata x WHERE x.symbol=f.symbol AND instrument='FUTSTK'  AND  f.trandate=x.trandate) as COI
,(select x.strike_pr from  market.temp_fnodata x WHERE x.symbol=f.symbol AND instrument='OPTSTK'AND option_typ='CE' AND   f.trandate=x.trandate ORDER BY open_int DESC limit 1) as CE_RES
,(select x.strike_pr from  market.temp_fnodata x WHERE x.symbol=f.symbol AND instrument='OPTSTK'AND option_typ='PE' AND   f.trandate=x.trandate ORDER BY open_int DESC limit 1) as PE_SUP
,(select SUM(x.open_int) from  market.temp_fnodata x WHERE x.symbol=f.symbol AND instrument='OPTSTK'AND option_typ='CE' AND  f.trandate=x.trandate) as CE_OI
,(select SUM(x.open_int) from  market.temp_fnodata x WHERE x.symbol=f.symbol AND instrument='OPTSTK'AND option_typ='PE' AND  f.trandate=x.trandate) as PE_OI
from  market.temp_fnodata f
join  market.active_contract c on (f.trandate=c.trandate  and  f.symbol=c.symbol)
where f.symbol='SBIN' AND instrument='FUTSTK'
and f.expiry_dt=c.curr_expiry