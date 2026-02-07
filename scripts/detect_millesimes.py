import duckdb
import pandas as pd
import sys
from pathlib import Path

# Paths
INPUT_FILE = Path("C:/Users/khali/Desktop/Projet_10/processed/merged_data.csv")
OUT_PREMIUM = Path("C:/Users/khali/Desktop/Projet_10/processed/vins_millesimes.csv")
OUT_STANDARD = Path("C:/Users/khali/Desktop/Projet_10/processed/vins_non_millesimes.csv")

OUT_PREMIUM.parent.mkdir(parents=True, exist_ok=True)

# Connexion DuckDB
con = duckdb.connect()

# Load data
df = pd.read_csv(INPUT_FILE)
con.register("merged", df)

# Calcul stats + z-score
con.execute("""
CREATE OR REPLACE TABLE wines_scored AS
SELECT
    *,
    (price - AVG(price) OVER ()) / STDDEV_POP(price) OVER () AS z_score
FROM merged
WHERE price IS NOT NULL
""")

# Vérifications
total_rows = con.execute("SELECT COUNT(*) FROM wines_scored").fetchone()[0]
null_z = con.execute("SELECT COUNT(*) FROM wines_scored WHERE z_score IS NULL").fetchone()[0]
premium_count = con.execute("SELECT COUNT(*) FROM wines_scored WHERE z_score > 2").fetchone()[0]

print(f"Nombre total de vins : {total_rows}")
print(f"Nombre de vins millésimés : {premium_count}")

if null_z > 0:
    print(" TEST FAILED: z-score NULL détecté")
    sys.exit(1)

if premium_count == 0:
    print(" TEST FAILED: aucun vin millésimé détecté")
    sys.exit(1)

print(" TEST PASSED: détection des vins millésimés OK")

# Export
con.execute("""
COPY (
    SELECT * FROM wines_scored WHERE z_score > 2
) TO ?
WITH (HEADER, DELIMITER ',')
""", [str(OUT_PREMIUM)])

con.execute("""
COPY (
    SELECT * FROM wines_scored WHERE z_score <= 2
) TO ?
WITH (HEADER, DELIMITER ',')
""", [str(OUT_STANDARD)])

print(f" Vins millésimés exportés : {OUT_PREMIUM}")
print(f" Vins non millésimés exportés : {OUT_STANDARD}")
