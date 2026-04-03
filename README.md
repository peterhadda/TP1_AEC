# TP1_AEC

Projet Python qui agrège plusieurs indicateurs par province canadienne et génère:
- un fichier JSON consolidé
- des graphiques (barres + circulaire)
- Notre Donnees organiser provinces_data.json

## Structure

- `src/main.py` : construit le JSON final à partir des scripts de collecte
- `src/bar_charts.py` : génère les graphes à partir du JSON final
- `src/config.py` : configuration centrale (sources, champs, mapping provinces)
- `data/processed/provinces_data.json` : sortie consolidée
- `data/processed/graphs/` : images des graphes

## Prérequis

- Python 3.10+ (idéalement 3.13 comme dans ton environnement)
- Dépendances:

```bash
pip install pandas requests matplotlib lxml
```

## Exécution

1. Générer/mettre à jour les données consolidées:

```bash
python src/main.py
```

2. Générer les graphes:

```bash
python src/bar_charts.py
```

## Graphes générés

- `severity_crime_pie.png` : répartition du `severity_index` (graphique circulaire)
- `gas_prices.png` : `essence_ordinaire_cents_litre` (barres colorées)
- `weather.png` : `avg_temperature` (barres colorées)

Les fichiers sont enregistrés dans `data/processed/graphs/`.

## Notes

- Le champ crime utilise `severity_index` (et non `total crime rate`).
- `auto_insurance` a été retiré de la configuration et du pipeline.
