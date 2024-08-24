

#https://tickets.fandango.com/checkoutapi/showtimes/v2/465031122/seat-map?_=1724423412890
#https://tickets.fandango.com/checkoutapi/showtimes/v2/465587968/seat-map?_=1724423482045

import requests

# API endpoint from the image
url = "https://tickets.fandango.com/checkoutapi/showtimes/v2/465587968/seat-map"

# Headers based on the information from your image
headers = {
    "authority": "tickets.fandango.com",
    "method": "GET",
    #"path": "/checkoutapi/showtimes/v2/465587968/seat-map?_=1724423482045",
    "scheme": "https",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Authorization": "lVbZsryZxxV9EJYQ3wMnd6tvx2KN127GEnsLKZNTfu0=.AQIDAHgkc5RGKnQifqNqiweNhz0UT2qkcIy+a2GG20Ti1kCgwAHna30msUfys2HX1k8BTt9cAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMquNqdFkspr5360pOAgEQgDs6kCK2PWdxDsfSFSQi989QzCTv9rkcKjop+MdByc+zMH56e0wEIael2DTucfxeWbzWFOQo9dfgQgT0tQ==.AQICAHigoaP0OXDFv1Ks5GINY4qfauMYrwQSiyX+5jjiYKmXvgFgdMAlS6rSpMxuuC6hOUe0AAAAgzCBgAYJKoZIhvcNAQcGoHMwcQIBADBsBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDFU/5RFwse6/WaiFVwIBEIA/pyxnlV+MsZ4LCCrL4JYvbuHJ5nbiGHJ7p/5W1JTi0Kt58wwOgdFdIutlZmgMmFPICFnsupe9jiA6FxrCd6Wc.MTcyNDQyNDY5MA==",
    "Content-Type": "application/json",
    "Referer": "https://tickets.fandango.com/mobileexpress/seatselection",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "X-Fd-Sessionid": "cl0briari0o2pozjjcglvsu5"
}

# Send GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Success!")
    print(response.json())  # or response.text if it's not JSON
else:
    print(f"Failed with status code {response.status_code}")

