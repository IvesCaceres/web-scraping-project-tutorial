import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3


url = 'https://campeonatochileno.cl/estadisticas'
r = requests.get(url)
#print(r)
soup = BeautifulSoup(r.text,'lxml')
table = soup.find('table', class_='table m-0 p-0 responsive')

headers = table.find_all('th')
#print(headers)
titles = [i.text for i in headers]
#print(titles)

df = pd.DataFrame(columns=titles)

rows = table.find_all('tr')
for i in rows [1:]:
    data = i.find_all('td')
    row = [tr.text for tr in data]
    
    l = len(df)
    df.loc[l] = row
df['Club'] = df['Club'].str.replace('\n', '')
df.drop('Últimas 5 Fechas', axis=1, inplace=True)

#print(df)



con = sqlite3.connect('nomegustaelfutbol.db')
con.execute('create table if not exists futbol_tabla(Pos integer, Club text, PTS integer,  PJ integer,  PG integer,  PE integer,  PP integer,  GF integer,  GC integer,  DIF integer)')
con.executemany('insert into futbol_tabla values(?,?,?,?,?,?,?,?,?,?)', df.values)

con.commit()
for row in con.execute ('select *from futbol_tabla'):
    print(row)
print()
con.close()

