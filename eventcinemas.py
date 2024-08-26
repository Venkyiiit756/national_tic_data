
#read the api from the website
import requests

response = requests.get('https://www.eventcinemas.com.au/Cinemas/GetSessions?cinemaIds=66&date=2024-09-02')

# validate the response
if response.status_code == 200:
    # log the status code the zip code and the date and url
    print(f"Status Code: {response.status_code}")
    #print(f"Date: {date}")
    # print the request url
    print(f"URL: {response.url}")
    #print(f"Status Code: {response.status_code}")
    #print(response.json())  # Return JSON response if successful
else:
    print({"error": f"Failed to retrieve data: {response.status_code}"})