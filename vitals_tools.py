"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return the systolic value from every encounter."""
    readings = []

    for encounter in encounters:
        readings.append(encounter[2])

    return readings


def mean_systolic(readings):
    """Return the mean reading or None when there are no readings."""
    if not readings:
        return None

    return sum(readings) / len(readings)


def count_patients(encounters):
    """Counts patient IDs"""
    patient_ids = set()

    for encounter in encounters:
        patient_ids.add(encounter[0])

    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return patient IDs at or above the cutoff."""
    patient_ids = set()

    for encounter in encounters:
        if encounter[2] >= cutoff:
            patient_ids.add(encounter[0])

    return sorted(patient_ids)
