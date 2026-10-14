import csv
import sys
import os
from collections import Counter

INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "china_exports.csv"
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else "china_exports_clean.csv"

SKIP_PARTNERS = {
    "World", "Areas, nes", "Other Asia, nes", "Other Europe, nes",
    "Other Africa, nes", "Other Americas, nes",
    "Bunkers", "Free Zones", "Special Categories",
    "Neutral Zone", "TOTAL", ""
}

SKIP_HS_CODES = {"TOTAL", "AG1", "AG2", "AG3", "AG4", "AG5", "AG6", "ALL", ""}

EXPECTED_HEADER = [
    "year", "trade_flow", "reporter", "partner",
    "hs_code", "hs_description",
    "trade_value_usd", "net_weight_kg", "quantity", "quantity_unit"
]

stats = {
    "total_raw": 0, "duplicate_headers": 0, "empty_trade_value": 0,
    "zero_trade_value": 0, "negative_trade_value": 0, "empty_partner": 0,
    "aggregate_partner": 0, "aggregate_hs_code": 0, "empty_hs_code": 0,
    "invalid_numeric": 0, "exact_duplicates": 0, "rows_cleaned": 0, "rows_written": 0,
}

COUNTRY_FIXES = {
    "Viet Nam": "Vietnam", "Türkiye": "Turkey", "Turkiye": "Turkey",
    "Iran (Islamic Republic of)": "Iran", "Korea, Republic of": "South Korea",
    "Korea, Rep.": "South Korea", "China, Hong Kong SAR": "Hong Kong",
    "China, Macao SAR": "Macao", "Russian Federation": "Russia",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "United States of America": "United States",
    "Lao People's Democratic Republic": "Laos",
    "Syrian Arab Republic": "Syria",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Tanzania, United Republic of": "Tanzania",
    "Congo, Democratic Republic of the": "DR Congo",
    "Côte d'Ivoire": "Ivory Coast", "Czechia": "Czech Republic",
    "State of Palestine": "Palestine", "Brunei Darussalam": "Brunei",
}

def normalize_country(name):
    name = name.strip()
    return COUNTRY_FIXES.get(name, name)

def is_valid_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def clean_row(row):
    if len(row) < 8:
        stats["invalid_numeric"] += 1
        return None

    year = row[0].strip()
    trade_flow = row[1].strip()
    reporter = row[2].strip()
    partner = row[3].strip()
    hs_code = row[4].strip()
    hs_desc = row[5].strip()
    trade_value_raw = row[6].strip()
    net_weight_raw = row[7].strip() if len(row) > 7 else "0"
    quantity_raw = row[8].strip() if len(row) > 8 else "0"
    quantity_unit = row[9].strip() if len(row) > 9 else ""

    if year == "year":
        stats["duplicate_headers"] += 1
        return None
    if partner == "" or partner is None:
        stats["empty_partner"] += 1
        return None
    if partner in SKIP_PARTNERS:
        stats["aggregate_partner"] += 1
        return None
    if hs_code.upper() in SKIP_HS_CODES:
        stats["aggregate_hs_code"] += 1
        return None
    if hs_code == "":
        stats["empty_hs_code"] += 1
        return None
    if trade_value_raw == "" or trade_value_raw is None:
        stats["empty_trade_value"] += 1
        return None
    if not is_valid_number(trade_value_raw):
        stats["invalid_numeric"] += 1
        return None

    trade_value = float(trade_value_raw)
    if trade_value < 0:
        stats["negative_trade_value"] += 1
        return None
    if trade_value == 0:
        stats["zero_trade_value"] += 1
        return None

    net_weight = float(net_weight_raw) if is_valid_number(net_weight_raw) else 0.0
    quantity = float(quantity_raw) if is_valid_number(quantity_raw) else 0.0
    if net_weight < 0: net_weight = 0.0
    if quantity < 0: quantity = 0.0

    partner = normalize_country(partner)
    hs_desc = " ".join(hs_desc.split())
    stats["rows_cleaned"] += 1

    return [year, trade_flow, reporter, partner, hs_code, hs_desc,
            f"{trade_value:.2f}", f"{net_weight:.2f}", f"{quantity:.2f}", quantity_unit]

def main():
    print("=" * 60)
    print("  Data Cleaning — Export Trade Data Analyzer")
    print("=" * 60)
    print(f"\n  Input:  {INPUT_FILE}")
    print(f"  Output: {OUTPUT_FILE}\n")

    if not os.path.exists(INPUT_FILE):
        print(f"  ERROR: File not found: {INPUT_FILE}")
        sys.exit(1)

    seen_rows = set()

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        writer.writerow(EXPECTED_HEADER)

        for row in reader:
            stats["total_raw"] += 1
            cleaned = clean_row(row)
            if cleaned is None:
                continue
            row_key = tuple(cleaned[:7])
            if row_key in seen_rows:
                stats["exact_duplicates"] += 1
                continue
            seen_rows.add(row_key)
            writer.writerow(cleaned)
            stats["rows_written"] += 1
            if stats["rows_written"] % 100000 == 0:
                print(f"  Processed {stats['total_raw']:,} rows, kept {stats['rows_written']:,}...")

    removed = stats["total_raw"] - stats["rows_written"]
    pct_kept = (stats["rows_written"] / stats["total_raw"] * 100) if stats["total_raw"] > 0 else 0
    input_size = os.path.getsize(INPUT_FILE) / (1024 * 1024)
    output_size = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)

    print(f"\n  Total raw rows:           {stats['total_raw']:>10,}")
    print(f"  Rows written (clean):     {stats['rows_written']:>10,}")
    print(f"  Rows removed:             {removed:>10,}")
    print(f"  Data retained:            {pct_kept:>9.1f}%")
    print(f"\n  --- Removal Breakdown ---")
    for k in ["duplicate_headers","empty_trade_value","zero_trade_value","negative_trade_value","empty_partner","aggregate_partner","aggregate_hs_code","empty_hs_code","invalid_numeric","exact_duplicates"]:
        print(f"  {k.replace('_',' ').title()+':':28s}{stats[k]:>10,}")
    print(f"\n  Input:  {input_size:>9.1f} MB")
    print(f"  Output: {output_size:>9.1f} MB")
    print(f"\n  Cleaning complete! Ready for HDFS ingestion.")

if __name__ == "__main__":
    main()
