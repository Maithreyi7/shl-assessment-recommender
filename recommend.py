import pandas as pd

# Load dataset
df = pd.read_csv("shl_products.csv")

# 🔥 Convert important columns to string (VERY IMPORTANT)
df["Description"] = df["Description"].astype(str)
df["Job Levels"] = df["Job Levels"].astype(str)
df["Languages"] = df["Languages"].astype(str)

print("Welcome to SHL Assessment Recommender\n")

role = input("Enter Job Role: ").lower()
level = input("Enter Job Level (Entry/Manager/etc): ").lower()
language = input("Preferred Language: ").lower()

# Filtering
results = df.copy()

if role:
    results = results[
        results["Name"].str.lower().str.contains(role.lower(), na=False)
    ]

if level:
    results = results[
        results["Job Levels"].str.lower().str.contains(level.lower(), na=False)
    ]

if language:
    results = results[
        results["Languages"].str.lower().str.contains(language.lower(), na=False)
    ]

print("\nRecommended Assessments:\n")

if results.empty:
    print("No exact match found. Showing closest matches...\n")
    results = df[df["Description"].str.lower().str.contains(role, na=False)]

for index, row in results.head(5).iterrows():
    print("Name:", row["Name"])
    print("Length:", row["Assessment Length"])
    print("URL:", row["URL"])
    print("-" * 40)