import os


cities = [
    "Kolkata", "Manipal", "Patna", "Palluruthy", "Tumkur", "Ranchi", "Mohali", "Vasai", 
    "Jamnagar", "Faridabad", "Cuttack", "Kanpur", "Lucknow", "Mumbai", "Thane", "Ulhasnagar", 
    "Ahmedabad", "Greater Noida", "Kochi", "Chandigarh", "Surat", "Pune", "Chennai", "Durg", 
    "Bhubaneswar", "Vellore", "Gwalior", "Vadodara", "Ambernath", "Howrah", "Trivandrum", 
    "Noida", "Chandrapur", "Andul", "Bhilai", "Mysuru", "Gandhinagar", "Dehradun", "Indore", 
    "Delhi-NCR", "Bhopal", "Nashik", "Navi Mumbai", "Goa", "Jaipur", "Kota", "Greater Mumbai", 
    "New Delhi", "Jalandhar", "Gurgaon", "Raipur", "Aurangabad", "Guwahati", "Hosur", 
    "Dhanbad", "Coimbatore", "Rourkela"
]

# Create the 'cities' directory if it doesn't exist
os.makedirs("cities", exist_ok=True)

# Create directories for each city
for city in cities:
    os.makedirs(os.path.join("cities", city), exist_ok=True)

print("Directories created successfully.")