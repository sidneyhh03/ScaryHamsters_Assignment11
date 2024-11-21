
# Name: Sidney Huschart, Shelby Sash, Roman Stryjewski, Cheikh Abdoul
# email:  huschash@mail.uc.edu, sashsk@mail.uc.edu, sashsk@mail.uc.edu, abdoulch@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   November 21 2024
# Course #/Section:   IS4010-001
# Semester/Year:   Fall 2024
# Brief Description of the assignment: Collaborate using github to clean data in a csv file
# Brief Description of what this module does: The entry point for the project  
# Citations:
# Anything else that's relevant:


# main.py


from CSVpackage.CSVProcessor import CSVProcessor

def main():
    if __name__ == "__main__":
        print("main.py")
        myCSVProcessor = CSVProcessor("Data/fuelPurchaseData.csv")
        myCSVProcessor.process()
        print(myCSVProcessor.readData())
    
#entry point
if __name__ == "__main__":
    main()
