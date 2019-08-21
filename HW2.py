#########HW2
import requests
import folium
import json
import pandas as pd
import numpy as np
from pymongo import MongoClient
import folium
from IPython.display import HTML
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

client = MongoClient('localhost', 27017)
db = client.LA
LA_collection = db.LA_collection




params = "TrafficID,IntersectionID,lat,lon,intersection,Shape,TOOLTIP"

type(params)
params == "TrafficID,IntersectionID,lat,lon,intersection,Shape,TOOLTIP"
QueryURL = "https://maps.lacity.org/lahub/rest/services/LADOT/MapServer/21/query?where=1%3D1&outFields="+params+"&outSR=4326&f=json"
response = requests.get(QueryURL)
data = response.json()

len(data)

for keys in data:
    print(type(data[keys]))
features = data['features']
len(data) #7
type(data) # dictionary
for collision in features:
    try:
        LA_collection.insert_one(collision)
    except:
        pass

find_coll = LA_collection.find()

array = list(find_coll)
array
df_list = []

for i in array:
    df_list.append(i['attributes'])
df_list


df = pd.DataFrame(df_list)
df.info()

df.size #size = number of total data points
df.shape #shape == observations then columns

df.columns #put the useful variables into the columns

df = df.drop(columns='TOOLTIP')

df = df.rename(columns = lambda col: col.replace(" ", ""))
df['intersection'] = df['intersection'].apply(lambda x: x.upper())
df.dtypes #change intersectionID to object/str


#df.IntersectionID = df.astype({'IntersectionID': 'float64'}).dtypes

df.isnull().sum(axis=0) # many intersection IDs missing
df1 = df.copy()
df1.replace(' ', np.nan, inplace=True)

df1.replace('', np.nan, inplace = True)


# shows all the blanks
df2.loc[df['intersection'] == ' ']

df2 = df.copy()

df2 = df2[df2.intersection != ' ']

#got rid of the blanks

df2.loc[df2['intersection'] == ' ']

print("These intersections have the most collisions \n")
print(df2['intersection'].value_counts()[df2['intersection'].value_counts()>2])
#find lat/lon where the 31 is?
calc = df2['intersection'].value_counts()[df2['intersection'].value_counts()>3].plot(kind='bar')
plt.xticks(rotation = 45)

lat_lon= df.groupby(['lat', 'lon']).size().reset_index(name='Freq')
print("These exact lats and lons have more than one collision \n")

print(lat_lon.loc[lat_lon['Freq'] > 1])

lat_lon_points = lat_lon[lat_lon['Freq'] > 1]
lat_lon_points = lat_lon_points[['lat', 'lon']] # two brackets access the data points

lat_lon_tuple = [tuple(x) for x in lat_lon_points.values]

#save in tuple for mapping later

lat.dtypes

lat = df.groupby(['lat']).size().reset_index(name='Freq')

#find the lattitudes with the most accidents
print("The lattitudes with more than 3 collisions \n")

print(lat[lat['Freq'] > 3])

lat_points = lat[lat['Freq'] > 3]


lat_lonMAP = folium.Map(location =(34.052235,-118.243683))

HeatMap(lat_lon_tuple, radius=13).add_to(lat_lonMAP)

lat_lonMAP.save('lat_lonMAP.html')


lon = df.groupby(['lon']).size().reset_index(name='Freq')

print("The longitudes with more than 3 collisions \n")
print(lon[lon['Freq'] > 3])



#next plotting these areas based on lat and lon.

# makea small sample to plot points on map. 9000 + is too many
sample_points = df2.sample(n = 200)


#lat and lon come from latlong.net to be accurate

sample_map1 = folium.Map(location =(34.052235,-118.243683))

for i in range(0, len(sample_points)):
    folium.Marker([sample_points.iloc[i]['lat'], sample_points.iloc[i]['lon']], popup= sample_points.iloc[i]['intersection']).add_to(sample_map1)

sample_map1.save('sample.html')


coord1 = [ ]

#put coordinates from API data into list
#create LA map
#create heat map of the data

#make a list of tuples

for i in range(len(df2)):
    coord.append((df2.iloc[i]['lat'],df2.iloc[i]['lon']))

LA_collision_map = folium.Map(location=(34.052235,-118.243683))

HeatMap(coord,radius=13).add_to(LA_collision_map)

LA_collision_map.save('LA_collision_map1.html')
