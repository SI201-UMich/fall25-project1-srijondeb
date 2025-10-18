# Name: Srijon Deb
# Student ID: 80514602
# Email: srijon@umich.edu
# Collaborators: None, worked on this project individually
# GenAI Usage: Used ChatGPT for planning & debugging

import csv

def load_data(filename):

    data = []
    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip the first dummy column if present
            row.pop("", None)

            # Clean numeric fields
            for field in ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year"]:
                if row[field] == "NA" or row[field] == "":
                    row[field] = None
                else:
                    # year can stay as int, others as float
                    if field == "year":
                        row[field] = int(row[field])
                    else:
                        row[field] = float(row[field])
            
            data.append(row)
            
    return data
