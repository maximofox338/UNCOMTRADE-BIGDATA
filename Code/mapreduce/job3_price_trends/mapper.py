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
        net_weight = float(row[7].strip())
        if trade_value <= 0 or net_weight <= 0:
            continue
        if hs_code in ("TOTAL", ""):
            continue
        unit_price = trade_value / net_weight
        if unit_price < 0.001 or unit_price > 1000000:
            continue
        print(f"{hs_code}|{hs_desc}|{year}\t{unit_price:.4f}")
    except (ValueError, IndexError, ZeroDivisionError):
        continue
