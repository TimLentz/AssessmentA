#!/usr/bin/env python3

''' This program analyzes data from two files, which can be specified
    from the command line or default to sales.csv and sd_mapping.csv.
    It creates a report with quarterly sales for each specialty
    distribution. For Cobbs Creek Healthcare Data Analysis Assessment
    Set A - Question #2'''

#used to create reader objects from csv files
import csv
#used to print a formatted table
from tabulate import tabulate
#used to accept command line arguments
import sys

def main(argv):
    #accept optional command line arguments
    if len(argv) == 3:
        file1 = argv[1]
        file2 = argv[2]
    else:
        file1 = "sales.csv"
        file2 = "sd_mapping.csv"

    #display a message while the program is running
    print("Analyzing", file1, "and", file2, "...")

    #open both files and store file objects in variables
    sales_csv = open(file1, "r")
    sd_csv = open(file2, "r")

    #create reader objects for both input files, each row is a dict
    #the first row of each file is used as fieldnames
    sales = csv.DictReader(sales_csv)
    sd = csv.DictReader(sd_csv)

    #A list of dictionaries to store sales data
    salesList = []

    #Add the apropriate quarter to each dictionary (row) and append it to the
    #salesList list.  Throw out any data that is not from 2021
    for row in sales:
        if row["DATE"][-4:] == "2021":
            if row["DATE"][:2] >= "10":
                row["QUARTER"] = 4
                salesList.append(row)
            elif row["DATE"][:2] >= "07":
                row["QUARTER"] = 3
                salesList.append(row)
            elif row["DATE"][:2] >= "04":
                row["QUARTER"] = 2
                salesList.append(row)
            else:
                row["QUARTER"] = 1
                salesList.append(row)

    #A dictionary for storing and printing the resulting tally of perscriptions from sales
    output = {"AMERISOURCE": ["AMERISOURCE", 0, 0, 0, 0],
              "CARDINAL": ["CARDINAL", 0, 0, 0, 0],
              "MCKESSON": ["MCKESSON", 0, 0, 0, 0],
              "-": ["NO_CONTRACT_SD", 0, 0, 0, 0]}

    #Count the total perscriptions (TOTAL_TRX) for each SD by 2021 quarter
    #For item in sd_mapping, add the perscritions from each associated account by PARENT_ID
    #to the total count in output
    for sdRow in sd:
        for salesRow in salesList:
            if salesRow["PARENT_ACCOUNT_ID"] == sdRow["PARENT_ID"]:
                output[sdRow["SD_NAME"]][salesRow['QUARTER']] += int(salesRow['TOTAL_TRX'])

    #Print a table with 2021 quarterly perforamnce trends for all available SDs
    header = ["Specialty Distribution", "2021Q1", "2021Q2", "2021Q3", "2021Q4"]
    print('\n', tabulate(output.values(), headers=header), '\n\n')

    # Create as csv file with the quarterly performance trends for all SDs
    with open("quarterlyPerformance.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(output.values())

    print("\ncohort.csv created\n")

    #Prevent window from closing
    input("press ENTER to exit")

if __name__ == "__main__":
    main(sys.argv)

__author__ = "Timothy Lentz"
