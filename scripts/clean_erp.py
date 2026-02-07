import duckdb
import pandas as pd
import sys
from pathlib import Path

# Chemin complet du fichier ERP
INPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/bottleneck/erp.xlsx")

# Dossier et fichier de sortie
OUTPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/processed/erp_clean.csv")

# Crée le dossier processed si nécessaire
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Connexion DuckDB (en mémoire)
con = duckdb.connect()

# Lecture du fichier Excel
df_erp = pd.read_excel(INPUT_FILE)

# Chargement dans DuckDB
con.register("erp_raw", df_erp)

# Dédoublonnage SQL
con.execute("""
CREATE OR REPLACE TABLE erp_clean AS
SELECT DISTINCT *
FROM erp_raw;
""")

# Vérification du nombre de lignes
row_count = con.execute("SELECT COUNT(*) FROM erp_clean").fetchone()[0]
print(f"Nombre de lignes après dédoublonnage ERP : {row_count}")

# TEST METIER (fail fast)
EXPECTED_ROWS = 825
if row_count != EXPECTED_ROWS:
    print("TEST FAILED: nombre de lignes incorrect")
    sys.exit(1)

print("TEST PASSED: dédoublonnage ERP OK")

# Export du résultat en CSV
df_clean = con.execute("SELECT * FROM erp_clean").fetchdf()
df_clean.to_csv(OUTPUT_FILE, index=False)
print(f"Fichier exporté : {OUTPUT_FILE}")
