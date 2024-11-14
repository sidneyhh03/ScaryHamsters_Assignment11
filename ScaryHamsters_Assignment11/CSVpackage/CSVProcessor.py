
# Brief Description of what this module does.   
# Citations:
# Anything else that's relevant:


# CSVProcessor.py


import csv

class CSVProcessor:
    
    def __init__(self, filename):
        self.__filename = filename
        
    def process(self):
        print("Processing", self.__filename)
        data = self.readData()

    def readData(self):
        return None
        
