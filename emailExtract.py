# This program extracts UF email addresses from a CSV file and prints them organized by class sections.
import os
import re

COURSE_NAME = "EEE3308C"


def extractEmailAddress(list):
    for item in list:
        if "@ufl.edu" in item:
            return item
    raise RuntimeError


def extractCVSInfo(namePattern):
    csvFiles = [file for file in os.listdir('.') if re.match(namePattern,file)]
    if len(csvFiles) > 1:
        print("Multiple " + COURSE_NAME + " CSV files in the current directory: ", csvFiles)
        print("Please make sure there is only one " + COURSE_NAME + " CSV file and try again.")
        exit()
    elif len(csvFiles) == 0:
        print("No " + COURSE_NAME + " CSV file found in current directory. Please try again.")
        exit()
    try:
        with open(csvFiles[0], "r") as studentInfo:
            lines = [row.split(",") for row in studentInfo]
    except EnvironmentError:
        print("Failed to open the CSV file: ",csvFiles[0])
        print("Please check the file and try again.")
        exit()
    return lines


namePattern = r"\d+_\w+_\d+_\d+_Grades-" + COURSE_NAME + r"\.csv"
lines = extractCVSInfo(namePattern)
dict = {}
for row in lines:
    for entry in row:
        if " Test\"" in entry: # search and remove test student
            lines.remove(row)
            break
        if COURSE_NAME + "-" in entry:
            try:
                email = extractEmailAddress(row)
            except:
                print("Warning: failed to parse UF email for: ", row)
                continue
            if entry not in dict:
                dict[entry] = [email]
            else:
                dict[entry].append(email)
print(COURSE_NAME + " Student Email Summary:",end="\n\n")
print("All Emails", end=" ")
print("(%d students)" % sum([len(value) for value in dict.values()]))
for emails in dict.values():
    for email in emails:
        print(email,end="; ")
print("\n\n")
for section,emails in dict.items():
    print("Section %s (%d students):" %(section,len(emails)))
    for email in emails:
        print(email,end='; ')
    print("\n\n")
