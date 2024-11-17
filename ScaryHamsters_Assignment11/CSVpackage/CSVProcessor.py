
# Brief Description of what this module does.   
# Citations:
# Anything else that's relevant:


# CSVProcessor.py

import csv
import requests
import re 

class CSVProcessor:
        
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
            self.update_addresses_with_zip_codes(data)
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