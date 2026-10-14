import sys
from collections import defaultdict

country_years = defaultdict(dict)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        key, value = line.split("\t", 1)
        parts = key.split("|", 1)
        if len(parts) != 2:
            continue
        country, year = parts
        value = float(value)
        if year in country_years[country]:
            country_years[country][year] += value
        else:
            country_years[country][year] = value
    except (ValueError, IndexError):
        continue

for country, years_data in sorted(country_years.items()):
    sorted_years = sorted(years_data.keys())
    for i in range(1, len(sorted_years)):
        prev_year = sorted_years[i-1]
        curr_year = sorted_years[i]
        prev_val = years_data[prev_year]
        curr_val = years_data[curr_year]
        if prev_val > 0:
            growth = ((curr_val - prev_val) / prev_val) * 100
            print(f"{country}\t{prev_year}\t{curr_year}\t{prev_val:.2f}\t{curr_val:.2f}\t{growth:.2f}")
