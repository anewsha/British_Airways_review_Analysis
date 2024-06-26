from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

web = requests.get('https://fastestlaps.com/tracks/adm-miachkovo')
soup = bs(web.content, 'html.parser')

table = soup.find('table', {'class':"table table-striped fl-laptimes-trackpage"})
theads = table.find('thead')
heads = theads.find_all('th')
headers = [head.text for head in heads]
tbody = table.find('tbody')
tr = tbody.find_all('tr')
rows = []
for i in tr:
    td = i.find_all('td')
    rows.append([r.text for r in td])
    
df = pd.DataFrame(rows, columns=headers)
path='FastLaps.csv'
df.to_csv(path)
print(df)