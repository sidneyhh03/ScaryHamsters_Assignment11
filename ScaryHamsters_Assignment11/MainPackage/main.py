
# Name: Sidney Huschart, Shelby Sash, Roman Stryjewski, Cheikh Abdoul
# email:  {required}
# Assignment Number: Assignment 11
# Due Date:   November 21 2024
# Course #/Section:   IS4010-001
# Semester/Year:   Fall 2024
# Brief Description of the assignment:  {required}

# Brief Description of what this module does.   
# Citations:
# Anything else that's relevant:


# main.py


from CSVPackage.CSVProcessor import *

if __name__ == "__main__":
    print("main.py")
    myCSVProcessor = CSVProcessor("Data/fuelPurchaseData.csv")
    myCSVProcessor.process()
    print(myCSVProcessor.readData())
