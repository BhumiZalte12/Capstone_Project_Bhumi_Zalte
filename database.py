import sqlite3
from contextlib import contextmanager
from pathlib import Path


class CountryDatabaseManager:
    def __init__(self):
        self.db_path = Path(__file__).parent / "countries.db"
        self.create_table()

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def create_table(self):
        with self.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS countries (
                    name TEXT PRIMARY KEY NOT NULL,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL
                        CHECK (population >= 0),
                    area REAL NOT NULL
                        CHECK (area >= 0)
                )
            """)

    def create_country(self, country):
        with self.connect() as connection:
            connection.execute("""
                INSERT INTO countries
                    (name, capital, population, area)
                VALUES (?, ?, ?, ?)
            """, (
                country["name"],
                country["capital"],
                country["population"],
                country["area"],
            ))

    def get_all_countries(self):
        with self.connect() as connection:
            rows = connection.execute("""
                SELECT name, capital, population, area
                FROM countries
                ORDER BY rowid
            """).fetchall()

            return [dict(row) for row in rows]

    def get_country(self, name):
        with self.connect() as connection:
            row = connection.execute("""
                SELECT name, capital, population, area
                FROM countries
                WHERE name = ?
            """, (name,)).fetchone()

            return dict(row) if row else None

    def update_country(self, name, details):
        with self.connect() as connection:
            cursor = connection.execute("""
                UPDATE countries
                SET capital = ?, population = ?, area = ?
                WHERE name = ?
            """, (
                details["capital"],
                details["population"],
                details["area"],
                name,
            ))

            return cursor.rowcount > 0

    def delete_country(self, name):
        with self.connect() as connection:
            cursor = connection.execute("""
                DELETE FROM countries
                WHERE name = ?
            """, (name,))

            return cursor.rowcount > 0