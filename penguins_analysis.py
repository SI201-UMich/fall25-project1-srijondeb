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


def average(values):
    if values:
        return sum(values) / len(values)
    else:
        None


def calc_avg_flipper_by_species_sex(data):
    # group flipper lengths by (species, sex)
    flipper_groups = {}

    for row in data:
        species = row.get("species")
        sex = row.get("sex")
        length = row.get("flipper_length_mm")

        # if any value is missing
        if not species or not sex or length is None:
            continue

        key = (species, sex)
        if key not in flipper_groups:
            flipper_groups[key] = []
        flipper_groups[key].append(length)

    # the average for each group
    averages = {}
    for key, lengths in flipper_groups.items():
        avg = sum(lengths) / len(lengths)
        averages[key] = avg

    return averages

