from pathlib import Path

import requests
import pandas as pd
import matplotlib.pyplot as plt


API_URL = "http://127.0.0.1:8000/countries"
PROJECT_FOLDER = Path(__file__).resolve().parent


def main():
    # Fetch country records through the API.
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    countries = response.json()

    if not countries:
        raise ValueError("No countries found. Run load_data.py first.")

    # Convert the records into a table.
    df = pd.DataFrame(countries)
    df = df[["name", "capital", "population", "area"]]

    print("\nCountry data:")
    print(df.to_string(index=False))
    print(f"\nTotal countries: {len(df)}")

    # Export CSV without an extra index column.
    csv_path = PROJECT_FOLDER / "exported_countries.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"\nCSV saved: {csv_path}")

    # Plot population on X and area on Y.
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(
        df["population"],
        df["area"],
        color="steelblue",
        s=70,
        alpha=0.8,
        edgecolors="black",
    )

    ax.set_title("Population vs Area — First 20 Countries")
    ax.set_xlabel("Population")
    ax.set_ylabel("Area (sq. km)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    fig.tight_layout()

    plot_path = PROJECT_FOLDER / "population_vs_area.png"
    fig.savefig(plot_path, dpi=300)
    plt.close(fig)

    print(f"Scatter plot saved: {plot_path}")


if __name__ == "__main__":
    main()