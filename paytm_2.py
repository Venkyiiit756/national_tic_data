import json
import openpyxl

# Define the path to the JSON file
json_file_path = "paytm_hyd_aug31_2103.json"

# Load the JSON data from the file
with open(json_file_path, "r") as file:
    data = json.load(file)

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
for cinema in data["meta"]["cinemas"]:
    theater_name = cinema["name"]
    cinema_id = str(cinema["id"])
    sessions = data["pageData"]["sessions"][cinema_id]
    
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
output_file_path = 'Theater_Data_with_hyd_aug31_21.xlsx'
workbook.save(output_file_path)

output_file_path
