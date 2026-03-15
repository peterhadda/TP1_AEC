print(1)
def calculer_taxes_quebec(montant_hors_taxe):
    """
    Calcule la TPS et la TVQ pour un montant donné et retourne les détails.

    Args:
        montant_hors_taxe (float): Le montant avant l'application des taxes.

    Returns:
        dict: Un dictionnaire contenant le montant original, la TPS, la TVQ,
              le total des taxes et le montant final.
    """
    # Taux de taxes actuels
    TPS_TAUX = 0.05  # 5%
    TVQ_TAUX = 0.09975 # 9.975%

    # Calcul des taxes
    tps = montant_hors_taxe * TPS_TAUX
    tvq = montant_hors_taxe * TVQ_TAUX

    # Calcul des totaux
    total_taxes = tps + tvq
    montant_total = montant_hors_taxe + total_taxes

    # Retourner un dictionnaire avec tous les détails
    return {
        "montant_original": montant_hors_taxe,
        "tps": tps,
        "tvq": tvq,
        "total_taxes": total_taxes,
        "montant_total": montant_total
    }

# --- Exemple d'utilisation ---
prix_item = 150.50
resultats = calculer_taxes_quebec(prix_item)

# Afficher les résultats de manière formatée
print(f"Montant original: {resultats['montant_original']:.2f} $")
print(f"TPS (5%): {resultats['tps']:.2f} $")
print(f"TVQ (9.975%): {resultats['tvq']:.2f} $")
print("--------------------")
print(f"Total des taxes: {resultats['total_taxes']:.2f} $")
print(f"Montant total avec taxes: {resultats['montant_total']:.2f} $")
