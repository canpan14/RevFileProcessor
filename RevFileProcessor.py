import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import csv
import sys
import os
from datetime import datetime

# This is all hard coded according to the example and should in the future use column classes instead
root = tk.Tk()
root.withdraw()

# Ask for file
filename = os.path.abspath(
    askopenfilename(initialdir="/", title="Select csv file", filetypes=(("CSV Files", "*.csv"),)))
# Set output file name
output_name = filename.rsplit('.')
del output_name[len(output_name) - 1]
if not output_name:
    sys.exit()
output_name = "".join(output_name)
output_name += "_processed.csv"
# Ask info to choose what years to process
yearsDesiredToProcess = simpledialog.askstring("Input",
                                               "How many years starting from the leftmost do you want to process? (If you go over how many you actually have it might blow up)",
                                               parent=root)
if not yearsDesiredToProcess or yearsDesiredToProcess == 0:
    sys.exit();
# Using the file that will be written to
csv_output_file = open(os.path.abspath(output_name), 'w', encoding='utf-8', newline='')
# Using the file is be read in
csv_file = open(filename, encoding='utf-8', errors='ignore')
# Define reader with , delimiter
csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
# Define writer to put quotes around input values with a comma in them
csv_writer = csv.writer(csv_output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


def format_date(date):
    try:
        return datetime.strftime(datetime.strptime(date, "%m/%d/%Y"), "%Y-%m-%d")
    except:
        return date

header_row = []
months = []
# Iterate over the rows in the csv
for idx, row in enumerate(csv_reader):
    if idx != 0:
        if not row[0]:
            continue
        # Iterate over the money values under each date
        amounts = []
        for count in range(0, int(yearsDesiredToProcess)):
            amounts += row[(30 + (count * 17)):(42 + (count * 17))]
        for index, amount in enumerate(amounts):
            row[0] = format_date(row[0])
            row[7] = format_date(row[7])
            row[8] = format_date(row[8])
            row[9] = format_date(row[9])
            # Write the values into the row
            csv_writer.writerow(row[0:30] + [format_date(months[index])] + [amount])
    else:
        header_row = row
        for count in range(0, int(yearsDesiredToProcess)):
            months += row[(30 + (count * 17)):(42 + (count * 17))]
        # Set headers for output file
        csv_writer.writerow(row[0:30] + ["Month", "Amount"])
csv_file.flush()
csv_output_file.flush()
csv_file.close()
csv_output_file.close()
