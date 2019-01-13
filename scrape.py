#!/usr/bin/env python3

import requests
import sys
from bs4 import BeautifulSoup

def main():
    url_base = "https://www.haasjr.org/grants/search?page="
    page = 0

    with open(sys.argv[1], "w", newline="") as f:
        has_next = True
        while has_next:
            url = url_base + str(page)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            tables = soup.find_all("table", {"class": "grants-search-results-table"})
            assert len(tables) == 1, "Error: there must be exactly one grants table on the page"
            table = tables[0]

            headers_found = list(map(lambda x: x.text.strip(), table.find_all("th")))
            headers_expected = ['Grantee', 'Grant Info', 'Year', 'Amount', 'Issue Area',
                                'Sub-Issue Area']
            assert headers_found == headers_expected
            # Build header access map so that we can say cells[h[key]] rather than
            # cells[idx]
            h = {key: idx for idx, key in enumerate(headers_expected)}

            for row in table.find("tbody").find_all("tr"):
                cells = row.find_all("td")
                grantee = cells[h["Grantee"]].text.strip()
                grantee_url = cells[h["Grantee"]].a.get("href").strip()

            page += 1


if __name__ == "__main__":
    main()
