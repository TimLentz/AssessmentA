#!/usr/bin/env python3

'''
    This program selects a subset of patients from a data file based on
    their diagnosis. It gives the number of patients with diagnoses in
    different groups in the same month. For Cobbs Creek Healthcare Data
    Analysis Assessment Set A - Question #3
'''

import csv      # used to create reader objects from csv files
import sys      # used to accept command line arguments


def getGroup(claim_code):
    """
    This function converts a claim code into a group id
    :param claim_code: claim code of the patient
    :return: group that the patient fits in, or false if not in cohort
    """
    if claim_code in ["C83.0", "C83.00", "C83.01", "C83.02", "C83.03"]:
        return "A"
    elif claim_code in ["C91", "C91.1", "C91.10", "C91.11", "C91.12"]:
        return "B"
    elif claim_code in ["C95.10", "C95.90"]:
        return "C"
    else:
        return False


def main(argv):
    # accept optional command line argument for a data file or
    # use default file: sample_dx.csv
    if len(argv) == 2:
        dataFile = argv[1]
        print("Analyzing", dataFile, "...")
    else:
        dataFile = "sample_dx.csv"
        print("Analyzing default file: sample_dx.csv ...")

    # open the data file and store file object in data_csv
    data_csv = open(dataFile, "r")

    # create a reader object for the data file
    data = csv.reader(data_csv)

    cohort = {}             # create a dictionary for the cohort
    multiDiagnoses = set()  # create a set for patients with multiple diagnoses

    for r in data:
        # set group equal to the patient's diagnosis group and return false if no group
        if group := getGroup(r[2]):
            # check if patient id is alreacy in the cohort
            if r[0] in cohort:
                for d in cohort[r[0]]:
                    # if this patient has any different diagnoses in the same month
                    if r[3].partition("/")[0] in d and group not in d[r[3].partition("/")[0]]:
                        # add them to the multiple diagnoses set (sets ignore duplicates)
                        multiDiagnoses.add(r[0])
                        d[r[3].partition("/")[0]].append(group)
                        break
                # if there are no existing diagnoses in this monty, update the row
                if not any(r[3].partition("/")[0] in d for d in cohort[r[0]]):
                    cohort[r[0]].append({r[3].partition("/")[0]: [group]})
            # otherwise add the patient to the cohort
            else:
                cohort[r[0]] = [{r[3].partition("/")[0]: [group]}]
    # print cohort
    header = ["Cohort Patient IDs"]
    print(header[0])
    for r in cohort:
        print(r)

    # create CSV file for cohort
    with open("cohort.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for r in cohort.keys():
            csvwriter.writerows([[r]])

    print("\nThe number of patients with diagnoses in different groups "
          "in the same month is:", len(multiDiagnoses),"\n")

    print("cohort.csv created\n")

    # Prevent window from closing
    input("press ENTER to exit")


if __name__ == '__main__':
    main(sys.argv)
