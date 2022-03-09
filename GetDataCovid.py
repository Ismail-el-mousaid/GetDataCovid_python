
import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
prices = []
images = []

page = requests.get("https://www.worldometers.info/coronavirus/")
#print(page.content)   Get tous code html

soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())  #Code html organisé

# Search for the table and extracting it
table = soup.find('table', attrs={'id': 'main_table_countries_today'})
#print(table)

rows = table.find_all("tr", attrs={"style": ""})
for i, item in enumerate(rows):
    if i == 0:
        data.append(item.text.strip().split("\n")[1:4])
    else:
        data.append(item.text.strip().split("\n")[1:4])
#print(data)

#Transformer les data en DataFrame
import dask.dataframe as dd
dt = pd.DataFrame(data)
dt = pd.DataFrame(data[1:], columns=data[0][:12]) #Formatting the header
df = dd.from_pandas(dt,npartitions=1)
data_df = df.drop(columns=['TotalCases'])
print(data_df.head())

#Map
import folium
from flask import Flask, render_template

map2 = folium.Map(location=[33.5555, -7.7777], zoom_start=2)
map2.save("templates/map2.html")
app = Flask(__name__)

@app.route("/map2")
def hello_world():
    return render_template("map2.html")    #Deployer map dans serveur

#app.run()

coordonnees_df = pd.read_csv(r"C:\Users\user\Desktop\Emsi\sfa\Dataset Covid\time_series_covid19_confirmed_global.csv")
coordonnees_df.fillna(0, inplace=True)
for i in range(0, 120):
    for j in range(0, 120):
        if data_df['Country,Other'][i] == coordonnees_df['Country/Region'][j]:
            Lat = coordonnees_df['Lat'][j]
            Long = coordonnees_df['Long'][j]
            NewCases = data_df['NewCases'][i]
            folium.Marker(location=[Lat, Long], popup="Seattle", tooltip=NewCases).add_to(map2)

#print(data_df['NewCases'].head())
