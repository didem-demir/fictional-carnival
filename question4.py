import pandas as pd
import numpy as np

file_path = "/Users/macbookpro/Desktop/dersler/4-2/P.I. Works/country_vaccination_stats.csv"
df = pd.read_csv(file_path)
print(df.head())

"""
Implement code to fill the missing data (impute) in daily_vaccinations column per country
 with the minimum daily vaccination number of relevant countries.  
 Note: If a country does not have any valid vaccination number yet, fill it with “0” (zero).
"""

country_list = list(df['country'].unique())

for c in country_list:
    replace_value = 0
    if(not np.isnan(df[df['country']==c]['daily_vaccinations'].agg('min'))):
        replace_value = df[df['country']==c]['daily_vaccinations'].agg('min')
    df.loc[df['country']==c,'daily_vaccinations'] = df.loc[df['country']==c,'daily_vaccinations'].fillna(replace_value)
 
