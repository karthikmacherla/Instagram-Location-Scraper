# Instagram Location Data Scraper

Given a list of location names, fetch the most relevant location tag, and fetch statistics such as number of posted pictures at that location, latitude and longitude.


# Running
1. Pull the git repo
2. Have a csv containing names of locations ready with column name `name` containing each location name.
2. Populate the fields in upper case at the top of `scrape.py`
3. Run `pipenv install`
4. Run `pipenv shell` and `python scrape.py`
