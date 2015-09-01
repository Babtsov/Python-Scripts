# This program filters students based on user selected section number.
import os, re
COURSE_NAME = "EEE3308C"
TABLE_CATEGORIES = "Name,Breadboard,Power Supply,Parts"


def extractCVSInfo(namePattern):
    print("Looking for valid files in current directory...")
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
            lines = [re.split(r',|\n',row) for row in studentInfo]
    except EnvironmentError:
        print("Failed to open the CSV file: ",csvFiles[0])
        print("Please check the file and try again.")
        exit()
    print("The following valid file found:",csvFiles[0])
    return lines


def select_section(sections):
    selection = 0
    print("Section numbers found in file:")
    for index in range(len(sections)):
        print(index + 1,") ",sections[index],sep="")
    while True:
        try:
            selection = int(input("Please select a section: "))
            if selection < 1 or selection > len(sections):
                raise RuntimeError
            break
        except:
            print("Invalid input. Try again.")
    return sections[selection - 1]


def main():
    namePattern = r"\d+_\w+_\d+_\d+_Grades-" + COURSE_NAME + r"\.csv"
    lines = extractCVSInfo(namePattern)
    filtered_list = []
    course_sections = []
    for row in lines:
        for entry in row:
            if "Student" in entry: # erase test student
                lines.remove(row)
                break
            if COURSE_NAME + "-" in entry and entry not in course_sections:
                course_sections.append(entry)

    section = select_section(list(course_sections))
    for row in lines:
        for entry in row:
            if section in entry:
                filtered_list.append(row)
    output_name = str(section) + "_students.csv"
    with open(output_name,'w') as output_file:
        print(section,"\n,",file=output_file)
        print(TABLE_CATEGORIES,file=output_file)
        for row in filtered_list:
            row = list(row)
            print(row[0],row[1],sep=",",file=output_file)
        print("\n\nTOTAL:",len(filtered_list),file=output_file)
        print("Done. The following filtered file created:",output_name)


if __name__ == "__main__":
    main()
