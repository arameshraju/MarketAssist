import alpha_vantage.timeseries

ts = TimeSeries(key='222LKR459HRSY5I8')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_daily('SBI.BSE')
print(data)

