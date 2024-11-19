
# Brief Description of what this module does.   
# Citations:
# Anything else that's relevant: 


# CSVProcessor.py

import csv
import requests
import re 
#import pandas as pd


class CSVProcessor:
    """
    Cleans data in FuelPurchaseData csv file and writes changes to new csv file, and anomilies to another 
    
    """
        
    def __init__(self, filename):
        self.__filename = filename
        self.cleaned_data = []
        self.anomalies = []
        self.api_key = "4a2979c0-a4a2-11ef-a907-953b7a3c587f"  
        self.api_base_url = "https://app.zipcodebase.com/api/v1/status"
   
    def process(self):
        #print("Processing", self.__filename)
        data = self.readData() #reads data from file
        if data:
            self.format_gross_price(data)
            self.remove_duplicates(data)
            self.handle_non_fuel_purchases(data)
            #self.update_addresses_with_zip(data)
            self.fetch_zip_code(data)
            #write updates to new csv files in Data folder
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
        for row in data:
            if 'Gross Price' in row:
                try:
                    row['Gross Price'] = f"{float(row['Gross Price']):.2f}"
                except ValueError:
                    print(f"Invalid Gross Price value: {row['Gross Price']} in row {row}")
            
    def remove_duplicates(self, data):
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
        if 'Fuel Type' in data[0]:  # Check if 'Fuel Type' column exists
            self.anomalies = [row for row in data if row.get('Fuel Type', '').strip().lower() == 'pepsi']
            data[:] = [row for row in data if row.get('Fuel Type', '').strip().lower() != 'pepsi']
        else: #column not found
            print("Warning: 'Fuel Type' column not found. Skipping anomaly processing.")

    def fetch_zip_code(self, data):
        for row in data:
            if not row.get('Zip Code'):
                city = row.get('City', '').strip()
                state = row.get('State', '').strip()
                if city and state:
                    try:
                        response = requests.get(
                            f"{self.api_base_url}/search",
                            params={"apikey": self.api_key, "city": city, "state": state},
                            timeout=10
                        )
                        response.raise_for_status()
                        zip_codes = response.json().get('results', {}).get(city, [])
                        if zip_codes:
                            row['Zip Code'] = zip_codes[0]
                    except requests.exceptions.RequestException as e:
                        print(f"Error fetching zip code for {city}, {state}: {e}")

#-----------------------------------
    def write_to_csv(self, data, output_file):
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
                