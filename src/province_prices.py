import pandas as pd

from config import CONFIG


WEEKLY_FOOD_BASKET = {
    "Boeuf haché, par kilogramme 5": 0.5,
    "Poulet entier, par kilogramme 5": 1.0,
    "Lait, 2 litres 5": 1.0,
    "Pain blanc, 675 grammes 6": 1.0,
    "Riz blanc, 2 kilogrammes 6": 0.25,
    "Pommes, par kilogramme 5": 1.0,
    "Bananes, par kilogramme 5": 1.0,
    "Tomates, par kilogramme 5": 0.5,
    "Laitue romaine, unité 5": 1.0,
    "Pommes de terre, 4,54 kilogrammes 5": 0.25,
}

WEEKLY_OTHER_PRODUCTS_BASKET = {
    "DÃƒÂ©odorant, 85 grammes 6": 1 / 8,
    "Dentifrice, 100 millilitres 6": 1 / 4,
    "Shampooing, 400 millilitres 6": 1 / 8,
    "DÃƒÂ©tergent ÃƒÂ  lessive, 4,43 litres 6": 1 / 10,
}


def load_prices():
    csv_path = CONFIG["raw_dir"] / "Province.csv"
    df = pd.read_csv(csv_path, sep=";", header=2, dtype=str, encoding="utf-8")
    df = df.rename(columns={df.columns[0]: "product"})
    df = df[df["product"].notna()]
    df["product"] = df["product"].str.strip()
    df = df[df["product"] != "Produits"]
    return df


def clean_numeric_columns(df, province_columns):
    for column in province_columns:
        df[column] = (
            df[column]
            .replace("..", pd.NA)
            .str.replace(",", ".", regex=False)
        )
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def compute_weighted_basket_cost(df, province, basket):
    basket_df = df[df["product"].isin(basket)].copy()
    if basket_df.empty:
        return None

    basket_df["weekly_quantity"] = basket_df["product"].map(basket)
    basket_df["weekly_cost"] = basket_df[province] * basket_df["weekly_quantity"]
    return round(basket_df["weekly_cost"].sum(skipna=True), 2)


def compute_basket_costs():
    df = load_prices()
    province_columns = [column for column in df.columns if column != "product"]
    df = clean_numeric_columns(df, province_columns)

    rows = []
    for province in province_columns:
        rows.append(
            {
                "province": province,
                "cout_hebdomadaire_nourriture_par_personne": compute_weighted_basket_cost(
                    df, province, WEEKLY_FOOD_BASKET
                ),
                "cout_hebdomadaire_autres_produits_par_personne": compute_weighted_basket_cost(
                    df, province, WEEKLY_OTHER_PRODUCTS_BASKET
                ),
            }
        )

    return pd.DataFrame(rows)


result = compute_basket_costs()
