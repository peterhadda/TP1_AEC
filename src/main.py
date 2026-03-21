import json
import importlib.util
from pathlib import Path
import pandas as pd

from config import CONFIG

BASE_DIR = Path(__file__).resolve().parent


def normalize_province(name):
    if name is None or pd.isna(name):
        return None
    name = str(name).strip()
    return CONFIG["province_aliases"].get(name, name)


def import_module(script_name):
    script_path = BASE_DIR / script_name
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add_value(data, province, field, value):
    province = normalize_province(province)
    if not province:
        return

    if province not in data:
        data[province] = {}

    data[province][field] = value


def extract_from_dataframe(df, province_field, value_field, final_field, data):
    for _, row in df.iterrows():
        province = row[province_field]
        value = row[value_field]
        add_value(data, province, final_field, value)


def extract_from_dict(d, final_field, data):
    for province, value in d.items():
        add_value(data, province, final_field, value)


def extract_from_list_of_dicts(lst, province_field, value_field, final_field, data):
    for item in lst:
        province = item.get(province_field)
        value = item.get(value_field)
        add_value(data, province, final_field, value)


def process_module(module, item_config, data):
    final_field = item_config["final_field"]
    province_field = item_config["province_field"]
    value_field = item_config["value_field"]

    if hasattr(module, "df_final") and isinstance(module.df_final, pd.DataFrame):
        extract_from_dataframe(module.df_final, province_field, value_field, final_field, data)
        return

    if hasattr(module, "result") and isinstance(module.result, pd.DataFrame):
        extract_from_dataframe(module.result, province_field, value_field, final_field, data)
        return

    if hasattr(module, "data_temp") and isinstance(module.data_temp, dict):
        extract_from_dict(module.data_temp, final_field, data)
        return

    if hasattr(module, "provinces") and isinstance(module.provinces, list):
        extract_from_list_of_dicts(module.provinces, province_field, value_field, final_field, data)
        return

    if hasattr(module, "run") and callable(module.run):
        result = module.run()

        if isinstance(result, pd.DataFrame):
            extract_from_dataframe(result, province_field, value_field, final_field, data)
        elif isinstance(result, dict):
            extract_from_dict(result, final_field, data)
        elif isinstance(result, list):
            extract_from_list_of_dicts(result, province_field, value_field, final_field, data)


def main():
    all_data = {}

    for item_name, item_config in CONFIG["items"].items():
        try:
            module = import_module(item_config["script"])
            process_module(module, item_config, all_data)
            print(f"{item_name} ajoute")
        except Exception as e:
            print(f"Erreur dans {item_name}: {e}")

    output_dir = CONFIG["processed_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / CONFIG["output_file"]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"\nFichier JSON sauvegarde : {output_path}")


if __name__ == "__main__":
    main()
