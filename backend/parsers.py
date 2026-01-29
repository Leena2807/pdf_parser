import re

def normalize_sgpa(value):
    if not value:
        return None
    value = value.strip()
    if value in ["-", "-----", "NA"]:
        return None
    try:
        return float(value)
    except:
        return None

# =========================
# LEDGER PARSER (Single Student)
# =========================
def parse_ledger(text, filename):
    students = []

    seat_match = re.search(
        r"SEAT\s*NO\.?\s*:\s*([A-Z]\d+)",
        text,
        re.IGNORECASE
    )

    name_match = re.search(
        r"NAME\s*:\s*([A-Z ]+?)(?:\s+MOTHER|\s+MOTHER'S|\s+MOTHER’S|$)",
        text,
        re.IGNORECASE
    )

    sem1_match = re.search(
        r"(FIRST|THIRD)\s+SEMESTER\s+SGPA\s*:\s*([-\d.]+)",
        text,
        re.IGNORECASE
    )

    sem2_match = re.search(
        r"(SECOND|FOURTH)\s+SEMESTER\s+SGPA\s*:\s*([-\d.]+)",
        text,
        re.IGNORECASE
    )

    if not seat_match:
        return students

    sgpa1 = normalize_sgpa(sem1_match.group(2)) if sem1_match else None
    sgpa2 = normalize_sgpa(sem2_match.group(2)) if sem2_match else None

    result = "PASS" if sgpa1 is not None else "FAIL"

    students.append({
        "seat_number": seat_match.group(1),
        "name": name_match.group(1).strip() if name_match else "UNKNOWN",
        "sgpa_sem1": sgpa1,
        "sgpa_sem2": sgpa2,
        "result": result,
        "source_file": filename
    })

    return students
def parse_fe_single(text, filename):
    students = []

    seat = re.search(r"SEAT\s*NO\s*:\s*([A-Z]\d+)", text, re.IGNORECASE)
    name = re.search(r"STUDENT\s+NAME\s*:\s*([A-Z ]+)", text, re.IGNORECASE)
    sgpa = re.search(r"FIRST\s+SEMESTER\s+SGPA\s*:\s*([-\d.]+)", text, re.IGNORECASE)

    if not seat or not sgpa:
        return students

    sgpa1 = normalize_sgpa(sgpa.group(1))

    students.append({
        "seat_number": seat.group(1),
        "name": name.group(1).strip() if name else "UNKNOWN",
        "sgpa_sem1": sgpa1,
        "sgpa_sem2": None,
        "result": "PASS" if sgpa1 is not None else "FAIL",
        "source_file": filename
    })

    return students
# =========================
# TABLE PARSER (Batch Results)
# =========================
def parse_table(text, filename):
    students = []

    table_pattern = re.compile(
        r"(S\d{9})\s+[A-Z ]+\s+([-\d.]+)\s+([-\d.]+)",
        re.MULTILINE
    )

    for seat, sg1, sg2 in table_pattern.findall(text):
        sgpa1 = normalize_sgpa(sg1)
        sgpa2 = normalize_sgpa(sg2)

        result = "PASS" if sgpa1 is not None and sgpa2 is not None else "FAIL"

        students.append({
            "seat_number": seat,
            "name": "UNKNOWN",
            "sgpa_sem1": sgpa1,
            "sgpa_sem2": sgpa2,
            "result": result,
            "source_file": filename
        })

    return students
def clean_name(name):
    tokens = name.split()
    clean = []
    for t in tokens:
        if re.match(r"^[-\d.]+$", t):
            break
        clean.append(t)
    return " ".join(clean)
def parse_table_wrapped(text, filename):
    students = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    current = None

    for line in lines:
        if re.match(r"S\d{9}", line):
            if current:
                current["name"] = clean_name(current["name"])
                students.append(current)

            parts = line.split()

            seat = parts[0]
            rest = parts[1:]

            # check if last two tokens are SGPA values
            if len(rest) >= 3 and re.match(r"[-\d.]+", rest[-1]) and re.match(r"[-\d.]+", rest[-2]):
                sgpa1 = normalize_sgpa(rest[-2])
                sgpa2 = normalize_sgpa(rest[-1])
                name = " ".join(rest[:-2])
            else:
                sgpa1 = None
                sgpa2 = None
                name = " ".join(rest)

            current = {
             "seat_number": seat,
             "name": name.strip(),
             "sgpa_sem1": sgpa1,
             "sgpa_sem2": sgpa2,
             "result": "PASS" if sgpa1 is not None else "FAIL",
             "source_file": filename
            }
        elif current and re.search(r"\d+\.\d+", line):
            values = re.findall(r"\d+\.\d+", line)

            if len(values) == 1:
                if current["sgpa_sem1"] is None:
                    current["sgpa_sem1"] = normalize_sgpa(values[0])
                elif current["sgpa_sem2"] is None:
                    current["sgpa_sem2"] = normalize_sgpa(values[0])
            
            elif len(values) >= 2:
                current["sgpa_sem1"] = normalize_sgpa(values[0])
                current["sgpa_sem2"] = normalize_sgpa(values[1])


            if current["sgpa_sem1"] is not None:
                current["result"] = "PASS"

        elif current:
            current["name"] += " " + line

    if current:
        current["name"] = clean_name(current["name"])
        students.append(current)

    return students
