import json, os

OUTPUT_DIR = "/home/vboxuser/export-analyzer/output"

data = {
    "metadata": {"project": "Export Trade Data Analyzer", "source": "UN Comtrade",
                  "records": "600,000", "period": "2018-2023", "reporter": "China", "jobs": 6},
    "job1_export_volume": [], "job2_top_products": {}, "job3_price_trends": {},
    "job4_growth_rate": [], "job5_volume_by_year": {}, "job6_products_by_year": {}
}

f = open(os.path.join(OUTPUT_DIR, "job1_export_volume.tsv"))
for line in f:
    parts = line.strip().split("\t")
    if len(parts) >= 3:
        data["job1_export_volume"].append({"country": parts[0],
            "total_value": round(float(parts[1]), 2), "record_count": int(parts[2])})
f.close()
data["job1_export_volume"].sort(key=lambda x: x["total_value"], reverse=True)

f = open(os.path.join(OUTPUT_DIR, "job2_top_products.tsv"))
products = {}
for line in f:
    parts = line.strip().split("\t")
    if len(parts) >= 5:
        country = parts[0]
        entry = {"hs_code": parts[1], "description": parts[2],
                 "total_value": round(float(parts[3]), 2), "record_count": int(parts[4])}
        if country not in products: products[country] = []
        products[country].append(entry)
f.close()
for c in products:
    products[c].sort(key=lambda x: x["total_value"], reverse=True)
    products[c] = products[c][:10]
data["job2_top_products"] = products

f = open(os.path.join(OUTPUT_DIR, "job3_price_trends.tsv"))
trends = {}
for line in f:
    parts = line.strip().split("\t")
    if len(parts) >= 7:
        key = parts[0] + " - " + parts[1]
        entry = {"year": int(parts[2]), "avg_price": round(float(parts[3]), 2),
                 "min_price": round(float(parts[4]), 2), "max_price": round(float(parts[5]), 2),
                 "sample_count": int(parts[6])}
        if key not in trends: trends[key] = []
        trends[key].append(entry)
f.close()
for p in trends: trends[p].sort(key=lambda x: x["year"])
data["job3_price_trends"] = trends

f = open(os.path.join(OUTPUT_DIR, "job4_growth_rate.tsv"))
for line in f:
    parts = line.strip().split("\t")
    if len(parts) >= 6:
        data["job4_growth_rate"].append({"country": parts[0], "year_from": parts[1],
            "year_to": parts[2], "value_from": round(float(parts[3]), 2),
            "value_to": round(float(parts[4]), 2), "growth_pct": round(float(parts[5]), 2)})
f.close()
data["job4_growth_rate"].sort(key=lambda x: x["growth_pct"], reverse=True)

f = open(os.path.join(OUTPUT_DIR, "job5_volume_by_year.tsv"))
vol_year = {}
for line in f:
    parts = line.strip().split("\t")
    if len(parts) >= 4:
        country = parts[0]
        entry = {"year": int(parts[1]), "value": round(float(parts[2]), 2), "record_count": int(parts[3])}
        if country not in vol_year: vol_year[country] = []
        vol_year[country].append(entry)
f.close()
for c in vol_year: vol_year[c].sort(key=lambda x: x["year"])
data["job5_volume_by_year"] = vol_year

f = open(os.path.join(OUTPUT_DIR, "job6_products_by_year.tsv"))
prod_year = {}
for line in f:
    parts = line.strip().split("\t")
    if len(parts) >= 5:
        year = parts[0]
        entry = {"hs_code": parts[1], "description": parts[2],
                 "total_value": round(float(parts[3]), 2), "record_count": int(parts[4])}
        if year not in prod_year: prod_year[year] = []
        prod_year[year].append(entry)
f.close()
for y in prod_year:
    prod_year[y].sort(key=lambda x: x["total_value"], reverse=True)
    prod_year[y] = prod_year[y][:10]
data["job6_products_by_year"] = prod_year

out_file = os.path.join(OUTPUT_DIR, "dashboard_data.json")
with open(out_file, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

size = os.path.getsize(out_file) / 1024
print(f"JSON created: {out_file} ({size:.0f} KB)")
print(f"  Countries: {len(data['job1_export_volume'])}")
print(f"  Markets: {len(data['job2_top_products'])}")
print(f"  Price trends: {len(data['job3_price_trends'])}")
print(f"  Growth records: {len(data['job4_growth_rate'])}")
print(f"  Yearly data: {len(data['job5_volume_by_year'])}")
print(f"  Year rankings: {len(data['job6_products_by_year'])}")
