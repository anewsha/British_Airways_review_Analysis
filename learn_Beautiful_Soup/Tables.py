
from bs4 import BeautifulSoup as bs
import pandas as pd
tabScript = """<table class="type 1 table">
    <tr>
      <th>Month</th>
      <th>Savings</th>
    </tr>
    <tr>
      <td>March</td>
      <td>$400</td>
    </tr>
    <tr>
      <td>April</td>
      <td>$300</td>
    </tr>
  </table>  
  <table class="type 2 table">
    <thead>
        <tr>
            <th>Month</th>
            <th>Savings</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>January</td>
            <td>$100</td>
        </tr>
        <tr>
            <td>February</td>
            <td>$200</td>
        </tr>
    </tbody>
  </table>"""

soup = bs(tabScript, 'html.parser')
table = soup.find('table',{'class':'type 1 table'})
headers = table.find_all('th')
heads=[]
for header in headers:
    heads.append(header.text)
rows = []
for row in table.find_all('tr')[1:]:
    td = row.find_all('td')
    rows.append([r.text for r in td])

path = 'table.csv'
df = pd.DataFrame(rows, columns=heads)
df.to_csv(path)
print(table.find_all('tr')[1:])
