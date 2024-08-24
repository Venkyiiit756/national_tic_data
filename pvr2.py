import requests

# Define the API endpoint
url = "https://api3.inoxmovies.com/api/v1/booking/content/msessions"

# Define the payload for the POST request
payload = {
    "city": "Hyderabad",
    "mid": "28563",
    "experience": "ALL",
    "lat": "17.1827790564",
    "lng": "78.60351551",
    "lang": "ALL",
    "format": "ALL",
    "dated": "NA",
    "time": "08:00-24:00",
    "cinetype": "ALL",
    "hc": "ALL",
    "adFree": False
}

# Set headers to match the fetch request
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "appversion": "1.0",
    "authorization": "Bearer",  # You may need to provide a valid token if required
    "chain": "INOX",
    "city": "Hyderabad",
    "content-type": "application/json",
    "country": "INDIA",
    "platform": "WEBSITE",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site"
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()
    print(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
