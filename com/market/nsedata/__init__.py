import requests

url_oc = "https://www.nseindia.com/option-chain"
# url = f"https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
url = f"https://www.nseindia.com/api/option-chain-equities?symbol=SBIN"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
session = requests.Session()
request = session.get(url_oc, headers=headers, timeout=5)
cookies = dict(request.cookies)
response = session.get(url, headers=headers, timeout=5, cookies=cookies)
print(response.json())
