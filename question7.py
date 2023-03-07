import pandas as pd
import numpy as np
import mysql
import mysql.connector as sql
connection = sql.connect(user = '_root_',
                         host = '_localhost_',
                         passwd = '_password_',
                         database = '_database_',
                         auth_plugin = 'mysql_native_password',
                         buffered = True)

mycursor = connection.cursor()
file_path = "country_vaccination_stats.csv"
df = pd.read_csv(file_path)
#replace the NaN values with -1. Because mysql cannot take null values. -1 is known to be an impossible value.
df['daily_vaccinations'].fillna(-1,inplace=True)
create_table_query = """
CREATE TABLE data (
  country VARCHAR(40),
  date VARCHAR(20),
  daily_vaccinations INT,
  vaccines VARCHAR(40)
  );
"""
mycursor.execute(create_table_query)
insert_query = """
                 INSERT INTO data(country,date,daily_vaccinations,vaccines)
                 VALUES (%s,%s,%s,%s)
                 """
for row in df.itertuples():
    mycursor.execute(insert_query,
                     (row.country,
                     row.date,
                     row.daily_vaccinations,
                     row.vaccines)
                     )
   
  num_data_query = """
CREATE TABLE num_data (SELECT *,ROW_NUMBER() OVER (PARTITION BY country ORDER BY daily_vaccinations ASC) AS row_num
FROM work.data);
SELECT * FROM num_data;
"""
mycursor.execute(num_data_query)

med_data_query = """
CREATE TABLE med_data (SELECT max_row_data.country, (FLOOR(max_row_data.max_row_num/2)) AS median_f,(CEIL(max_row_data.max_row_num/2)) AS median_c
FROM (SELECT country, MAX(row_num) AS max_row_num
FROM num_data
GROUP BY country) AS max_row_data
GROUP BY max_row_data.country);
"""
mycursor.execute(med_data_query)

median_by_country_query = """
CREATE TABLE median_by_country (SELECT n.country, AVG(n.daily_vaccinations) AS median
FROM num_data AS n, med_data AS m
WHERE n.country = m.country AND (n.row_num = m.median_f OR n.row_num = m.median_c)
GROUP BY n.country);
"""
mycursor.execute(median_by_country_query)

update_query = """
UPDATE work.data
SET daily_vaccinations = 
(SELECT median
FROM median_by_country
WHERE work.data.country = median_by_country.country)
WHERE work.data.daily_vaccinations = -1;
"""
mycursor.execute(update_query)

second_update_query = """
UPDATE work.data
SET daily_vaccinations = 0
WHERE work.data.daily_vaccinations = -1;
"""
mycursor.execute(second_update_query)
