#https://tickets.fandango.com/checkoutapi/showtimes/v2/465031122/seat-map?_=1724423412890
#https://tickets.fandango.com/checkoutapi/showtimes/v2/465587968/seat-map?_=1724423482045

import requests



# Headers based on the information from your image
headers = {
    "authority": "tickets.fandango.com",
    "method": "GET",
    # "path": "/checkoutapi/showtimes/v2/465838045/seat-map?_=1724592022492/",
    "scheme": "https",
    "accept": "application/json, text/javascript, /; q=0.01",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "Authorization": "WF/rN8gHWDzBT8pEW6bzbM8Zrlxg3t/XhRlNybIpnEQ=.AQIDAHgkc5RGKnQifqNqiweNhz0UT2qkcIy+a2GG20Ti1kCgwAHzM/PEI892xBZZmkjYiL5MAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMsRMFpR9mURYOYFu9AgEQgDtu0h1roPMPgS/PkkAcUyGdhLjcD5Mh3kuliRGWB2s7ghkbT9Q9RXw06qNwk/8tcYRcgnL7xQyeYNSNgw==.AQICAHigoaP0OXDFv1Ks5GINY4qfauMYrwQSiyX+5jjiYKmXvgExC8ownpAMd9FTNbWkxCqEAAAAgzCBgAYJKoZIhvcNAQcGoHMwcQIBADBsBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDIre7uNJUY+n7AE+fAIBEIA/9fvOzbq+Is/XHy2rHNFx18MJWFRuE3DJMUNXaU511xUGOrhaOLrtL3wTpmriE9pvPGHSI3DEEBIdcNkIxzkr.MTcyNDYxNDQ3MA==",
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

"""
showtimeId = "465886453"
 # API endpoint from the image
url = "https://tickets.fandango.com/checkoutapi/showtimes/v2/"+showtimeId+"/seat-map/"
    
# Send GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Success!")
    print(response.json())  # or response.text if it's not JSON
    responseJson = response.json()
    resposneData = responseJson['data']
    print(resposneData['showtimeId'])
    print(resposneData['totalAvailableSeatCount'])
    print(resposneData['totalSeatCount'])
else:
    print(f"Failed with status code {response.status_code}")
    print(f"Response content: {response.text}")"""


# read the movieDetailList.json file
import json
with open('movieDetailList.json') as f:
  data = json.load(f)
  
# print the data length
print(len(data))

#print the data keys
print(data[0].keys())

fullshowdetails = []

#iterate through the data
for i in range(len(data)):
        #iterate of the showtimes
        for showtime in data[i]['showtimes']:
            
            # append multiple values to the fullshowdetails
            fullshowdetails.append({
                'state': data[i]['state'],
                'city': data[i]['city'],
                'theater_name': data[i]['theater_name'],
                'showtime_id': showtime['showtime_id'],
                'date': showtime['date']
            })
                

#final list
finallist = []


#print the type of object
print(type(fullshowdetails))


#print the length of the fullshowdetails
print(len(fullshowdetails))

#print the fullshowdetails
#print(fullshowdetails)



#itearte through the show in the fullshowdetails
for show in fullshowdetails:
    showtimeId = str(show['showtime_id'])
    
    # API endpoint from the image
    #url = "https://tickets.fandango.com/checkoutapi/showtimes/v2/{showtimeId}/seat-map/"
    url = "https://tickets.fandango.com/checkoutapi/showtimes/v2/"+showtimeId+"/seat-map/"
    
    #send the get request
    response = requests.get(url, headers=headers)
    #check the response
    if response.status_code == 200:
        print("Success!")
        responseJson = response.json()
        responseData = responseJson['data']
        
        #append the responsedata's totalAvailableSeatCount to fullshowdetails
        show['totalAvailableSeatCount'] = responseData['totalAvailableSeatCount']
        #append the responsedata's totalSeatCount to fullshowdetails
        show['totalSeatCount'] = responseData['totalSeatCount']
    else:
        print(f"Failed with status code {response.status_code}")
        print(f"Response content: {response.text}")

#print the fullshowdetails
print(fullshowdetails)
