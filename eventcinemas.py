import requests

# Using print statements instead of logging
url = "https://www.eventcinemas.com.au/Cinemas/GetSessions"
params = {
    'cinemaIds': ['17', '19', '22', '43', '49', '56', '66', '81'],
    'date': '2024-09-02'
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

try:
    print("Starting GET request to Event Cinemas API")
    response = requests.get("https://www.eventcinemas.com.au/api/ticketing/session?sessionId=13948813&bookingSource=www%7Cmovies&includeSuggestedOnlyAddons=true&supportedPaymentProviders=1&supportedPaymentProviders=2&supportsModifierGroupSplit=true&isMobile=true/")
    response.raise_for_status()  # Check if the request was successful
    print(f"Request successful, status code: {response.status_code}")
    
    data = response.json()  # Parse the response as JSON
    print("Successfully parsed JSON response")
    result = data  # Store the response data
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    result = f"An error occurred: {e}"

result
