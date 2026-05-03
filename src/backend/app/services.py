def calculate_final(tugas, uts, uas):
    return round(0.3 * tugas + 0.3 * uts + 0.4 * uas, 2)


def get_grade(score):
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 55:
        return "C"
    elif score >= 40:
        return "D"
    return "E"