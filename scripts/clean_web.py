import duckdb
import pandas as pd
import sys
from pathlib import Path

# Chemins
INPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/bottleneck/web.xlsx")
OUTPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/processed/web_clean.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Colonnes clés
KEY_COLUMNS_WEB = ["sku", "total_sales"]

# Lecture Excel
df_web = pd.read_excel(INPUT_FILE)

# Supprimer lignes avec NaN dans les colonnes clés
df_web = df_web.dropna(subset=KEY_COLUMNS_WEB)

# Dédoublonnage sur SKU seulement (garder la première occurrence)
df_web_clean = df_web.drop_duplicates(subset=["sku"], keep="first")

# Vérification du nombre de lignes
row_count = len(df_web_clean)
print(f"Nombre de lignes après nettoyage et dédoublonnage web : {row_count}")

# Test métier
EXPECTED_ROWS = 714
if row_count != EXPECTED_ROWS:
    print("TEST FAILED: nombre de lignes incorrect")
    sys.exit(1)

print("TEST PASSED: nettoyage + dédoublonnage web OK")

# Export CSV
df_web_clean.to_csv(OUTPUT_FILE, index=False)
print(f"Fichier exporté : {OUTPUT_FILE}")

