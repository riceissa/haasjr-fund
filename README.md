# Haas, Jr. Fund

This is for Vipul Naik's [Donations List Website](https://github.com/vipulnaik/donations).

See https://github.com/vipulnaik/donations/issues/92 for the issue on DLW repo.

See https://www.haasjr.org/grants/search for data source.

## Instructions for doing a run

```bash
# If you need to scrape the data, run scrape.py first. Note that this script
# uses a somewhat sketchy method for detecting when to stop scraping (it checks
# for a particular error message), so if the script seems to go on forever, make
# sure it is actually collecting data.
./scrape.py lol.csv

# Once you have the CSV, run proc.py.
./proc.py lol.csv > lmao.sql
```

## License

CC0 for scripts, not sure about the data.
