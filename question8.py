"""
The wanted part of the link is in between '//' and '</'. I would read the links as string and split the the parts.
Since the url would be in <url>...</url> xml tags, the part that should be removed from the end is after '</'.
Also the head part which is '...//' does not wanted so '//' could be used as a key to split.
Of course this code would only work if the data is exactly like given.
If we are extracting the data from a webpage, since other xml tags will exist, I would have used BeautifulSoup. 
The code has been written based on the data provided as a picture.
"""
import pandas as pd
d = {"Device_Type" : ["AXO145","TRU151","ZOD231","YRT326","LWR245"],
 "Stat_Access_Link" : ["<url>https://xcd32112.smart_meter.com</url>",
                       "<url>http://tXh67.dia_meter.com</url>",
                       "<url>https://yT5495.smart_meter.com</url>",
                       "<url>https://ret323_TRu.crown.com</url>",
                       "<url>https://luwr3243.celcius.com</url>"]}
df = pd.DataFrame(d)
lst = []
for row in df.itertuples():
    lst.append(row.Stat_Access_Link.split("//")[1].split("</")[0])
lst
df['Pure_Url'] = lst
print(df)
