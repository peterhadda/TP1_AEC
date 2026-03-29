import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import CONFIG


METRICS = [
    ("severity_index", "Indice de severite du crime", "severity_crime_pie.png"),
    ("essence_ordinaire_cents_litre", "Prix de l'essence (cents/litre)", "gas_prices.png"),
    ("avg_temperature", "Temperature moyenne (C)", "weather.png"),
]


def load_data() -> pd.DataFrame:
    input_path = CONFIG["processed_dir"] / CONFIG["output_file"]
    with open(input_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rows = []
    for province, values in raw.items():
        row = {"province": province}
        row.update(values)
        rows.append(row)

    return pd.DataFrame(rows)


def to_numeric(series: pd.Series) -> pd.Series:
    as_string = series.astype(str).str.replace("%", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(as_string, errors="coerce")


def save_bar_chart(df: pd.DataFrame, column: str, title: str, filename: str) -> None:
    chart_df = df[["province", column]].copy()
    chart_df[column] = to_numeric(chart_df[column])
    chart_df = chart_df.dropna(subset=[column]).sort_values(column, ascending=False)

    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab20(range(len(chart_df)))
    plt.bar(chart_df["province"], chart_df[column], color=colors)
    plt.title(title)
    plt.xlabel("Province")
    plt.ylabel(column)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_dir = CONFIG["processed_dir"] / "graphs"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / filename, dpi=150)
    plt.close()


def save_pie_chart(df: pd.DataFrame, column: str, title: str, filename: str) -> None:
    chart_df = df[["province", column]].copy()
    chart_df[column] = to_numeric(chart_df[column])
    chart_df = chart_df.dropna(subset=[column]).sort_values(column, ascending=False)

    plt.figure(figsize=(9, 9))
    plt.pie(
        chart_df[column],
        labels=chart_df["province"],
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title(title)
    plt.tight_layout()

    output_dir = CONFIG["processed_dir"] / "graphs"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / filename, dpi=150)
    plt.close()


def main() -> None:
    df = load_data()
    for column, title, filename in METRICS:
        if column in df.columns:
            if column == "severity_index":
                save_pie_chart(df, column, title, filename)
            else:
                save_bar_chart(df, column, title, filename)
            print(f"Graphique cree: {filename}")
        else:
            print(f"Colonne absente, ignoree: {column}")


if __name__ == "__main__":
    main()
