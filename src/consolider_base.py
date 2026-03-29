import json
import sqlite3
from pathlib import Path

import pandas as pd

from config import CONFIG


BASE_COLUMNS = [
    "severity_index",
    "avg_temperature",
    "unemployment_rate",
    "total_tax_rate",
    "cout_hebdomadaire_nourriture_par_personne",
    "cout_hebdomadaire_autres_produits_par_personne",
    "job_persecptive",
    "communaute_latine",
    "electricite_cents_kwh",
    "essence_ordinaire_cents_litre",
    "possibility_no_floods",
]


def to_number(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    txt = str(value).strip().replace("%", "").replace(",", ".")
    try:
        return float(txt)
    except ValueError:
        return None


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_tables(raw: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    province_rows = []
    ai_long_rows = []
    ai_wide_rows = []

    for province, values in raw.items():
        row = {"province": province}
        for col in BASE_COLUMNS:
            raw_value = values.get(col)
            if col == "job_persecptive":
                row[col] = raw_value
            else:
                row[col] = to_number(raw_value)
        province_rows.append(row)

        ai_usage = values.get("usage_de_techonologie_ia", {})
        if isinstance(ai_usage, dict):
            ai_wide = {"province": province}
            for sector, percent in ai_usage.items():
                numeric_percent = to_number(percent)
                ai_long_rows.append(
                    {
                        "province": province,
                        "secteur": sector,
                        "usage_percent": numeric_percent,
                    }
                )
                ai_wide[sector] = numeric_percent
            ai_wide_rows.append(ai_wide)

    province_df = pd.DataFrame(province_rows).sort_values("province").reset_index(drop=True)
    ai_long_df = pd.DataFrame(ai_long_rows).sort_values(["province", "secteur"]).reset_index(drop=True)
    ai_wide_df = pd.DataFrame(ai_wide_rows).sort_values("province").reset_index(drop=True)

    return province_df, ai_long_df, ai_wide_df


def save_outputs(province_df: pd.DataFrame, ai_long_df: pd.DataFrame, ai_wide_df: pd.DataFrame) -> Path:
    out_dir = CONFIG["processed_dir"] / "consolide"
    out_dir.mkdir(parents=True, exist_ok=True)

    province_csv = out_dir / "provinces_metrics.csv"
    ai_long_csv = out_dir / "ai_usage_long.csv"
    ai_wide_csv = out_dir / "ai_usage_wide.csv"
    sqlite_path = out_dir / "provinces_data.db"

    province_df.to_csv(province_csv, index=False, encoding="utf-8-sig")
    ai_long_df.to_csv(ai_long_csv, index=False, encoding="utf-8-sig")
    ai_wide_df.to_csv(ai_wide_csv, index=False, encoding="utf-8-sig")

    with sqlite3.connect(sqlite_path) as conn:
        province_df.to_sql("province_metrics", conn, if_exists="replace", index=False)
        ai_long_df.to_sql("ai_usage_long", conn, if_exists="replace", index=False)
        ai_wide_df.to_sql("ai_usage_wide", conn, if_exists="replace", index=False)

    return out_dir


def save_province_items_json(raw: dict, out_dir: Path) -> None:
    items = []
    for province, values in raw.items():
        item = {"province": province}
        item.update(values)
        items.append(item)

    items = sorted(items, key=lambda x: x["province"])

    output_path = out_dir / "provinces_items.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4, ensure_ascii=False)


def main():
    input_path = CONFIG["processed_dir"] / CONFIG["output_file"]
    raw = load_json(input_path)
    province_df, ai_long_df, ai_wide_df = build_tables(raw)
    out_dir = save_outputs(province_df, ai_long_df, ai_wide_df)
    save_province_items_json(raw, out_dir)
    print(f"Base exploitable generee dans: {out_dir}")


if __name__ == "__main__":
    main()
