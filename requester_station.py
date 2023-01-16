import requests

url = "http://192.168.204.54:8015"

res = requests.get(url)

if res.status_code == 200:
	print(res.json())
