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
    
    return None


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


def calc_heaviest_species_by_island(data):
    # grouping body masses by (island, species)
    body_mass_groups = {}

    for row in data:
        island = row.get("island")
        species = row.get("species")
        mass = row.get("body_mass_g")

        if not island or not species or mass is None:
            continue  # skip rows with missing data

        key = (island, species)
        if key not in body_mass_groups:
            body_mass_groups[key] = []
        body_mass_groups[key].append(mass)

    # average mass for each (island, species)
    avg_masses = {}
    for key, masses in body_mass_groups.items():
        avg = sum(masses) / len(masses)
        avg_masses[key] = avg

    # heaviest species per island
    heaviest_by_island = {}
    for (island, species), avg_mass in avg_masses.items():
        if island not in heaviest_by_island:
            heaviest_by_island[island] = {"species": species, "avg_mass": avg_mass}
        else:
            current_max = heaviest_by_island[island]["avg_mass"]
            if avg_mass > current_max:
                heaviest_by_island[island] = {"species": species, "avg_mass": avg_mass}

    return heaviest_by_island


def write_results(results, filename, result_type):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)

        if result_type == "flipper":
            writer.writerow(["species", "sex", "average_flipper_length"])
            for (species, sex), avg in results.items():
                writer.writerow([species, sex, round(avg, 2)])

        elif result_type == "heaviest":
            writer.writerow(["island", "species", "avg_mass"])
            for island, value in results.items():
                writer.writerow([island, value["species"], round(value["avg_mass"], 2)])



def main():
    data = load_data("penguins.csv")

    # First calculation: Average flipper length by species and sex
    flipper_averages = calc_avg_flipper_by_species_sex(data)
    write_results(flipper_averages, "flipper_averages.csv", "flipper")

    # Second calculation: Heaviest species by island
    heaviest_species = calc_heaviest_species_by_island(data)
    write_results(heaviest_species, "heaviest_species.csv", "heaviest")

    print("Both results written successfully.")
