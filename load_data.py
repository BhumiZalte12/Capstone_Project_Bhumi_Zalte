from database import CountryDatabaseManager
from scraper import scrape_countries


def main():
    countries = scrape_countries()
    database = CountryDatabaseManager()

    added = 0

    for country in countries:
        # Skip countries already stored when running this again.
        if database.get_country(country["name"]) is None:
            database.create_country(country)
            added += 1

    stored_countries = database.get_all_countries()

    print(f"New countries added: {added}")
    print(f"Total countries in database: {len(stored_countries)}")
    print("\nAndorra record:")
    print(database.get_country("Andorra"))


if __name__ == "__main__":
    main()