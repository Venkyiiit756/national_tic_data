import requests
import pandas as pd

def get_theaters_with_showtimes(zip_code, date, page=1, limit=10):
    base_url = "https://www.fandango.com/napi/theaterswithshowtimes"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Referer": f"https://www.fandango.com/{zip_code}_movietimes?date={date}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "If-None-Match": "W/\"3b3df-OoS/JgEj2u373uy1h9mayOiq9Jo\""
    }
    
    params = {
        "zipCode": zip_code,
        "city": "",
        "state": "",
        "date": date,
        "page": page,
        "favTheaterOnly": "false",
        "limit": limit,
        "isdesktop": "true",
        "filter": "open-theaters",
        "filterEnabled": "true",
        "expandedSearch[useExpanded]": "false",
        "expandedSearch[setExpanded]": "",
        "partnerRestrictedTicketing": "",
        "joinNowURL": f"https://www.fandango.com/accounts/join-now?from=https://www.fandango.com/{zip_code}_movietimes?date={date}"
    }
    
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # Return JSON response if successful
    else:
        return {"error": f"Failed to retrieve data: {response.status_code}"}

# Example usage:
zip_code = "75093"
date = "2024-09-01"
page = 1
limit = 10

data = get_theaters_with_showtimes(zip_code, date, page, limit)

# Print the fetched data
#print(theaters_data)


# Reading the file content as a string to inspect and process the JSON-like structure
"""with open(file_path, 'r') as file:
    file_content = file.read()"""

# Converting the JSON-like content into a Python dictionary using eval (since it's likely a Python dictionary format)
#data = eval(theaters_data)

# Re-checking the structure of the data related to 'id': 155562 from the newly loaded content
for theater in data['theaters']:
    for movie in theater.get('movies', []):
        if movie.get('id') == 155562:
            movie_data = movie
            break

# Extracting the required fields from the reloaded data
showtime_details = []
for variant in movie_data.get('variants', []):
    for amenity_group in variant.get('amenityGroups', []):
        for showtime in amenity_group.get('showtimes', []):
            showtime_details.append({
                'showtime_id': showtime.get('id'),
                'date': showtime.get('ticketingDate', 'N/A'),
                'showtime_hash_code': showtime.get('showtimeHashCode', 'N/A'),
                'ticket_jump_url': showtime.get('ticketingJumpPageURL', 'N/A')
            })

# Creating a DataFrame and displaying it to the user
df_showtime_details = pd.DataFrame(showtime_details)
print(df_showtime_details)
#tools.display_dataframe_to_user(name="Showtime Details from Corrected JSON", dataframe=df_showtime_details)

