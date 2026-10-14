import sys

current_key = None
prices = []

def emit(key, plist):
    parts = key.split("|", 2)
    if len(parts) == 3:
        code, desc, year = parts
        avg_p = sum(plist) / len(plist)
        min_p = min(plist)
        max_p = max(plist)
        print(f"{code}\t{desc}\t{year}\t{avg_p:.2f}\t{min_p:.2f}\t{max_p:.2f}\t{len(plist)}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        key, value = line.split("\t", 1)
        value = float(value)
    except ValueError:
        continue
    if current_key == key:
        prices.append(value)
    else:
        if current_key is not None:
            emit(current_key, prices)
        current_key = key
        prices = [value]

if current_key is not None:
    emit(current_key, prices)
