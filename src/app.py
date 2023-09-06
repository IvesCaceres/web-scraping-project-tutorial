import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import time
import matplotlib.pyplot as plt

#paso 3
url = "https://blog.nubox.com/contadores/como-se-calcula-impuesto-primera-categoria"
html_data = requests.get(url, time.sleep(2))
#paso 4
soup = BeautifulSoup(html_data.text,"html.parser")
tablas = soup.find_all('table')

for index,tabla in enumerate(tablas):
    if ("1991 al 2001" in str(tabla)):
        table_index = index

tabla_sii = pd.DataFrame(columns=["año","%","reforma"])

for row in tablas[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        agno = col[0].text.replace("\n","")
        porcentaje = col[1].text.replace("\n","")
        reforma = col[2].text.replace("\n","")
        tabla_sii = tabla_sii.append({"año":agno,"%":porcentaje,"reforma":reforma}, ignore_index=True)

tabla_sii = tabla_sii.drop(0)

tabla_sii.fillna(" ")
records = tabla_sii.to_records().tolist()

print(records)



# #inser data into sqlite3

con = sqlite3.connect("test.db")
#cursor = conecta.cursor()
con.execute("create table siitabla (id key, año integer, porcentaje text, reforma text)")
con.executemany("insert into siitabla values (?,?,?,?)", records)

##9 recuperar la info, imprime por pantalla las filas
for row in con.execute('select * from siitabla'):
    print(row)

con.close()

###10 graficar data
#tabla_sii.plot(x="año", y="%", kind="bar")

