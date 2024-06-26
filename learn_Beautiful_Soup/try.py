import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

html = requests.get("http://en.wikipedia.org/wiki/"
               "Comparison_of_text_editors")
soup = BeautifulSoup(html.content, "html.parser")
table = soup.find('table',{'class':"wikitable sortable mw-datatable sticky-header-multi sort-under"})
title = table.find("caption").text
trheads = table.find_all('tr')[:2]
heads = []
for i in trheads:
    th = i.find_all('th')
    heads.append([h.text for h in th])

trbody = table.find_all('tr')[2:]
rows = []
for tr in trbody:
    firsttd = tr.find('th').text
    td = tr.find_all('td')[:-2]
    td_last=tr.find_all('td')[-2:]

    rows.append([firsttd]+[ r.text for r in td]+[d['data-sort-value'] for d in td_last]) 

print(rows)


# with open("editors.csv", "wt+", newline="", encoding='utf-8') as f:
#     writer = csv.writer(f)
#     for row in rows:
#         csv_row = [] 
#         for cell in row.findAll(["td", "th"]):
#             csv_row.append(cell.get_text())
#         writer.writerow(csv_row)