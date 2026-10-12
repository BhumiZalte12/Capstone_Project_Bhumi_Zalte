import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"


def scrape_countries():
    # Download the webpage.
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    # Read its HTML.
    soup = BeautifulSoup(response.content, "html.parser")

    # Keep only the first 20 country blocks.
    country_blocks = soup.find_all("div", class_="country")[:20]

    if len(country_blocks) != 20:
        raise ValueError("Expected to find 20 countries. Check the webpage.")

    countries = []

    for block in country_blocks:
        country = {
            "name": block.find(
                "h3", class_="country-name"
            ).get_text(strip=True),

            "capital": block.find(
                "span", class_="country-capital"
            ).get_text(strip=True),

            "population": int(
                block.find(
                    "span", class_="country-population"
                ).get_text(strip=True)
            ),

            "area": float(
                block.find(
                    "span", class_="country-area"
                ).get_text(strip=True)
            ),
        }

        countries.append(country)

    return countries


if __name__ == "__main__":
    countries = scrape_countries()

    for number, country in enumerate(countries, start=1):
        print(
            f"{number}. {country['name']} | "
            f"Capital: {country['capital']} | "
            f"Population: {country['population']:,} | "
            f"Area: {country['area']:,.2f} sq. km"
        )

    print(f"\nSuccessfully scraped {len(countries)} countries.")
    