# MarketAssist
Stock market related tools


#Database 

### Sql Commnads

Create schema market;
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

### Queries
