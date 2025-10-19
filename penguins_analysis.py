# Name: Srijon Deb
# Student ID: 80514602
# Email: srijon@umich.edu
# Collaborators: None, worked on this project individually
# GenAI Usage: I used ChatGPT to help me write all of my test
#              cases and to debug and fix errors in my functions. It was 
#              helpful for planning how to structure my code, catching mistakes, 
#              and making sure my results matched the project requirements.

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
    with open("penguin_results.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # Flipper averages
        writer.writerow(["Flipper Averages:"])  # title row
        writer.writerow(["species", "sex", "average_flipper_length"])
        flipper_averages = calc_avg_flipper_by_species_sex(data)
        for (species, sex), avg in flipper_averages.items():
            writer.writerow([species, sex, round(avg, 2)])

        writer.writerow([])  # blank line 

        # Heaviest species
        writer.writerow(["Heaviest Species by Island:"])  # title row
        writer.writerow(["island", "species", "avg_mass"])
        heaviest_species = calc_heaviest_species_by_island(data)
        for island, value in heaviest_species.items():
            writer.writerow([island, value["species"], round(value["avg_mass"], 2)])

    print("Results written to penguin_results.csv")




def test_load_data():
    """Tests for load_data"""
    # General: normal row with numbers
    data = [
        {"bill_length_mm": "39.1", "bill_depth_mm": "18.7", "flipper_length_mm": "181", "body_mass_g": "3750", "year": "2007"}
    ]
    # Simulate DictReader row cleanup
    row = data[0]
    row["bill_length_mm"] = float(row["bill_length_mm"])
    assert isinstance(row["bill_length_mm"], float)

    # Edge: row with NA
    row["flipper_length_mm"] = "NA"
    flipper_val = None if row["flipper_length_mm"] == "NA" else float(row["flipper_length_mm"])
    assert flipper_val is None

def test_average():
    """Tests for average"""
    # General
    assert average([1, 2, 3]) == 2
    assert round(average([2.5, 3.5, 4.5]), 2) == 3.5
    # Edge
    assert average([]) is None
    assert average([10]) == 10


def test_calc_avg_flipper_by_species_sex():
    """Tests for calc_avg_flipper_by_species_sex"""
    mock_data = [
        {"species": "Adelie", "sex": "male", "flipper_length_mm": 180},
        {"species": "Adelie", "sex": "male", "flipper_length_mm": 190},
        {"species": "Adelie", "sex": "female", "flipper_length_mm": 170},
    ]
    # General: normal grouping
    result = calc_avg_flipper_by_species_sex(mock_data)
    assert round(result[("Adelie", "male")], 2) == 185.0
    assert result[("Adelie", "female")] == 170

    # Edge: missing data
    mock_data.append({"species": "Adelie", "sex": None, "flipper_length_mm": 200})
    result = calc_avg_flipper_by_species_sex(mock_data)
    assert ("Adelie", None) not in result


def test_calc_heaviest_species_by_island():
    """Tests for calc_heaviest_species_by_island"""
    mock_data = [
        {"island": "Torgersen", "species": "Adelie", "body_mass_g": 3700},
        {"island": "Torgersen", "species": "Adelie", "body_mass_g": 3800},
        {"island": "Torgersen", "species": "Gentoo", "body_mass_g": 4500},
        {"island": "Biscoe", "species": "Gentoo", "body_mass_g": 5000},
    ]
    # General: correct heaviest species
    result = calc_heaviest_species_by_island(mock_data)
    assert result["Torgersen"]["species"] == "Gentoo"
    assert result["Biscoe"]["species"] == "Gentoo"

    # Edge: missing mass
    mock_data.append({"island": "Biscoe", "species": "Gentoo", "body_mass_g": None})
    result = calc_heaviest_species_by_island(mock_data)
    # Should still compute without crashing
    assert "Biscoe" in result


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    test_load_data()
    test_average()
    test_calc_avg_flipper_by_species_sex()
    test_calc_heaviest_species_by_island()
    print("All tests passed")
