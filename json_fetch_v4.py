import os
import requests
import json
import time
import datetime
from datetime import datetime, timedelta
import pytz
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter
import zipfile

# Function to convert UTC to IST and format time
def format_showtime(utc_time_str):
    try:
        # Parse UTC time
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        utc_tz = pytz.UTC
        ist_tz = pytz.timezone('Asia/Kolkata')
        
        # Convert to IST
        utc_time = utc_tz.localize(utc_time)
        ist_time = utc_time.astimezone(ist_tz)
        
        # Format as "X AM/PM" (remove leading zeros)
        return ist_time.strftime("%-I %p")  # For Unix-based systems (Linux/Mac)
    except Exception as e:
        return utc_time_str


# Function to add total row
def add_total_row(sheet, start_row, end_row, columns_to_sum):
    # Add a total row with bold font
    total_font = Font(bold=True)
    total_fill = PatternFill(start_color="E6E6E6", end_color="E6E6E6", fill_type="solid")
    
    for col in range(1, sheet.max_column + 1):
        if col in columns_to_sum:
            formula = f'=SUM({get_column_letter(col)}{start_row}:{get_column_letter(col)}{end_row})'
            cell = sheet.cell(row=end_row + 1, column=col, value=formula)
        else:
            cell = sheet.cell(row=end_row + 1, column=col, value='')
        
        cell.font = total_font
        cell.fill = total_fill
        cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                           top=Side(style='thin'), bottom=Side(style='thin'))

    # Add "Total" text in first column
    cell = sheet.cell(row=end_row + 1, column=1, value='Total')
    cell.font = total_font
    cell.fill = total_fill
    cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                        top=Side(style='thin'), bottom=Side(style='thin'))
    cell.alignment = Alignment(horizontal="center", vertical="center")


cities = ['hyderabad', 'vijayawada']
cities = ['ahmedabad', 'ambala', 'amritsar', 'bengaluru', 'bathinda', 'bhopal', 'chandigarh', 'coimbatore', 'delhi-ncr', 'gwalior', 'hubli', 'hyderabad', 'jaipur', 'kochi', 'kolkata', 'kota', 'lucknow', 'ludhiana', 'mangalore', 'mumbai', 'panipat', 'patna', 'pune', 'surat', 'thane', 'vadodara', 'vijayawada', 'bharuch', 'anand', 'panchkula', 'dhanbad', 'aurangabad', 'nashik', 'chennai', 'vizianagaram', 'navi-mumbai', 'nagpur', 'indore', 'goa', 'raipur', 'durgapur', 'faridabad', 'burdwan', 'vizag', 'kanpur', 'belagavi', 'siliguri', 'bhubaneswar', 'udaipur', 'kalyan', 'madurai', 'greater-noida', 'jalgaon', 'manipal', 'gurgaon', 'new-delhi', 'jodhpur', 'mysuru', 'kurnool', 'bhilwara', 'ajmer', 'gandhinagar', 'rajkot', 'bhiwadi', 'thrissur', 'jorhat', 'meerut', 'allahabad', 'balaghat', 'bhilai', 'bilaspur', 'bokaro', 'dehradun', 'gandhidham', 'guwahati', 'haridwar', 'jalandhar', 'jammu', 'kalaburagi', 'kolhapur', 'latur', 'mohali', 'moradabad', 'nanded', 'neemuch', 'pathankot', 'rudrapur', 'sikar', 'ujjain', 'bhimavaram', 'alappuzha', 'trichy', 'amalapuram', 'saharanpur', 'anakapalle', 'attili', 'kozhikode', 'chilakaluripet', 'chirala', 'draksharamam', 'eluru', 'guntakal', 'guntur', 'gurazala', 'kakinada', 'kasibugga', 'macherla', 'machilipatnam', 'mandapeta', 'mylavaram', 'nandyal', 'narasaraopet', 'narsapur', 'narsipatnam', 'nellore', 'nuziveedu', 'palasa', 'parvathipuram', 'payakaraopeta', 'peddapuram', 'rajahmundry', 'ramachandrapuram', 'ravulapalem', 'samalkota', 'sattenapalle', 'srikakulam', 'tadepalligudem', 'tekkali', 'tenali', 'tiruvuru', 'vinukonda', 'vissannapeta', 'rewari', 'vijayapura', 'gadag', 'kalpetta', 'kottarakara', 'malappuram', 'mananthavady', 'manjeri', 'mukkam', 'payyanur', 'perinthalmanna', 'ponnani', 'punalur', 'tirur', 'satna', 'puducherry', 'dharapuram', 'erode', 'hosur', 'karimangalam', 'katpadi', 'komarapalayam', 'pollachi', 'rajapalayam', 'sivakasi', 'thanjavur', 'theni', 'tirunelveli', 'tirupur', 'bhuvanagiri', 'dubbak', 'godavarikhani', 'kalwakurthy', 'karimnagar', 'khammam', 'madhira', 'mancherial', 'metpally', 'miryalaguda', 'nalgonda', 'nizamabad', 'parigi', 'sangareddi', 'sathupally', 'secunderabad', 'shadnagar', 'suryapet', 'tandur', 'warangal', 'bareilly', 'gorakhpur', 'jhansi', 'muzaffarnagar', 'kanhangad', 'avinashi', 'tirupati', 'pennagaram', 'kavali', 'alwar', 'dausa', 'mathura', 'shri-ganganagar', 'salem', 'junagadh', 'jagdalpur', 'jetpur', 'ankleshwar', 'balasore', 'rewa', 'ahmednagar', 'chandrapur', 'betul', 'guna', 'sarni', 'karnal', 'asansol', 'agra', 'aligarh', 'jamshedpur', 'andul', 'howrah', 'athagarh', 'roorkee', 'ropar', 'dhamtari', 'doraha', 'ghaziabad', 'ghazipur', 'himmatnagar', 'jalpaiguri', 'kaithal', 'noida', 'loni', 'kothapeta', 'narasannapeta', 'vuyyuru', 'vapi', 'krishnagiri', 'armoor', 'bhupalapalli', 'valsad', 'gondia', 'nadiad', 'kanchipuram', 'adipur', 'kawardha', 'kondagaon', 'indapur', 'rahuri', 'gajapathinagaram', 'palluruthy', 'akola', 'amravati', 'angamaly', 'bikaner', 'chhindwara', 'dindigul', 'durg', 'rajnandgaon', 'halol', 'jamnagar', 'khandwa', 'kishangarh', 'kollam', 'kurukshetra', 'muzaffarpur', 'malout', 'patan', 'ranchi', 'sangli', 'sonipat', 'ulhasnagar', 'vasai', 'yamunanagar', 'zirakpur', 'kotkapura', 'moga', 'yavatmal', 'dabhoi', 'dahod', 'baloda-bazar', 'etawah', 'haldwani', 'barwani', 'bulandshahr', 'hisar', 'kashipur', 'bhuj', 'bellary', 'dhuri', 'kalol', 'tinsukia', 'raigarh', 'bhavnagar', 'hathras', 'surendranagar', 'palghar', 'ichalkaranji', 'abohar', 'khambhat', 'baddi', 'edappal', 'cuddalore', 'hoshiarpur', 'dasuya', 'muvattupuzha', 'udgir', 'tadipatri', 'mudhol', 'ashtamichira', 'saligram', 'pattambi', 'khanapur', 'yellandu', 'chidambaram', 'chhatarpur', 'varanasi', 'mughalsarai', 'tirumalgiri', 'deesa', 'idar', 'nagaon', 'sanand', 'kichha', 'raebareli', 'navsari', 'mehsana', 'bayad', 'siddhpur', 'shillong', 'kodaly', 'podili', 'tuticorin', 'palakonda', 'thiruvarur', 'darsi', 'kozhinjampara', 'gudivada', 'ranebennur', 'cumbum', 'palakkad', 'chamarajanagara', 'nagercoil', 'varadium', 'gorantla', 'ulundurpet', 'vijapur', 'wani', 'kullu', 'bahadurgarh', 'digras', 'dhule', 'rourkela', 'pithampur', 'ashoknagar', 'mansa', 'kekri', 'cuttack', 'davanagere', 'shivpuri', 'gadarwara', 'bhusawal', 'kopargaon', 'kalol-panchmahal', 'pendra', 'dalli-rajhara', 'mangaldoi', 'sivasagar', 'firozepur', 'kodungallur', 'hanumangarh', 'karad', 'dewas', 'gaya', 'dimapur', 'itarsi', 'beawar', 'adoni', 'unnao', 'kareli', 'dharwad', 'chitradurga', 'jind', 'bagalkot', 'ratlam', 'sagwara', 'shivamogga', 'khanna', 'ambikapur', 'bhandara', 'faizabad', 'kundli', 'nimbahera', 'arambagh', 'aurangabad-west-bengal', 'krishnanagar', 'dubrajpur', 'thalassery', 'dhampur', 'khopoli', 'pandharpur', 'sitapur', 'dharamsala', 'sundargarh', 'jamkhed', 'addanki', 'ponnur', 'atmakur', 'anjar', 'bobbili', 'jhabua', 'nawanshahr', 'pithapuram', 'tatipaka', 'pipariya', 'seoni-malwa', 'hamirpur', 'korba', 'anantapur', 'gurdaspur', 'tumkur', 'banga', 'morena', 'azamgarh', 'pratapgarh-uttar-pradesh', 'dibrugarh', 'palampur', 'nawapara', 'fazilka', 'jangaon', 'rajam', 'jirapur', 'pilkhuwa', 'jalalabad', 'dehgam', 'bhadravati', 'port-blair', 'aruppukkottai', 'sivagangai', 'devakottai', 'nandurbar', 'palani', 'mannarkkad', 'repalle', 'berhampur', 'jiaganj', 'khargone', 'trivandrum', 'kanchikacherla', 'hanuman-junction', 'kaikaluru', 'naidupeta', 'atmakur-nellore', 'madanapalle', 'punganur', 'kuppam', 'jaggampeta', 'yeleswaram', 'hajipur', 'burhanpur', 'jajpur-road', 'kalimpong', 'bapatla', 'mukhed', 'motihari', 'tuni', 'baghapurana', 'lonavala', 'tanda', 'hindaun', 'singarayakonda', 'venkatagiri', 'dongargarh', 'bakhrahat', 'sultanpur', 'madugula', 'rupnagar', 'morinda', 'junnar', 'gopalganj', 'kolar', 'malikipuram', 'cooch-behar', 'shirpur', 'rayagada', 'mahabubabad', 'angul', 'mundra', 'nandigama', 'neelapalle', 'petlad', 'uthukottai', 'amreli', 'kunnamkulam', 'cheepurupalli', 'chittoor', 'dharmavaram', 'ganapavaram', 'kandukur', 'markapuram', 'mogalthur', 'nagari', 'nindra', 'proddatur', 'saluru', 'yemmiganur', 'adoor', 'amballur', 'chalakudy', 'guruvayur', 'irinjalakuda', 'kattanam', 'kodakara', 'koothattukulam', 'peringottukara', 'thalikulam', 'thiruvalla', 'valanchery', 'wadakkancherry', 'acharapakkam', 'ambur', 'ammaiyarkuppam', 'annur', 'anthiyur', 'arakkonam', 'batlagundu', 'eriyur', 'kallakurichi', 'kangeyam', 'karaikudi', 'kulithalai', 'kumbakonam', 'muthur', 'namakkal', 'perundalaiyur', 'perundurai', 'pudukkottai', 'ramanathapuram', 'sankarankovil', 'sathankulam', 'sethiyathope', 'somanur', 'tenkasi', 'thiruthani', 'thiruvannamalai', 'thuraiyur', 'tiruchendur', 'tirukoilur', 'udumalpet', 'vedaranyam', 'vellakoil', 'vellore', 'bonakal', 'chevella', 'nirmal', 'krosuru', 'cherukupalli', 'railway-koduru', 'godhra', 'dholka', 'tohana', 'giridih', 'bodi', 'villupuram', 'islampur', 'singrauli', 'sangrur', 'kotdwar', 'dharmaj', 'kapadvanj', 'fatehabad', 'punjai-puliampatti', 'north-paravur', 'kuchaman', 'kavindapadi', 'alangayam', 'agartala', 'mullanpur', 'palakollu', 'kadiri', 'kovvur', 'kadapa', 'chagallu', 'duggirala', 'allagadda', 'kotabommali', 'gudur-kurnool', 'palamaner', 'nallamada', 'kothacheruvu', 'nidadavolu', 'bestavaripeta', 'chebrolu', 'nellimarla', 'nallajerla', 'hiramandalam', 'palvancha', 'himatnagar', 'domkal', 'sultan-bathery', 'penuganchiprolu', 'pamur', 'rayachoti', 'tanguturu', 'uppada', 'pathapatnam', 'pedana', 'somandepalle', 'pamidi', 'shahpur', 'dandeli', 'sidlaghatta', 'udupi', 'koratagere', 'sirsi', 'chikkaballapura', 'tiptur', 'pavagada', 'ankola', 'kambainallur', 'tiruchengode', 'thammampatti', 'rasipuram', 'jalakandapuram', 'valapadi', 'tirupattur', 'kaveripattinam', 'mettur', 'chinnasalem', 'sankagiri', 'pallipalayam', 'bommidi', 'jammikunta', 'parkal', 'thorrur', 'chityal', 'kamanpur', 'choutuppal', 'huzurabad', 'huzurnagar', 'kothagudem', 'sirpur-kagaznagar', 'valigonda', 'ieeja', 'ambernath', 'akividu', 'bilgi', 'kodumur', 'panruti', 'rabkavi', 'daryapur', 'dhone', 'jami', 'ponduru', 'ichchapuram', 'satyavedu', 'gokavaram', 'deoghar', 'sindagi', 'katni', 'vijayamangalam', 'gingee', 'gobichettipalayam', 'idappadi', 'ambasamudram', 'kadayam', 'bellampally', 'mukerian', 'dinanagar', 'jayamkondan', 'banswada', 'kota-nellore', 'peravurani', 'mudalgi', 'sankeshwar', 'umbergaon', 'pandikkad', 'neyveli', 'jamkhambhaliya', 'katihar', 'bijainagar', 'kovilpatti', 'harur', 'sakti', 'hapur', 'nadia', 'sambalpur', 'jharsuguda', 'gauribidanur', 'sujangarh', 'puliyankudi', 'kurinjipadi', 'hardoi', 'silchar', 'mattanur', 'kotpad', 'thanipadi', 'uthangarai', 'patiala', 'pedakurapadu', 'chinnamanur', 'titagarh', 'patran', 'sirsa', 'batala', 'khamgaon', 'lakhimpur-uttar-pradesh', 'srikalahasti', 'sardulgarh', 'nagapattinam', 'mala', 'bhagalpur', 'washim', 'berachampa', 'changaramkulam', 'sambhal', 'jeypore', 'dabra', 'ponnamaravathi', 'thiruthuraipoondi', 'nambiyur', 'jamtara', 'narwana', 'sugauli', 'mandi-gobindgarh', 'paralakhemundi', 'arumbavur', 'sullurpeta', 'sirkali', 'koratla', 'bagepalli', 'kuzhithurai', 'banaganapalli', 'bagnan', 'jaunpur', 'mayiladuthurai', 'palacode', 'forbesganj', 'kotputli', 'pusad', 'morbi', 'narnaul', 'jejuri', 'khurja', 'raxaul', 'alangudi', 'ekma-chapra', 'bundu', 'barhi', 'alakode', 'dharmapuri', 'tezpur', 'silvassa', 'surandai', 'cherpulassery', 'golaghat', 'bijapur', 'veraval', 'kalyani', 'kalakad', 'karur', 'chiplun', 'paramathivelur', 'saharsa', 'purnia', 'keeranur', 'samastipur', 'dumka', 'lakhimpur-assam', 'nabadwip', 'kokrajhar', 'ramabhadrapuram', 'dhanera', 'attur', 'bhadohi', 'chanpatia', 'malda', 'raiganj', 'sumerpur', 'borsad', 'daman', 'karwar', 'nelakondapally', 'mandvi', 'khandela', 'sathyamangalam', 'periyakulam', 'bazpur', 'damoh', 'krishnarajanagara', 'siruvalur', 'talwandi-bhai', 'pileru', 'falna', 'pulivendula', 'ron', 'chotila', 'gundlupet', 'chennur', 'una', 'luxettipet', 'hoogly', 'supaul', 'hazaribagh', 'Nathdwara', 'tittagudi', 'Valliyur', 'Viralimalai', 'Balanagar', 'Koottanad', 'Pirangut', 'Shirur', 'marthandam', 'cherupuzha', 'budaun', 'undavalli', 'mau', 'akbarpur', 'kankipadu', 'kakkattil', 'arni', 'srivilliputhur', 'kollengode', 'velanthavalam', 'sindhanur', 'kheda', 'mummidivaram', 'aranthangi', 'nazirpur', 'gohana', 'raichur', 'jabalpur', 'nava-raipur', 'jagraon', 'cheruvathur', 'bharatpur', 'palasa-kasibugga', 'malkipuram', 'p-dharmavaram', 'chimakurthy', 'maduranthakam', 'sunam', 'waterland', 'budhlada', 'kottakkal', 'wandoor', 'kolathur', 'farrukhabad', 'nichlaul', 'vrindavan', 'edacheri', 'kangra', 'mandi', 'chamba', 'sirmaur', 'kinnaur', 'razole', 'nakrekal', 'firozabad', 'kurumassery', 'kondotty', 'vita', 'tumakuru', 'tindivanam', 'neyveli-township', 'bilaspur-himachal-pradesh', 'virudhachalam', 'nanjangud', 'bibinagar', 'bhongir', 'thavanampalle', 'umreth', 'bangarupallem', 'anaikatti', 'balasinor', 'chintamani', 'pali', 'kanipakam', 'nagireddypet', 'jalore', 'yelamanchili', 'elamanchili', 'panachamoodu', 'west-champaran', 'gudur-nellore', 'sathupalli', 'thiruppathur', 'kolargoldfields', 'hoshangabad', 'andimadam', 'gopiganj', 'ariyalur', 'parawada', 'basantpur', 'chandausi', 'ottapalam', 'falakata', 'kanigiri', 'mappedu', 'srinagar', 'nagaram', 'amangal', 'velangi', 'gudiyatham', 'cheyyar', 'arcot', 'ranipet', 'vaniyambadi', 'sonari', 'kondur', 'perambra', 'puttur', 'jhunjhunu', 'lalgudi', 'manapparai', 'krishnarajpet', 'malur', 'ranastalam', 'kothampakkam', 'rajampet', 'vyara', 'ghumarwin', 'melli', 'una-gujarat', 'kotma', 'mahalingpur', 'gauriganj', 'melattur', 'vandavasi', 'burhar', 'chaygaon', 'sankarapuram', 'sholinghur', 'halduchour', 'lalkuan', 'pantnagar', 'thiruvallur', 'marpally', 'kolappalur', 'gondal', 'bhainsa', 'kankroli', 'koheda', 'gadwal', 'haveri', 'pernambut', 'mettupalayam', 'sukma', 'dantewada', 'koilkuntla', 'ayodhya', 'marandahalli', 'karanja-lad', 'paonta-sahib', 'eral', 'authoor', 'putturap', 'gajuwaka', 'newtehri', 'kunnamangalam', 'ramgarh', 'hindupuram', 'vettaikaranpudur', 'kolumam', 'thiruvalangadu', 'koderma', 'devgad', 'handwara', 'baramulla', 'atraulia', 'kayamkulam', 'sathuvachari', 'sahjanwa', 'greater-mumbai', 'karanodai', 'palladam', 'penumuru', 'rath', 'pallipattu', 'pulgaon', 'curchorem', 'choondal', 'kalady', 'bengaluru', 'chennai', 'coimbatore', 'delhi-ncr', 'hyderabad', 'kolkata', 'madurai', 'puducherry', 'tirupur', 'trivandrum', 'vijayawada', 'vizag']

# Base API URL
base_url = "https://apiproxy.paytm.com/v3/movies/search/movie?meta=1&reqData=1&city={}&movieCode=urjofqgl6u&version=3&site_id=6&channel=HTML5&child_site_id=370&client_id=ticketnew&clientId=ticketnew"

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Directory to save the JSON files
json_directory = f"cityJsons_{timestamp}"
os.makedirs(json_directory, exist_ok=True)

# Loop through each city, fetch the JSON data, and save it
for city in cities:
    api_url = base_url.format(city)
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        continue
    
    if response.status_code == 200:
        json_data = response.json()
        json_file_path = os.path.join(json_directory, f"{city}.json")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"Saved data for {city}")
    else:
        print(f"Failed to fetch data for {city}. Status code: {response.status_code}")

print("Data fetching complete.")

# Get all JSON file paths
json_file_paths = [os.path.join(json_directory, file) for file in os.listdir(json_directory) if file.endswith(".json")]

# Create final Excel workbook
final_workbook = openpyxl.Workbook()
final_sheet = final_workbook.active
final_sheet.title = "CombinedData"
final_headers = ["City", "Theater name", "AvailableTickets", "TotalTickets", "BookedTickets", "Occupancy (%)", "TotalGross", "BookedGross"]
final_sheet.append(final_headers)

# Apply header styling
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                    top=Side(style='thin'), bottom=Side(style='thin'))

for col_num, column_title in enumerate(final_headers, 1):
    cell = final_sheet.cell(row=1, column=col_num)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal="center", vertical="center")

# Set column widths
column_widths = [15, 25, 18, 15, 15, 15, 15, 15]
for i, width in enumerate(column_widths, 1):
    final_sheet.column_dimensions[get_column_letter(i)].width = width

# Initialize data structures
city_data = {}
city_output_files = []
city_excels_dir = f"cityExcels_{timestamp}/city_excel_data"
os.makedirs(city_excels_dir, exist_ok=True)

# Process each JSON file
for json_file_path in json_file_paths:
    with open(json_file_path, "r", encoding='utf-8') as file:
        data = json.load(file)

    city_name = os.path.splitext(os.path.basename(json_file_path))[0]
    workbook = openpyxl.Workbook()
    sheet1 = workbook.active
    sheet1.title = "DetailedData"
    sheet2 = workbook.create_sheet(title="AggregatedData_Per_Showtime")
    sheet3 = workbook.create_sheet(title="AggregatedData_Per_Theater")

    # Define headers
    sheet1_headers = ["Theater name", "Audi", "ShowTime", "Label", "AvailableTickets", "TotalTickets", "BookedTickets", "Occupancy (%)", "Price", "TotalGross", "BookedGross"]
    sheet2_headers = ["Theater name", "Audi", "Showtime", "AvailableTickets", "TotalTickets", "BookedTickets", "Occupancy (%)", "TotalGross", "BookedGross"]
    sheet3_headers = ["Theater name", "AvailableTickets", "TotalTickets", "BookedTickets", "Occupancy (%)", "TotalGross", "BookedGross"]

    # Append headers
    sheet1.append(sheet1_headers)
    sheet2.append(sheet2_headers)
    sheet3.append(sheet3_headers)

    # Apply header styling to all sheets
    for sheet in [sheet1, sheet2, sheet3]:
        headers = sheet1_headers if sheet == sheet1 else sheet2_headers if sheet == sheet2 else sheet3_headers
        for col_num, column_title in enumerate(headers, 1):
            cell = sheet.cell(row=1, column=col_num)
            cell.font = header_font
            cell.fill = header_fill
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center", vertical="center")

    # Set column widths for each sheet
    sheet1_widths = [25, 10, 15, 10, 18, 15, 15, 15, 10, 15, 15]
    sheet2_widths = [25, 10, 15, 18, 15, 15, 15, 15, 15]
    sheet3_widths = [25, 18, 15, 15, 15, 15, 15]

    for sheet, widths in [(sheet1, sheet1_widths), (sheet2, sheet2_widths), (sheet3, sheet3_widths)]:
        for i, width in enumerate(widths, 1):
            sheet.column_dimensions[get_column_letter(i)].width = width

    # Initialize data containers
    sheet2_data = {}
    sheet3_data = {}

    # Process cinema data
    for cinema in data.get("meta", {}).get("cinemas", []):
        theater_name = cinema.get("name", "Unknown Theater")
        cinema_id = str(cinema.get("id", "0"))
        sessions = data.get("pageData", {}).get("sessions", {}).get(cinema_id, [])

        for session in sessions:
            audi = session.get("audi", "Unknown Audi")
            show_time = format_showtime(session.get("showTime", "Unknown Time"))
            key = (theater_name, audi, format_showtime(session.get("showTime", "Unknown Time")))


            for area in session.get("areas", []):
                label = area.get("label", "N/A")
                sAvailTickets = area.get("sAvail", 0)
                sTotalTickets = area.get("sTotal", 0)
                price = area.get("price", 0.0)
                sBookedTickets = sTotalTickets - sAvailTickets

                sTotalGross = sTotalTickets * price
                sBookedGross = sBookedTickets * price

                # Calculate correct occupancy (as decimal)
                occupancy = (sBookedTickets / sTotalTickets) if sTotalTickets else 0

                # Write to Sheet1
                sheet1.append([
                    theater_name, audi, show_time, label, 
                    sAvailTickets, sTotalTickets, sBookedTickets, 
                    occupancy, price, round(sTotalGross, 2), round(sBookedGross, 2)
                ])

                # Accumulate data for Sheet2
                if key not in sheet2_data:
                    sheet2_data[key] = {
                        "AvailableTickets": 0,
                        "TotalTickets": 0,
                        "BookedTickets": 0,
                        "TotalGross": 0.0,
                        "BookedGross": 0.0
                    }
                sheet2_data[key]["AvailableTickets"] += sAvailTickets
                sheet2_data[key]["TotalTickets"] += sTotalTickets
                sheet2_data[key]["BookedTickets"] += sBookedTickets
                sheet2_data[key]["TotalGross"] += sTotalGross
                sheet2_data[key]["BookedGross"] += sBookedGross

                # Accumulate data for Sheet3
                if theater_name not in sheet3_data:
                    sheet3_data[theater_name] = {
                        "AvailableTickets": 0,
                        "TotalTickets": 0,
                        "BookedTickets": 0,
                        "TotalGross": 0.0,
                        "BookedGross": 0.0
                    }
                sheet3_data[theater_name]["AvailableTickets"] += sAvailTickets
                sheet3_data[theater_name]["TotalTickets"] += sTotalTickets
                sheet3_data[theater_name]["BookedTickets"] += sBookedTickets
                sheet3_data[theater_name]["TotalGross"] += sTotalGross
                sheet3_data[theater_name]["BookedGross"] += sBookedGross

    # Write Sheet2 data with formatted showtime
    for key, values in sheet2_data.items():
        theater_name, audi, show_time = key
        show_time = format_showtime(show_time)  # Ensure showtime is formatted here
        occupancy = (values["BookedTickets"] / values["TotalTickets"]) if values["TotalTickets"] else 0
        sheet2.append([
            theater_name, audi, show_time,
            values["AvailableTickets"], values["TotalTickets"], values["BookedTickets"],
            occupancy, round(values["TotalGross"], 2), round(values["BookedGross"], 2)
        ])


    # Write Sheet3 data
    for theater_name, values in sheet3_data.items():
        occupancy = (values["BookedTickets"] / values["TotalTickets"]) if values["TotalTickets"] else 0
        sheet3.append([
            theater_name, values["AvailableTickets"], values["TotalTickets"],
            values["BookedTickets"], occupancy,
            round(values["TotalGross"], 2), round(values["BookedGross"], 2)
        ])

        # Add to final sheet
        final_sheet.append([
            city_name, theater_name, values["AvailableTickets"], values["TotalTickets"],
            values["BookedTickets"], occupancy,
            round(values["TotalGross"], 2), round(values["BookedGross"], 2)
        ])

        # Accumulate city data
        if city_name not in city_data:
            city_data[city_name] = {
                "AvailableTickets": 0,
                "TotalTickets": 0,
                "BookedTickets": 0,
                "TotalGross": 0.0,
                "BookedGross": 0.0
            }
        city_data[city_name]["AvailableTickets"] += values["AvailableTickets"]
        city_data[city_name]["TotalTickets"] += values["TotalTickets"]
        city_data[city_name]["BookedTickets"] += values["BookedTickets"]
        city_data[city_name]["TotalGross"] += values["TotalGross"]
        city_data[city_name]["BookedGross"] += values["BookedGross"]

    # Add total rows and format sheets
    for sheet, columns in [(sheet1, [5, 6, 7, 9, 10, 11]), 
                          (sheet2, [4, 5, 6, 8, 9]),
                          (sheet3, [2, 3, 4, 6, 7])]:
        add_total_row(sheet, 2, sheet.max_row, columns)

    # Sort and format sheets
    for sheet in [sheet1, sheet2, sheet3]:
        # Apply borders and alternating row colors
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, max_col=sheet.max_column):
            for cell in row:
                cell.border = thin_border
                if cell.row % 2 == 0 and cell.row != sheet.max_row:  # Skip coloring the total row
                    cell.fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")

        # Format occupancy column as percentage
        occupancy_col = 8 if sheet == sheet1 else 7 if sheet == sheet2 else 5
        for row in sheet.iter_rows(min_row=2, min_col=occupancy_col, max_col=occupancy_col):
            for cell in row:
                cell.number_format = '0.00%'

        # Center align all cells
        for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, max_col=sheet.max_column):
            for cell in row:
                cell.alignment = Alignment(horizontal="center", vertical="center")

    # Save the city workbook
    city_output_file_path = os.path.join(city_excels_dir, f"{city_name}_{timestamp}.xlsx")
    workbook.save(city_output_file_path)
    city_output_files.append(city_output_file_path)

# Create consolidated city data sheet
consolidated_sheet = final_workbook.create_sheet(title="ConsolidatedCityData")
consolidated_headers = ["City", "AvailableTickets", "TotalTickets", "BookedTickets", "Occupancy (%)", "TotalGross", "BookedGross"]
consolidated_sheet.append(consolidated_headers)

# Style consolidated sheet headers
for col_num, column_title in enumerate(consolidated_headers, 1):
    cell = consolidated_sheet.cell(row=1, column=col_num)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Set column widths
    widths = [15, 18, 15, 15, 15, 15, 15]
    consolidated_sheet.column_dimensions[get_column_letter(col_num)].width = widths[col_num - 1]

# Write consolidated city data
for city_name, values in city_data.items():
    occupancy = (values["BookedTickets"] / values["TotalTickets"]) if values["TotalTickets"] else 0
    consolidated_sheet.append([
        city_name, values["AvailableTickets"], values["TotalTickets"],
        values["BookedTickets"], occupancy,
        round(values["TotalGross"], 2), round(values["BookedGross"], 2)
    ])

# Add total row and format consolidated sheet
add_total_row(consolidated_sheet, 2, consolidated_sheet.max_row, [2, 3, 4, 6, 7])

# Format consolidated sheet
for row in consolidated_sheet.iter_rows(min_row=2, max_row=consolidated_sheet.max_row, max_col=consolidated_sheet.max_column):
    for cell in row:
        cell.border = thin_border
        if cell.row % 2 == 0 and cell.row != consolidated_sheet.max_row:  # Skip coloring the total row
            cell.fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

# Format occupancy column as percentage
for row in consolidated_sheet.iter_rows(min_row=2, min_col=5, max_col=5):
    for cell in row:
        cell.number_format = '0.00%'

# Add total row and format final sheet
add_total_row(final_sheet, 2, final_sheet.max_row, [3, 4, 5, 7, 8])

# Format final sheet
for row in final_sheet.iter_rows(min_row=2, max_row=final_sheet.max_row, max_col=final_sheet.max_column):
    for cell in row:
        cell.border = thin_border
        if cell.row % 2 == 0 and cell.row != final_sheet.max_row:  # Skip coloring the total row
            cell.fill = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

# Format occupancy column as percentage in final sheet
for row in final_sheet.iter_rows(min_row=2, min_col=6, max_col=6):
    for cell in row:
        cell.number_format = '0.00%'

# Save final workbook
final_output_file_path = f"cityExcels_{timestamp}/combined_cities_{timestamp}.xlsx"
final_workbook.save(final_output_file_path)

# Create ZIP file
zip_file_path = f"cityExcels_{timestamp}/city_excel_data.zip"
with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    for root, dirs, files in os.walk(city_excels_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, city_excels_dir)
            zip_file.write(file_path, arcname)

print("Excel files created and zipped successfully with:")
print("- Corrected IST time format (xx:xx AM/PM)")
print("- Fixed occupancy percentage calculations")
print("- Added total rows to all sheets")
print("- Proper formatting and styling")

