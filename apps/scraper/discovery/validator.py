import csv
import logging
from concurrent.futures import ThreadPoolExecutor

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = "docs/MUNICIPAL_SOURCES.csv"


def validate_url(row):
    url = row.get("URL")
    if not url or row.get("Status") == "Verified":
        return row

    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; LeyesMxBot/0.1)"}
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)

        if response.status_code == 200:
            row["Status"] = "Verified"
            row["Notes"] += f" [Auto-Verified: Status 200, Size {len(response.text)}]"
        else:
            row["Notes"] += f" [Check Failed: Status {response.status_code}]"

    except Exception as e:
        row["Notes"] += f" [Check Failed: {str(e)}]"

    return row


def main():
    rows = []
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Validating {len(rows)} sources...")

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(validate_url, rows))

    with open(CSV_PATH, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("Validation complete. Updated registry.")


if __name__ == "__main__":
    main()
