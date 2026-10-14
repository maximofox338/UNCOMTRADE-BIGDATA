import sys

current_key = None
current_sum = 0.0
current_count = 0

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
        current_sum += value
        current_count += 1
    else:
        if current_key is not None:
            parts = current_key.split("|", 1)
            if len(parts) == 2:
                print(f"{parts[0]}\t{parts[1]}\t{current_sum:.2f}\t{current_count}")
        current_key = key
        current_sum = value
        current_count = 1

if current_key is not None:
    parts = current_key.split("|", 1)
    if len(parts) == 2:
        print(f"{parts[0]}\t{parts[1]}\t{current_sum:.2f}\t{current_count}")
