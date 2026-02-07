import json
import re
from pathlib import Path

import requests
from lxml import html

URL = "https://www.diputados.gob.mx/LeyesBiblio/regla.htm"
BASE_URL = "https://www.diputados.gob.mx/LeyesBiblio/"


def fetch_reglamentos(local_file=None):
    if local_file:
        with open(local_file, "r", encoding="iso-8859-1") as f:
            content = f.read()
    else:
        response = requests.get(URL)
        response.encoding = "iso-8859-1"  # Site uses legacy encoding
        content = response.text

    tree = html.fromstring(content)

    reglamentos = []

    # Find all links to PDFs in regley/ or Regla/ folders
    # The reglamentos page may use different PDF path conventions
    links = tree.xpath('//a[contains(@href, "regley/") or contains(@href, "Regla/")]')

    seen_urls = set()

    for link in links:
        href = link.get("href")
        if not href or not href.endswith(".pdf"):
            continue

        full_url = BASE_URL + href if not href.startswith("http") else href
        clean_url = full_url.split("#")[0]

        if clean_url in seen_urls:
            continue
        seen_urls.add(clean_url)

        # Heuristic to find title:
        # In Diputados site, usually:
        # <tr>
        #   <td> Title </td>
        #   <td> Link to PDF </td>
        # </tr>

        row = link.xpath("./ancestor::tr[1]")
        if not row:
            continue
        row = row[0]

        cells = row.findall("td")
        if not cells:
            continue

        # Title is usually in the first or second cell
        title = ""
        for cell in cells:
            text = cell.text_content().strip()
            if len(text) > 10 and not text.endswith(".pdf"):
                title = text
                break

        if not title:
            # Fallback
            title = Path(href).stem.replace("_", " ").title()

        # Extract ID (slug) from filename with reg_ prefix
        filename = Path(href).name
        slug = "reg_" + filename.lower().replace(".pdf", "")

        reglamentos.append(
            {
                "id": slug,
                "name": title.replace("\r", " ").replace("\n", " ").strip(),
                "url": clean_url,
                "remote_path": href,
            }
        )

    return reglamentos


def main():
    print("Crawling reglamentos catalog...")

    import sys

    local_path = "regla_dump.html" if Path("regla_dump.html").exists() else None

    reglamentos = fetch_reglamentos(local_path)

    print(f"Found {len(reglamentos)} reglamentos.")

    output_path = Path("data/discovered_reglamentos.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reglamentos, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
