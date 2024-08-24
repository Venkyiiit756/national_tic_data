import requests
import json
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
# Define the URL
url = "https://api3.inoxmovies.com/api/v1/booking/content/msessions"
#cities_list = ["Ahmedabad","Ajmer","Amritsar","Anand","Armoor","Aurangabad","Bareilly","Belgaum","Bengaluru","Bharuch","Bhilai","Bhilwara","Bhiwadi","Bhopal","Bhubaneswar","Bilaspur","Bokaro","Burdwan","Chandigarh","Chennai","Coimbatore","Cuttack","Darjeeling","Dehradun","Delhi","Delhi-NCR","Dhanbad","Dharwad","Faridabad","Gandhinagar","Ghaziabad","Goa","Gorakhpur","Greater Noida","Guntur","Gurugram","Guwahati","Gwalior","Howrah","Hubli","Hyderabad","Indore","Jaipur","Jalandhar","Jalgaon","Jammu","Jamnagar","Jodhpur","Jorhat","Kakinada","Kalyan","Kanpur","Karnal","Khanna","Kochi","Kolhapur","Kolkata","Kota","Kurnool","Latur","Lucknow","Ludhiana","Madurai","Malegaon","Mangalore","Manipal","Meerut","Mohali","Moradabad","Mumbai","Mysuru","Nadiad","Nagpur","Nanded","Narsipatnam","Nashik","Navi Mumbai","Nizamabad ","Noida","Panipat","Pathankot","Patiala","Patna","Pondicherry","Prayagraj","Pune","Raipur","Rajkot","Ranchi","Rourkela","Salem","Satna","Sri Ganganagar","Srinagar","Surat","Thane","Thrissur","Trivandrum","Tumakuru","Udaipur","Ujjain","Vadodara","Vellore","Vijayawada","Vizag","Vizianagaram","Warangal","Yamunanagar","Zirakpur"]
cities_list = ["Hyderabad"]

def call_city(city_name):
    time.sleep(0.1)
    print(f"{city_name} data extracted:;")
    """form_data = {
        'lat': '17.1827790564',
        'lng': '78.60351551',
        'city': city_name,
        'av': '5.1',
        'pt': 'WEBSITE',
        'did': '49175263211697553062677',
        'userid': '0',
        'date': '2024-08-22',
        'mid': '30971'
    }"""

    form_data = {
        "city": city_name,
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
        "adFree": 'false'
    }

    # leo - NHO00022370
    # bk - NHO00017083

    response = requests.post(url, data=form_data)
    shows_count = 0
    total_ticks = 0
    ava_tickets = 0

    try:
        if response.status_code == 200:
            resp = json.loads(response.text)
            th_list = resp['output']["cinemas"]

            for th in th_list:
                th_name = th["cn"]
                shows = th["childs"][0]["sws"][0]["s"]
                for each_show in shows:
                    st = each_show["st"]
                    total_ticks += each_show["ts"]
                    ava_tickets += each_show["as"]
                    # print(f"{th_name}: {st}")
                    shows_count += 1
        else:
            print(f"POST request failed with status code {response.text}")
    except Exception as ex:
        print(f"No Shows in city {city_name}")
    return {
        "city_name": city_name,
        "shows": shows_count,
        "total_tickets": total_ticks,
        "booked_tickets": total_ticks - ava_tickets,
        "ava_tickets": ava_tickets
    }


data = [call_city(each) for each in cities_list]
df = pd.DataFrame(data)

# remove rows where tickets aren't opened yet

df = df[df['total_tickets'] != 0]

df['Tickets booked %'] = (df['booked_tickets']/df['total_tickets']) * 100
df['Tickets booked %'] = round(df['Tickets booked %'], 2)

df.sort_values(by='Tickets booked %', ascending=False, inplace=True)

df = df.reset_index(drop=True)

print(f"\nTotal Tickets {df['total_tickets'].sum()}")
print(f"Total Shows {df['shows'].sum()}")
print(f"Booked Tickets {df['booked_tickets'].sum()}")
#print(f"Overall % {round((df['booked_tickets'].sum()/df['total_tickets'].sum()) * 100, 2)}")

print(df)
