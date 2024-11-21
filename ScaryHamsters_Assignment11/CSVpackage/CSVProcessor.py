# Name: Sidney Huschart, Shelby Sash, Roman Stryjewski, Cheikh Abdoul
# email:  huschash@mail.uc.edu, sashsk@mail.uc.edu, sashsk@mail.uc.edu, abdoulch@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   November 21 2024
# Course #/Section:   IS4010-001
# Semester/Year:   Fall 2024
# Brief Description of the assignment: Collaborate using github to clean data in a csv file
# Brief Description of what this module does: Wrote the code to clean up the  data in FuelPurchaseData csv file. Crested two new files with new sets of data.
# Citations:
# Anything else that's relevant:


# CSVProcessor.py

import csv
import requests
import re 
import time

class CSVProcessor:
    """
     
    """
        
    def __init__(self, filename):
        """
        Initializes instance of CSVProcessor class 
        @param self: the instance of the class
        @param filename: string specifying the path to the csv file being processed
        """
        self.__filename = filename
        self.cleaned_data = []
        self.anomalies = []
        self.api_key = "8510a400-a7cf-11ef-9e53-29f24329e12a"  
        self.api_base_url = "https://app.zipcodebase.com/api/v1/code/city"

   
    def process(self):
        #print("Processing", self.__filename)
        data = self.readData() #reads data from file
        if data:
            self.format_gross_price(data)
            self.remove_duplicates(data)
            self.handle_non_fuel_purchases(data)
            #self.update_addresses_with_zip_codes(data)
            self.write_to_csv(data, "Data/cleanedData.csv")
            self.write_to_csv(self.anomalies, "Data/dataAnomalies.csv")

    def readData(self):
        try:
            with open(self.__filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
            return data
        except FileNotFoundError:
            print(f"File {self.__filename} not found.")
            return None
        
    def format_gross_price(self, data):
        """
        Formats the "Gross Price" column to two decimal places
        @param self: the instance of the class
        @param data: A list of dictionaries that represents the rows
        @return: None. Method modifies the csv file
        """
        for row in data:
            if 'Gross Price' in row:
                try:
                    row['Gross Price'] = f"{float(row['Gross Price']):.2f}"
                except ValueError:
                    print(f"Invalid Gross Price value: {row['Gross Price']} in row {row}")
            
    def remove_duplicates(self, data):
        """
        Removes duplicated rows from the data in the csv file
        @param self: the instance of the class
        @param data: A list of dictionaries that represents the rows
        @return: None. Method updates the `data` list in place with only unique rows
        """
        unique_data = []
        seen = set()
        for row in data:
            row_tuple = tuple(row.items())
            if row_tuple not in seen:
                seen.add(row_tuple)
                unique_data.append(row)
        data.clear()
        data.extend(unique_data) 
        
    def handle_non_fuel_purchases(self, data):
        """
        Identifies non-fuel values in "Fuel Type" row and removes from original dataset
        @param self: the instance of the class
        @param data: A list of dictionaries that represents the rows
        @return: None. Method updates the `data` list by removing "non-fuel" purchases
        """
        if 'Fuel Type' in data[0]:  # Check if 'Fuel Type' column exists
            self.anomalies = [row for row in data if row.get('Fuel Type', '').strip().lower() == 'pepsi']
            data[:] = [row for row in data if row.get('Fuel Type', '').strip().lower() != 'pepsi']
        else: #column not found
            print("Warning: 'Fuel Type' column not found. Skipping anomaly processing.")

    def write_to_csv(self, data, output_file):
        """
        Writes data to a csv file
        @param self: the instance of the class
        @param data: A list of dictionaries that represents the rows
        @param output_file: A string specifying gthe path to the output file
        @return: None. Method writes data to specified csv file
        """
        # Write data to CSV, including headers dynamically  
        if data:
            keys = data[0].keys()
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
        else:
            # If there's no data, create an empty file with headers
            with open(output_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([])  # Empty header
#-----------------
"""
    def update_addresses_with_zip_codes(self, data):
        for row in data:
            if 'Full Address' in row:
                full_address = row['Full Address']
                if not re.search(r'\b\d{5}\b', full_address):  # Check for a 5-digit zip code
                    city_state = self.extract_city_state(full_address)
                    if city_state:
                        zip_code = self.fetch_zip_code(city_state)
                        if zip_code:
                            row['Full Address'] += f", {zip_code}"

    def extract_city_state(self, full_address):
        # Simplistic approach: assuming addresses are formatted as "Street, City, State"
        try:
            parts = full_address.split(",")
            if len(parts) >= 2:
                city = parts[-2].strip()
                state = parts[-1].strip()
                return f"{city},{state}"
            return None
        except Exception as e:
            print(f"Error extracting city and state from address '{full_address}': {e}")
            return None

    def fetch_zip_code(self, city_state):
        try:
            # Adding the country parameter (United States)
            response = requests.get(
                self.api_base_url,
                params={
                    "apikey": self.api_key,
                    "city": city_state.split(',')[0].strip(),  # City
                    "state": city_state.split(',')[1].strip(),  # State
                    "country": "US"  # Hardcoded as United States
                }
            )
            if response.status_code == 200:
                data = response.json()
                # Assuming the response returns results like this:
                # data['results']['city,state'][0]
                zip_codes = data.get('results', {}).get(city_state, [])
                if zip_codes:
                    return zip_codes[0]  # Return the first zip code found
                else:
                    print(f"No zip code found for {city_state}.")
            else:
                print(f"Error fetching zip code for {city_state}: {response.text}")
        except Exception as e:
            print(f"Exception occurred during API call for {city_state}: {e}")
        return None
"""
#------------------------------




    
        

    