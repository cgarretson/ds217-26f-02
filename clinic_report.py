#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Read and return usable encounters plus skipped-row count."""
    encounters = []
    skipped = 0

    with open(data_path, "r", encoding="utf-8") as file:
        header = file.readline()

        for line in file:
            line = line.strip()

            if line == "":
                skipped = skipped + 1
                print("Skipping a blank row.")
                continue

            fields = line.split(",")

            if len(fields) != 3:
                skipped = skipped + 1
                print("Skipping a row with the wrong number of fields.")
                continue

            try:
                systolic = int(fields[2])
            except ValueError:
                skipped = skipped + 1
                print("Skipping a row with a non-integer systolic reading.")
                continue

            if systolic < 60 or systolic > 250:
                skipped = skipped + 1
                print("Skipping a row with an implausible systolic reading.")
                continue

            patient_id = fields[0]
            visit_date = fields[1]

            encounters.append([patient_id, visit_date, systolic])

    return encounters, skipped


def main():
    """Write vitals report and patient follow-up list."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings)} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)

    report_path = OUTPUT_DIR / "vitals_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        for line in report_lines:
            file.write(line + "\n")

    with open(report_path, "r", encoding="utf-8") as file:
        print(file.read())



    cutoff = 130

    followup_patients = patients_at_or_above(encounters, cutoff)

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        "Reason: Patients with at least one usable systolic reading at or above the cutoff are included for follow-up.",
    ]

    for patient_id in followup_patients:
        followup_lines.append(patient_id)

    followup_path = OUTPUT_DIR / "followup_list.txt"

    with open(followup_path, "w", encoding="utf-8") as file:
        for line in followup_lines:
            file.write(line + "\n")

    with open(followup_path, "r", encoding="utf-8") as file:
        print(file.read())

if __name__ == "__main__":
    main()