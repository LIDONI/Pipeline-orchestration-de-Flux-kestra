import duckdb
import pandas as pd
import sys
from pathlib import Path

# Chemins
BASE_PATH = Path("C:/Users/khali/Desktop/Projet_10/processed")
INPUT_FILE = BASE_PATH / "merged_data.csv"
OUTPUT_FILE = BASE_PATH / "revenue_by_product.csv"

# Connexion DuckDB
con = duckdb.connect()

# Lecture des données
df = pd.read_csv(INPUT_FILE)

# Enregistrement DuckDB
con.register("merged_data", df)

# Calcul du chiffre d'affaires (RÈGLE MÉTIER FINALE)
con.execute("""
CREATE OR REPLACE TABLE revenue AS
SELECT
    product_id,
    sku,
    price,
    total_sales,
    price * total_sales AS chiffre_affaires
FROM merged_data
WHERE total_sales > 0
""")

# Vérifications
row_count = con.execute("SELECT COUNT(*) FROM revenue").fetchone()[0]
total_revenue = con.execute("SELECT SUM(chiffre_affaires) FROM revenue").fetchone()[0]

print(f"Nombre de lignes CA : {row_count}")
print(f"Chiffre d'affaires total : {round(total_revenue, 2)} €")

# Test métier officiel
EXPECTED_TOTAL_REVENUE = 65652.60

if round(total_revenue, 2) != EXPECTED_TOTAL_REVENUE:
    print("TEST FAILED: chiffre d'affaires total incorrect")
    sys.exit(1)

print("TEST PASSED: calcul du chiffre d'affaires OK")

# Export CSV
df_revenue = con.execute("SELECT * FROM revenue").fetchdf()
df_revenue.to_csv(OUTPUT_FILE, index=False)

print(f"Rapport chiffre d'affaires exporté : {OUTPUT_FILE}")
