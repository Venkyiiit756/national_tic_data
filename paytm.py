import json
import openpyxl
import requests

# Define the API endpoint

city = "chennai"
api_url = "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=2&city="+city+"&movieCode=o0gvbyvmx&version=3&site_id=6&channel=HTML5&child_site_id=370&client_id=ticketnew&clientId=ticketnew"

# Fetch the JSON data from the API
response = requests.get(api_url)
data = response.json()

# Create a new Excel workbook and add sheets
workbook = openpyxl.Workbook()
sheet1 = workbook.active
sheet1.title = "Sheet1"
sheet2 = workbook.create_sheet(title="Sheet2")

# Write headers for Sheet1
sheet1_headers = ["Theater name", "Audi", "ShowTime", "Label", "sAvailTickets", "sTotalTickets", "sBookedTickets", "Price", "sTotalGross", "sBookedGross"]
sheet1.append(sheet1_headers)

# Write headers for Sheet2
sheet2_headers = ["Theater name", "Audi", "Showtime", "AvailableTickets", "TotalTickets", "BookedTickets", "TotalGross", "BookedGross"]
sheet2.append(sheet2_headers)

# Extract data from JSON
cinema_data = data["meta"]["cinemas"][0]
sessions = data["pageData"]["sessions"][str(cinema_data["id"])]

theater_name = cinema_data["name"]

for session in sessions:
    audi = session["audi"]
    show_time = session["showTime"]
    
    for area in session["areas"]:
        label = area["label"]
        sAvailTickets = area["sAvail"]
        sTotalTickets = area["sTotal"]
        price = area["price"]
        sBookedTickets = sTotalTickets - sAvailTickets
        
        sTotalGross = sTotalTickets * price
        sBookedGross = sBookedTickets * price
        
        # Write to Sheet1
        sheet1.append([theater_name, audi, show_time, label, sAvailTickets, sTotalTickets, sBookedTickets, price, sTotalGross, sBookedGross])
        
        # Write to Sheet2 (adjusting headers for general terms)
        sheet2.append([theater_name, audi, show_time, sAvailTickets, sTotalTickets, sBookedTickets, sTotalGross, sBookedGross])

# Save the workbook
output_file_path = city+'Theater_Data_with_API.xlsx'
workbook.save(output_file_path)

print(f"Excel file has been saved to {output_file_path}")

