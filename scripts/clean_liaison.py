import duckdb
import pandas as pd
import sys
from pathlib import Path

# Chemin du fichier
INPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/bottleneck/liaison.xlsx")
OUTPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/processed/liaison_clean.csv")

# Crée le dossier processed si nécessaire
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Connexion DuckDB
con = duckdb.connect()

# Lecture du fichier Excel
df_liaison = pd.read_excel(INPUT_FILE)

# Chargement dans DuckDB
con.register("liaison_raw", df_liaison)

# Dédoublonnage
con.execute("""
CREATE OR REPLACE TABLE liaison_clean AS
SELECT DISTINCT *
FROM liaison_raw;
""")

# Vérification du nombre de lignes
row_count = con.execute("SELECT COUNT(*) FROM liaison_clean").fetchone()[0]
print(f"Nombre de lignes après dédoublonnage liaison : {row_count}")

# Test métier
EXPECTED_ROWS = 825
if row_count != EXPECTED_ROWS:
    print("TEST FAILED: nombre de lignes incorrect")
    sys.exit(1)

print("TEST PASSED: dédoublonnage liaison OK")

# Export CSV
df_clean = con.execute("SELECT * FROM liaison_clean").fetchdf()
df_clean.to_csv(OUTPUT_FILE, index=False)
print(f"Fichier exporté : {OUTPUT_FILE}")
