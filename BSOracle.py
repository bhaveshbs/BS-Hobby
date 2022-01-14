#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Tue Dec 21 11:32:38 2021

# @author: bsharma
# """

#!/usr/bin/env python
# coding: utf-8


import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import numpy as np
from geopy.distance import geodesic
import pandas as pd
pd.set_option('max_rows',20)


# loading csv files as dataframes


shelter = pd.read_csv('mass_shelters.csv')
grocery = pd.read_csv('mass_veg_grocery.csv')
rest = pd.read_csv('mass_veg_rest.csv')
zipcoordinates = pd.read_excel("zip_coordinates.xlsx")


# In[32]:


# data cleaning
shelter.drop(columns=['Unnamed: 0','transactions','categories'], inplace=True)
grocery.drop(columns=['Unnamed: 0','transactions','categories'], inplace=True)
rest.drop(columns=['Unnamed: 0','transactions','categories'], inplace=True)
shelter['address'] = shelter['address'].str.replace('[',"")
shelter['address'] = shelter['address'].str.replace(']',"")
grocery['address'] = grocery['address'].str.replace('[',"")
grocery['address'] = grocery['address'].str.replace(']',"")
rest['address'] = rest['address'].str.replace('[',"")
rest['address'] = rest['address'].str.replace(']',"")
zipcoordinates['ZIP'] = zipcoordinates['ZIP'].apply(str)
zipcoordinates['LAT'] = zipcoordinates['LAT'].apply(str)
zipcoordinates['LNG'] = zipcoordinates['LNG'].apply(str)
zipcoordinates['ZIP'] = np.where(zipcoordinates['ZIP'].str.len()==3,"00"+zipcoordinates['ZIP'],zipcoordinates['ZIP'])
zipcoordinates['ZIP'] = np.where(zipcoordinates['ZIP'].str.len()==4,"0"+zipcoordinates['ZIP'],zipcoordinates['ZIP'])


# In[35]:


# user_pincode = '02478'


# In[36]:


# lat2 = zipcoordinates.loc[zipcoordinates['ZIP'] == user_pincode,:].LAT.values[0]
# lon2 = zipcoordinates.loc[zipcoordinates['ZIP'] == user_pincode,:].LNG.values[0]


# In[37]:


# adding separate columns for coordinates - grocery
lat = []
for i in range(len(grocery['coordinates'])):
  lat.append(grocery['coordinates'][i].split(': ')[1].split(',')[0])
lng = []
for j in range(len(grocery['coordinates'])):
  lng.append(grocery['coordinates'][j].split(': ')[-1].split('}')[0])

grocery['lat'] = lat
grocery['lng'] = lng


# In[38]:


# adding separate columns for coordinates - restaurants
lat = []
for i in range(len(rest['coordinates'])):
  lat.append(rest['coordinates'][i].split(': ')[1].split(',')[0])
lng = []
for j in range(len(rest['coordinates'])):
  lng.append(rest['coordinates'][j].split(': ')[-1].split('}')[0])

rest['lat'] = lat
rest['lng'] = lng


# In[39]:


# adding separate columns for coordinates - shelter
lat = []
for i in range(len(shelter['coordinates'])):
  lat.append(shelter['coordinates'][i].split(': ')[1].split(',')[0])
lng = []
for j in range(len(shelter['coordinates'])):
  lng.append(shelter['coordinates'][j].split(': ')[-1].split('}')[0])

shelter['lat'] = lat
shelter['lng'] = lng


# In[40]:


# lat1 = grocery.loc[grocery.name=='The Sweet Beet',:].lat.values[0]
# lon1 = grocery.loc[grocery.name=='The Sweet Beet',:].lng.values[0]


# In[42]:

# Combined table for all datasets    

# grocery['category'] = 'Grocery Store'
# rest['category'] = 'Restaurant'
# shelter['category'] = 'Shelter'

# result = grocery.append(rest).append(shelter)
# result.reset_index(inplace=True)
# result.drop(columns='index',inplace=True)


# result.to_csv('result0.csv')


# In[50]:


import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)


# In[52]:


from dash.dcc import Graph
from typing import Text
df = pd.read_csv('result0.csv')
dff = df.copy()
dff.drop(columns=['Unnamed: 0','review_count','zipcode','city','coordinates','lat','lng'], inplace=True)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


# ------------------------------------------------------------------------------
# App layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H3("Vegans: Nearby Search Dashboard", style={'text-align': 'center', 'color':'midnightblue'}),
    html.H4("Oracle - Interwoo Practice", style={'text-align': 'left'}),
    
   
    
    html.Div([html.H5("What is this Dashboard about?", style={'text-align': 'left','color':'midnightblue'}),"The dashboard is a resource for a vegan to locate nearby amenities. It allows users to find vegan food based on the following two criterias:- restaurants and grocery stores near their location, along with their respective ratings. ",
              "It also allows the user to find animal shelters to do volunteering work, if need be, along with their ratings. The information has been obtained from www.yelp.com API. "], style={'width':'50%','float':'left','text-align': 'left', 'text-size':'12', 'margin-bottom': '20px'}),
    html.H5("How to use this Dashboard?", style={'text-align': 'left','color':'midnightblue'}),
    
    html.Div(["Please enter your zip code, distance range, and indicate whether you are looking for restaurants, grocery stores or animal shelters in the search criteria and the dashboard will display the results, matching the criteria. ",
              "Detailed information about the search results is presented in the table below. Also, the map below shows coordinates to the nearest amenities within the specified distance range. The bar graph indicates yelp ratings of the nearby amenities. The result table is sorted by the name, rating, address, and phone number."], style={'width':'50%','float':'right','text-align': 'left', 'text-size':'12'}),
  
    
    html.Div([
        html.H6("Enter zipcode:", style={'text-align': 'left','color':'midnightblue'}),
        dcc.Input(id="input_zipcode", type="text", value="02478"),
        
        html.H6("Select a category:", style={'text-align': 'left','color':'midnightblue'}),
        dcc.Dropdown(id='select_category',
                     options=[
                         
                          {'label': 'Restaurants', 'value': 'Restaurant'},
                          {'label': 'Grocery Stores', 'value': 'Grocery Store'},
                          {'label': 'Shelters', 'value': 'Shelter'}],
                     value='Restaurant'
                  ),    
        
        html.H6("Enter distance range:", style={'text-align': 'left','color':'midnightblue'}),          
        dcc.Slider(id='select_radius',
                   min=0,
                   max=100,
                   step=0.5,
                   value=25,
                   ), 
        ]),
    html.Br(),
    html.Div([
        html.H6("Map results", style={'text-align': 'left','color':'midnightblue'}),
        dcc.Graph(id='vegan_map')
        ],
        style={'width':'50%','float':'left'}
        ),
    html.Div([
        html.H6("Ratings", style={'text-align': 'left','color':'midnightblue'}),
        dcc.Graph(id='rating_graph')
        ],
        style={'width':'50%','float':'right'}
        ),
    
    html.H3("Search results", style={'text-align': 'left','color':'midnightblue'}),
    html.Div(generate_table(dff),
             id = 'table_div',
             style={'font-size': 15 ,'width':'150%', ' float':'center'}),

    
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    [Output(component_id='vegan_map', component_property='figure'),
     Output(component_id='rating_graph', component_property='figure')],
    [Input(component_id='input_zipcode', component_property='value'),
     Input(component_id='select_category', component_property='value'),
     Input(component_id='select_radius', component_property='value')]
)

def update_graph(input_zipcode,select_category,select_radius):
    
    lat2 = zipcoordinates.loc[zipcoordinates['ZIP'] == input_zipcode,:].LAT.values[0]
    lon2 = zipcoordinates.loc[zipcoordinates['ZIP'] == input_zipcode,:].LNG.values[0]
    
    me = (lat2,lon2)
    
    lats = []
    lons = []
    names =[]
    
    if(select_category=='Restaurant'):
        a = rest.copy()
        for i in rest['name']:
            lat1 = rest.loc[rest.name==i,:].lat.values[0]
            lon1 = rest.loc[rest.name==i,:].lng.values[0]
            you = (lat1,lon1)
            miles = geodesic(me,you).miles
            if(miles <= select_radius):
                lats.append(lat1)
                lons.append(lon1)
                names.append(i)
                
    elif(select_category=='Grocery Store'):
        a = grocery.copy()
        for i in grocery['name']:
            lat1 = grocery.loc[grocery.name==i,:].lat.values[0]
            lon1 = grocery.loc[grocery.name==i,:].lng.values[0]
            you = (lat1,lon1)
            miles = geodesic(me,you).miles
            if(miles <= select_radius):
                lats.append(lat1)
                lons.append(lon1)
                names.append(i)
    elif(select_category=='Shelter'):
        a = shelter.copy()
        for i in shelter['name']:
            lat1 = shelter.loc[shelter.name==i,:].lat.values[0]
            lon1 = shelter.loc[shelter.name==i,:].lng.values[0]
            you = (lat1,lon1)
            miles = geodesic(me,you).miles
            if(miles <= select_radius):
                lats.append(lat1)
                lons.append(lon1)
                names.append(i)
        
    # mapbox_access_token = open(".mapbox_token").read()

    figure = go.Figure(go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=names,
        ))

    figure.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w',
            bearing=0,
            center=dict(
                lat=float(lat2),
                lon=float(lon2)
            ),
            pitch=0,
            zoom=10
        ),
    )

    
    data_bar = a.loc[a['name'].isin(names[:10]),:]
    fig1 = px.bar(data_bar, x='name', y='rating')

    return figure, fig1

server = app.server

@app.callback( 
    Output(component_id="table_div", component_property="children"),
    [Input(component_id='input_zipcode', component_property='value'),
     Input(component_id='select_category', component_property='value'),
     Input(component_id='select_radius', component_property='value')])

def update_table(input_zipcode,select_category,select_radius):
    
    lat2 = zipcoordinates.loc[zipcoordinates['ZIP'] == input_zipcode,:].LAT.values[0]
    lon2 = zipcoordinates.loc[zipcoordinates['ZIP'] == input_zipcode,:].LNG.values[0]
    
    me = (lat2,lon2)
    
    lats = []
    lons = []
    names =[]
    
    if(select_category=='Restaurant'):
        a = rest.copy()
        for i in rest['name']:
            lat1 = rest.loc[rest.name==i,:].lat.values[0]
            lon1 = rest.loc[rest.name==i,:].lng.values[0]
            you = (lat1,lon1)
            miles = geodesic(me,you).miles
            if(miles <= select_radius):
                lats.append(lat1)
                lons.append(lon1)
                names.append(i)
                
    elif(select_category=='Grocery Store'):
        a = grocery.copy()
        for i in grocery['name']:
            lat1 = grocery.loc[grocery.name==i,:].lat.values[0]
            lon1 = grocery.loc[grocery.name==i,:].lng.values[0]
            you = (lat1,lon1)
            miles = geodesic(me,you).miles
            if(miles <= select_radius):
                lats.append(lat1)
                lons.append(lon1)
                names.append(i)
    elif(select_category=='Shelter'):
        a = shelter.copy()
        for i in shelter['name']:
            lat1 = shelter.loc[shelter.name==i,:].lat.values[0]
            lon1 = shelter.loc[shelter.name==i,:].lng.values[0]
            you = (lat1,lon1)
            miles = geodesic(me,you).miles
            if(miles <= select_radius):
                lats.append(lat1)
                lons.append(lon1)
                names.append(i)
        
    tab = a.loc[a.name.isin(names),['name','rating','address','phone','category']]
    return generate_table(tab)

if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




