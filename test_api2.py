#https://tickets.fandango.com/checkoutapi/showtimes/v2/465031122/seat-map?_=1724423412890
#https://tickets.fandango.com/checkoutapi/showtimes/v2/465587968/seat-map?_=1724423482045

import requests

# API endpoint from the image
url = "https://tickets.fandango.com/checkoutapi/showtimes/v2/465886453/seat-map/"

# Headers based on the information from your image
headers = {
    "authority": "tickets.fandango.com",
    "method": "GET",
    # "path": "/checkoutapi/showtimes/v2/465838045/seat-map?_=1724592022492/",
    "scheme": "https",
    "accept": "application/json, text/javascript, /; q=0.01",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "Authorization": "88P0w1Wk+WKqvoAjJBQbleHMJNRNL/lJBSJz2T/FQyw=.AQIDAHgkc5RGKnQifqNqiweNhz0UT2qkcIy+a2GG20Ti1kCgwAG04bPArNEyxYu9Nqsg98aRAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQM7VO5F3uUbWpsjOz+AgEQgDudCm8gCH6Qc5x5gWSe8eLOQa3NzqY7X1UGPc66OG9DXhFjJmRsjanwcFzpbQGp9RM/5Qra3pc7IVBM0g==.AQICAHigoaP0OXDFv1Ks5GINY4qfauMYrwQSiyX+5jjiYKmXvgEU1Dmm3IB3g5wEjXF052qfAAAAgzCBgAYJKoZIhvcNAQcGoHMwcQIBADBsBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDJi8gqtWmIC7XT2OIAIBEIA/pztrtOO8+eXA8mUsF8Ha3YX/Ae+sRPq9SnBBspkOtcUPwwYGICo03ejpEhR6MSjUWzXIt2hrS67WyCaUtNCu.MTcyNDU5NDUwMA==",
    "Content-Type": "application/json",
    "Referer": "https://tickets.fandango.com/mobileexpress/seatselection",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "X-Fd-Sessionid": "cl0briari0o2pozjjcglvsu5",
    "priority": "u=1, i",
    "referer": "https://tickets.fandango.com/mobileexpress/seatselection?row_count=465838045&mid=155562&chainCode=CNMK&sdate=2024-09-01+13%3A30&tid=aacbt&route=map-seat-map",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

# Send GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Success!")
    print(response.json())  # or response.text if it's not JSON
else:
    print(f"Failed with status code {response.status_code}")
    print(f"Response content: {response.text}")