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
        # log the status code the zip code and the date and url
        print(f"Zip Code: {zip_code}")
        #print(f"Date: {date}")
        # print the request url
        #print(f"URL: {response.url}")
        #print(f"Status Code: {response.status_code}")
        return response.json()  # Return JSON response if successful
    else:
        return {"error": f"Failed to retrieve data: {response.status_code}"}

# Example usage:
#zip_code = "75093"
date = "2024-09-01"
page = 1
limit = 40

zip_code_list = []

#declare the theaterlist variable to store required theaters data
theaterlist = []

# read zip code list from file
with open('zipcodes.txt', 'r') as file:
    #fill the zip code list
    zip_code_list = file.read().splitlines()
    

movieDetailList = []

# process the zip code list
for zip_code in zip_code_list:
    print(f"Processing zip code: {zip_code}")
    
    pageCount = 1;
    # process this for the list of the zip codes
    data = get_theaters_with_showtimes(zip_code, date, page, limit)
    
    #print(data)
    
    #print(data.keys())
    # access the key 'theaters' from the data
    #if theaters is not present in the data, then skip the iteration
    if 'theaters' not in data:
        continue
    
    print("Total pages ================", data['pagination'].get('totalPages'))
                     
    
    for theater in data['theaters']:
        #print(theater.keys())
        for movie in theater.get('movies', []):
            if(movie.get('id') == 155562):
                #print theater name and some decoration
                print("Theater Name=============================== ", theater.get('name'))
                # add theater name to movieDetailList
                
                alreadyFound = False
                # iterate over the movieTheaterList
                for movieTheater in movieDetailList:
                    # check if the theater name is already present in the movieDetailList
                    if movieTheater.get('theater_name') == theater.get('name'):
                        # if present, then break the loop
                        alreadyFound = True
                        break
                    
                if(alreadyFound == False):
                    movieDetailList.append({
                        'theater_name': theater.get('name'),
                        'state': theater.get('state'),
                        'zip': theater.get('zip'),
                        'chainCode': theater.get('chainCode'),
                        'chainName': theater.get('chainName'),
                        'city': theater.get('city'),
                        'cityStateZip': theater.get('cityStateZip'),
                        'date': theater.get('date'),
                        'formattedID': theater.get('formattedID'),
                        'fullAddress': theater.get('fullAddress'),
                        'geo': theater.get('geo'),
                        'hasShowtimes': theater.get('hasShowtimes'),
                        'id': theater.get('id'),
                        'movieId': theater.get('id')              
                    })
                

  # Re-checking the structure of the data related to 'id': 155562 from the newly loaded content
    """for theater in data['theaters']:
        for movie in theater.get('movies', []):
            if movie.get('id') == 155562:
                # add theater data to theaterlist
                theaterlist.append({
                    'id': theater.get('id'),
                    'name': theater.get('name'),
                    'city': theater.get('city'),
                    'cityStateZip': theater.get('cityStateZip'),
                    'date': theater.get('date'),
                    'chainCode': theater.get('chainCode'),
                    'chainName': theater.get('chainName'),
                    'state': theater.get('state'),
                    'zip': theater.get('zip')
                })
                
                print(movie.get('id'))
                print(movie.get('title'))
                

                
                #fill the showtime details for each movie in the theater
                showtime_details = []
                for variant in movie.get('variants', []):
                    for amenity_group in variant.get('amenityGroups', []):
                        for showtime in amenity_group.get('showtimes', []):
                            showtime_details.append({
                                'showtime_id': showtime.get('id'),
                                'date': showtime.get('ticketingDate', 'N/A'),
                                'showtime_hash_code': showtime.get('showtimeHashCode', 'N/A'),
                                'ticket_jump_url': showtime.get('ticketingJumpPageURL', 'N/A')
                            })
                            
                # add the movie details to each theater in theater list
                theaterlist[-1]['movie'] = {
                    'id': movie.get('id'),
                    'title': movie.get('title'),
                    'runtime': movie.get('runtime'),
                    'rating': movie.get('rating'),
                    'releaseDate': movie.get('releaseDate'),
                    'showtimes': showtime_details
                }
                break
"""


"""# Extracting the required fields from the reloaded data
showtime_details = []
for variant in movie_data.get('variants', []):
    for amenity_group in variant.get('amenityGroups', []):
        for showtime in amenity_group.get('showtimes', []):
            showtime_details.append({
                'showtime_id': showtime.get('id'),
                'date': showtime.get('ticketingDate', 'N/A'),
                'showtime_hash_code': showtime.get('showtimeHashCode', 'N/A'),
                'ticket_jump_url': showtime.get('ticketingJumpPageURL', 'N/A')
            })"""

# save the theater list to as json file

#

import json

#save movieDetailList to json file
with open('movieDetailList.json', 'w') as f:
    json.dump(movieDetailList, f, indent=4)


with open('theaterlist2.json', 'w') as f:
    json.dump(theaterlist, f, indent=4)




# Creating a DataFrame and displaying it to the user
#df_showtime_details = pd.DataFrame(showtime_details)
#print(df_showtime_details)
#tools.display_dataframe_to_user(name="Showtime Details from Corrected JSON", dataframe=df_showtime_details)

