import sys, csv

reader = csv.reader(sys.stdin)
for row in reader:
    if row[0] == "year":
        continue
    try:
        if len(row) < 8:
            continue
        partner = row[3].strip()
        trade_value = float(row[6].strip())
        if trade_value <= 0 or partner in ("World", "Areas, nes", ""):
            continue
        print(f"{partner}\t{trade_value}")
    except (ValueError, IndexError):
        continue
