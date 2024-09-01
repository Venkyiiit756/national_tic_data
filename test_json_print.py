import os

# Define the directory containing the JSON files
directory = "cityJsons"

# Get all JSON file paths from the directory
json_file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".json")]

# Print the list of JSON file paths
print(json_file_paths)
