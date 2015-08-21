# This program extracts UF email addresses from a CSV file and prints them organized by class sections.
def extractEmailAddress(list):
    for item in list:
        if "@ufl.edu" in item:
            return item
    raise RuntimeError

with open("grades.csv", "r") as studentInfo:
    lines = [row.split(",") for row in studentInfo]
dict = {}
for row in lines:
    for entry in row:
        if "EEE3308C-" in entry:
            try:
                email = extractEmailAddress(row)
            except:
                print("Warning: failed to parse UF email for: ", row)
                continue
            if entry not in dict:
                dict[entry] = [email]
            else:
                dict[entry].append(email)
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
