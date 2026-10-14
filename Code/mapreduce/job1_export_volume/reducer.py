import sys

current_country = None
current_sum = 0.0
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        country, value = line.split("\t", 1)
        value = float(value)
    except ValueError:
        continue
    if current_country == country:
        current_sum += value
        current_count += 1
    else:
        if current_country is not None:
            print(f"{current_country}\t{current_sum:.2f}\t{current_count}")
        current_country = country
        current_sum = value
        current_count = 1

if current_country is not None:
    print(f"{current_country}\t{current_sum:.2f}\t{current_count}")
