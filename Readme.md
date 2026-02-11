# Pipeline d’orchestration de flux BottleNeck avec Kestra

## Contexte

BottleNeck est un marchand de vin disposant de deux systèmes sources :
- **ERP** : ventes internes
- **CMS Web** : e-commerce

Une première analyse réalisée par le Data Analyst a permis de :
- nettoyer et réconcilier les données
- calculer le **chiffre d’affaires**
- identifier les **vins premium** à l’aide de la méthode statistique **z-score**

 **Objectif** : industrialiser et automatiser cette chaîne de traitement avec **Kestra**, incluant :
- contrôle qualité automatique
- livrables métiers mensuels
- exécution planifiée

---

##  Architecture du pipeline (Data Lineage)

![Diagramme des flux](kestra/Diagramme-des-flux.png)

Le pipeline se compose des étapes suivantes :

1. **Ingestion des sources** : ERP.xlsx, LIAISON.xlsx, WEB.xlsx  
2. **Nettoyage & normalisation** : suppression des valeurs manquantes, harmonisation des colonnes  
3. **Dédoublonnage (DuckDB)** : suppression des doublons, contrôle des volumes  
4. **Fusion des données** : jointures via le fichier de liaison  
5. **Calculs métiers** : chiffre d’affaires par produit et total  
6. **Identification vins premium** : z-score > 2  
7. **Exports finaux** : `report.xls`, `vins_premium.csv`, `vins_ordinaires.csv`  
8. **Tests & contrôles qualité** : tests après chaque étape critique, blocage si échec

---

## 📂 Structure du projet

├── data/
│ ├── raw/ # Fichiers sources (xlsx)

│ ├── clean/ # Données nettoyées

│ ├── dedup/ # Données dédoublonnées

│ └── output/ # Livrables métiers
│

├── scripts/

│ ├── clean_erp.py

│ ├── clean_liaison.py

│ ├── clean_web.py

│ ├── zscore_identification.py

│ └── export_excel.py
│

├── kestra/ # Diagrammes et fichiers Kestra

│ └── Diagramme-des-flux.png
│
├── flow.yaml # Workflow Kestra

└── README.md

---

## Orchestration avec Kestra

- Exécution séquentielle de toutes les étapes
- Tests bloquants après chaque étape critique
- Génération automatique des livrables finaux

### Planification

- **Tous les 15 du mois à 09:00**
- Fuseau horaire : Europe/Paris
- Cron : `0 9 15 * *`

---

## Tests & validation

| Étape | Test | Résultat attendu |
|-------|------|----------------|
| Nettoyage ERP | Null values | 825 lignes |
| Nettoyage LIAISON | Null values | 825 lignes |
| Nettoyage WEB | Null values | 1428 → 714 |
| Fusion finale | Count lignes | 714 |
| CA total | Somme | 70 568.60 € |
| Z-score | Vins premium | 30 |

> Tout test KO bloque le pipeline et génère des logs dans Kestra.

---

## Livrables métiers

- **Report Excel** : `report.xls`
  - Feuille 1 : CA par produit
  - Feuille 2 : CA total
- **CSV** : `vins_premium.csv` / `vins_ordinaires.csv`

---

## Gestion des incidents

- Retry automatique sur erreur ou indisponibilité
- Logs centralisés dans Kestra
- Relance manuelle possible étape par étape
- Scripts idempotents pour éviter les doublons

---

## Conclusion

- Pipeline reproductible et fiable
- Tests intégrés pour garantir la qualité
- Exécution automatique mensuelle
- Résultats conformes aux attentes métier

# 👤 Owner

<h1 align="center">Hi 👋, I'm khalid</h1>
<h3 align="center"> Data & Cloud Engineer|| Power BI and Qlik sense developer</h3>

Ce projet a été réalisé par :

**khalid OURO-ADOYI**  

📧 Email : khalidouroadoyi@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/khalid-ouro-adoyi/) | [GitHub](https://github.com/LIDONI)
- 📫 How to reach me **khalidouroadoyi@gmail.com**

- 👨‍💻 All of my projects are available at [https://github.com/lidoni?tab=repositories](https://github.com/lidoni?tab=repositories)

- 📄You can see my presentations in my linkedin posts [https://www.linkedin.com/in/khalid-ouro-adoyi/](https://www.linkedin.com/in/khalid-ouro-adoyi/)
