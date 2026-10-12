# Country Data API and Analysis

A Python capstone project that scrapes country information, stores it in SQLite, exposes it through a FastAPI CRUD API, and exports the data as a CSV with a population-versus-area chart.

## Features

- Scrapes the first 20 country records from [Scrape This Site](https://www.scrapethissite.com/pages/simple/).
- Stores country name, capital, population, and area in a local SQLite database.
- Provides API endpoints to list, retrieve, create, update, and delete countries.
- Fetches API data into a CSV file and generates a scatter plot.

## Requirements

- Python 3.9 or newer
- Internet access when scraping country records

## Setup

Create and activate a virtual environment, then install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

Load the first 20 countries into the SQLite database:

```sh
python load_data.py
```

Start the API:

```sh
uvicorn api:app --reload
```

The interactive API documentation is available at <http://127.0.0.1:8000/docs>.

Run the client in a separate terminal while the API is running:

```sh
python client.py
```

The client prints the country data and writes `exported_countries.csv` and `population_vs_area.png` into the project directory.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/countries` | List all countries |
| `GET` | `/countries/{country_name}` | Get one country by name |
| `POST` | `/countries` | Create a country |
| `PUT` | `/countries/{country_name}` | Update a country's capital, population, and area |
| `DELETE` | `/countries/{country_name}` | Delete a country |

Example request body for `POST /countries`:

```json
{
  "name": "Exampleland",
  "capital": "Example City",
  "population": 100000,
  "area": 2500.5
}
```

## Project Files

- `api.py` - FastAPI application and request validation.
- `database.py` - SQLite database operations.
- `scraper.py` - Country data scraper.
- `load_data.py` - Loads scraped records into the database.
- `client.py` - Calls the API and creates CSV and chart outputs.
- `requirements.txt` - Python dependencies.

## Notes

The database is created locally when the application runs. The scraper depends on the structure and availability of the source website.