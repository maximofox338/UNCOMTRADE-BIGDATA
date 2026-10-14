import json, csv, time, sys, os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

API_KEY = sys.argv[1] if len(sys.argv) > 1 else None
OUTPUT_FILE = "china_exports.csv"
CHINA_CODE = "156"
YEARS = ["2018", "2019", "2020", "2021", "2022", "2023"]

CSV_HEADER = [
    "year", "trade_flow", "reporter", "partner",
    "hs_code", "hs_description",
    "trade_value_usd", "net_weight_kg", "quantity", "quantity_unit"
]

def fetch_json(url, headers=None):
    req = Request(url)
    if headers:
        for key, val in headers.items():
            req.add_header(key, val)
    try:
        response = urlopen(req, timeout=60)
        return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        print(f"    HTTP Error {e.code}: {e.reason}")
        if e.code == 429:
            print("    Rate limited. Waiting 60s...")
            time.sleep(60)
            return fetch_json(url, headers)
        return None
    except (URLError, Exception) as e:
        print(f"    Error: {e}")
        return None

def download_full_mode(api_key):
    print("  MODE: Full API (with subscription key)")
    print("  Limit: 100,000 records per request\n")
    all_records = []
    base_url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
    headers = {"Ocp-Apim-Subscription-Key": api_key}

    for i, year in enumerate(YEARS):
        print(f"  [{i+1}/{len(YEARS)}] Downloading year {year}...", flush=True)
        params = {"reporterCode": CHINA_CODE, "flowCode": "X", "period": year,
                  "maxRecords": "100000", "includeDesc": "true"}
        url = f"{base_url}?{urlencode(params)}"
        data = fetch_json(url, headers)

        if data and "data" in data and data["data"]:
            for r in data["data"]:
                all_records.append({
                    "year": r.get("period", year), "trade_flow": "Export",
                    "reporter": r.get("reporterDesc", "China"),
                    "partner": r.get("partnerDesc", ""),
                    "hs_code": r.get("cmdCode", ""),
                    "hs_description": r.get("cmdDesc", ""),
                    "trade_value_usd": r.get("primaryValue", 0),
                    "net_weight_kg": r.get("netWgt", 0),
                    "quantity": r.get("qty", 0),
                    "quantity_unit": r.get("qtyUnitAbbr", "")
                })
            print(f"    -> {len(data['data'])} records downloaded")
        else:
            print(f"    -> No data or error")
        time.sleep(3)
    return all_records

def save_csv(records, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()
        writer.writerows(records)
    size = os.path.getsize(filename) / (1024 * 1024)
    print(f"\n  Saved: {filename}")
    print(f"  Records: {len(records):,}")
    print(f"  Size: {size:.1f} MB")

def main():
    print(f"\n  Reporter: China | Flow: Exports | Years: {', '.join(YEARS)}\n")
    if API_KEY:
        records = download_full_mode(API_KEY)
    else:
        print("  ERROR: API key required. Usage: python download_comtrade.py YOUR_KEY")
        sys.exit(1)
    if records:
        save_csv(records, OUTPUT_FILE)

if __name__ == "__main__":
    main()
