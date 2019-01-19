#!/usr/bin/env python3

import csv
import requests
import sys
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 1+1:
        print("Unexpected arg count. Please specify output file.")
        sys.exit()

    url_base = "https://www.haasjr.org/grants/search?page="
    page = 0

    with open(sys.argv[1], "w", newline="") as f:
        fieldnames = ["grantee", "grantee_url", "year", "amount", "issue_area",
                      "sub_issue_area", "grant_info"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            print("On page " + str(page), file=sys.stderr)
            url = url_base + str(page)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "lxml")

            if soup.body.find_all(text="Your search didn’t match any grants. Please try again."):
                break

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

            rows = table.find("tbody").find_all("tr")
            for index, row in enumerate(rows):

                # This is a "grant info row", which means it was processed
                # already as part of the previous row (see comment below). So
                # we can safely skip it.
                if row.get("class") == ["grants-search-grant-info-row"]:
                    continue

                cells = row.find_all("td")
                grantee = cells[h["Grantee"]].text.strip()
                grantee_url = cells[h["Grantee"]].a.get("href").strip()
                year = cells[h["Year"]].text.strip()
                amount = cells[h["Amount"]].text.strip()
                issue_area = cells[h["Issue Area"]].text.strip()
                sub_issue_area = cells[h["Sub-Issue Area"]].text.strip()

                # The HTML table structure is pretty weird: if a grant has
                # extra "grant info", it is shown only as a [+] (to be clicked)
                # in the row for the grant, and the info itself is shown as a
                # separate row below the grant. Therefore to get the grant
                # info, we have to peek at the next row to see if it's a "grant
                # info row".
                grant_info = ""
                try:
                    if rows[index+1].get("class") == ["grants-search-grant-info-row"]:
                        grant_info = rows[index+1].text.strip()
                except IndexError:
                    pass

                writer.writerow({
                    "grantee": grantee,
                    "grantee_url": grantee_url,
                    "year": year,
                    "amount": amount,
                    "issue_area": issue_area,
                    "sub_issue_area": sub_issue_area,
                    "grant_info": grant_info,
                })

            page += 1


if __name__ == "__main__":
    main()
