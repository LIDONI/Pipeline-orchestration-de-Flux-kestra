import duckdb
import pandas as pd
import sys
from pathlib import Path

# Chemins
BASE_PATH = Path("C:/Users/khali/Desktop/Projet_10/processed")

ERP_FILE = BASE_PATH / "erp_clean.csv"
WEB_FILE = BASE_PATH / "web_clean.csv"
LIAISON_FILE = BASE_PATH / "liaison_clean.csv"

OUTPUT_FILE = BASE_PATH / "merged_data.csv"

# Connexion DuckDB
con = duckdb.connect()

# Chargement des fichiers CSV
df_erp = pd.read_csv(ERP_FILE)
df_web = pd.read_csv(WEB_FILE)
df_liaison = pd.read_csv(LIAISON_FILE)

# Enregistrement dans DuckDB
con.register("erp", df_erp)
con.register("web", df_web)
con.register("liaison", df_liaison)

# Fusion SQL
con.execute("""
CREATE OR REPLACE TABLE merged_data AS
SELECT
    e.product_id,
    e.price,
    e.stock_quantity,
    w.sku,
    w.total_sales
FROM erp e
JOIN liaison l
    ON e.product_id = l.product_id
JOIN web w
    ON l.id_web = w.sku
""")

# Vérification du nombre de lignes
row_count = con.execute("SELECT COUNT(*) FROM merged_data").fetchone()[0]
print(f"Nombre de lignes après fusion : {row_count}")

# TEST MÉTIER
EXPECTED_ROWS = 714
if row_count != EXPECTED_ROWS:
    print(" TEST FAILED: incohérence dans la fusion des données")
    sys.exit(1)

print(" TEST PASSED: fusion ERP + Web via Liaison OK")

# Export CSV
df_merged = con.execute("SELECT * FROM merged_data").fetchdf()
df_merged.to_csv(OUTPUT_FILE, index=False)

print(f"Fichier fusionné exporté : {OUTPUT_FILE}")
