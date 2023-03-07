import pandas as pd

file_path = "country_vaccination_stats.csv"
df = pd.read_csv(file_path)

"""
Implement code to list the top-3 countries with highest median daily vaccination numbers
 by considering missing values imputed version of dataset.
"""

print(df.groupby('country')['daily_vaccinations'].agg('median').sort_values(ascending=False).head(3))
