import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import CountryDatabaseManager


app = FastAPI(title="Country Data API")
database = CountryDatabaseManager()


class CountryDetails(BaseModel):
    capital: str = Field(min_length=1)
    population: int = Field(ge=0)
    area: float = Field(ge=0, allow_inf_nan=False)


class Country(CountryDetails):
    name: str = Field(min_length=1)


@app.get("/countries")
def get_countries():
    return database.get_all_countries()


@app.get("/countries/{country_name}")
def get_country(country_name: str):
    country = database.get_country(country_name)

    if country is None:
        raise HTTPException(
            status_code=404,
            detail="Country not found",
        )

    return country


@app.post("/countries", status_code=201)
def create_country(country: Country):
    try:
        database.create_country(country.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A country with this name already exists",
        )

    return database.get_country(country.name)


@app.put("/countries/{country_name}")
def update_country(country_name: str, details: CountryDetails):
    updated = database.update_country(
        country_name,
        details.model_dump(),
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Country not found",
        )

    return database.get_country(country_name)


@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    deleted = database.delete_country(country_name)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Country not found",
        )

    return {"message": f"{country_name} deleted successfully"}