import sys, csv

reader = csv.reader(sys.stdin)
for row in reader:
    if row[0] == "year":
        continue
    try:
        if len(row) < 8:
            continue
        year = row[0].strip()
        hs_code = row[4].strip()
        hs_desc = row[5].strip().replace("|", "-")
        trade_value = float(row[6].strip())
        if trade_value <= 0 or hs_code in ("TOTAL", ""):
            continue
        print(f"{year}|{hs_code}|{hs_desc}\t{trade_value}")
    except (ValueError, IndexError):
        continue
