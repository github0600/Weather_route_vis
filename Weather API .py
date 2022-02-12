#!/usr/bin/env python
# coding: utf-8

# Docs of API
# https://www.worldweatheronline.com/developer/api/docs/historical-weather-api.aspx#qparameter

# the code of the API
# https://github.com/ekapope/WorldWeatherOnline

# pip install plotly

# pip install wwo-hist




from wwo_hist import retrieve_hist_data
import pandas as pd
import plotly.graph_objects as go
import calendar




import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output




coordinations  = [('37° 52\' 5.336" S', '144° 55\' 40.452" E'),
                ('38° 19\' 57.125" S', '144° 54\' 17.831" E'),
                ('38° 51\' 34.878" S', '142° 54\' 18.281" E'), 
                ('37° 50\' 33.481" S', '135° 38\' 20.388" E'),
                ('35° 5\' 50.501" S', '128° 48\' 40.243" E'), 
                ('34° 20\' 7.398" S', '121° 35\' 19.757" E'),
                ('34° 55\' 34.99" S', '118° 45\' 4.596" E'), 
                ('35° 3\' 36.441" S', '115° 51\' 54.355" E'),
                ('30° 45\' 16.173" S', '110° 26\' 25.532" E'),
                ('12° 5\' 45.683" S', '106° 25\' 8.984" E'),
                ('6° 18\' 54.271" S', '105° 33\' 56.07" E'), 
                ('5° 15\' 14.261" S', '106° 13\' 37.411" E'),
                ('3° 42\' 37.526" S', '107° 35\' 13.608" E'), 
                ('2° 0\' 50.122" S', '107° 12\' 50.324" E'),
                ('0° 42\' 51.809" N', '105° 19\' 28.118" E'), 
                ('1° 18\' 56.371" N', '104° 19\' 31.582" E'),
                ('1° 13\' 14.328" N', '103° 52\' 6.734" E')]


# ## Getting the Data from the API



def converter(coordinations):
    #split the tuples to list
    coor_decimal_list = []
    for i in range(len(coordinations)):
        coor = []
        #Convert longtitude and latitude from minutes&seconds to degrees 
        for j in range(len(coordinations[i])): 
            #Cleanning the cooridnate to be able to calculate it and convert it it to floats
            lis = coordinations[i][j].split(" ")
            degree = int(lis[0].strip("°"))
            minutes = int(lis[1].strip("'"))
            seconds = float(lis[2].strip('"'))
            
            #Calculate the longtitude if south mulitply -1
            if lis[3] == 'S' or lis[3] == 's' or lis[3] == 'W' or lis[3] == 'w':
                longtitude_converter = -1
            else:
                longtitude_converter = 1
                
            #Convert Equation
            convert_equation = (degree  + (minutes/60) + (seconds/3600)) * longtitude_converter
            #put the longtitude and latitude into a list
            coor.append(convert_equation)
        cooridination = str(coor[0]) + ',' + str(coor[1])
        
        #make a list of cooridnation lists
        coor_decimal_list.append(cooridination)
    return coor_decimal_list


# These locations not found in the API
# 
# 
# 
# ('35° 5\' 50.501" S', '128° 48\' 40.243" E'), 
# ('30° 45\' 16.173" S', '110° 26\' 25.532" E'),
# ('12° 5\' 45.683" S', '106° 25\' 8.984" E'),



frequency=24
start_date = '01-JUNE-2019'
end_date = '01-JUNE-2020'
api_key = '34801822cbb44f8fb8d170233221202'


locations_list = converter(coordinations)
locations = ['-35.09736138888889,128.81117861111113', '-30.7544925,110.44042555555556', '-12.096023055555555,106.41916222222223']
#for i in locations:
#   location_list.remove(i)

hist_weather_data = retrieve_hist_data(api_key,
                                    location_list,
                                    start_date,
                                    end_date,
                                    frequency,
                                    location_label = False,
                                    store_df = True)

#export_csv = True


# ## Clean Data




#locations_list = converter(coordinations)
data = pd.DataFrame(columns=['date_time', 'tempC', 'location'])
for i in range(len(locations_list)):
    #to handle the empty locations
    try:
        df = pd.read_csv("{}.csv".format(locations_list[i]))[['date_time', 'tempC']]
    except:
        print("Can't open file {}".format(locations_list[i]))
        continue
    df['date_time'] = pd.to_datetime(df['date_time'])
    df = df.astype({'tempC': 'int32'})
    df = df.resample('2W', on='date_time',loffset='1W').mean()
    
    ##
    df['location'] = locations_list[i] 
    df.reset_index(inplace=True)
    data = data.append(df)    


# ### Get week number in a month




data['week_year'] = data['date_time'].dt.isocalendar().week
data['year'] = data['date_time'].dt.year
data['month'] = data['date_time'].dt.month


# ### Split location to Longtiude and Latitude




data[['lat','long']] = data['location'].str.split(',',expand=True)



# ## Visualization




app = dash.Dash(__name__)


#pp['month'] = pp['month'].apply(lambda x: calendar.month_abbr[x])

years = data['year'].value_counts().keys().sort_values(ascending=True)
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Weather Visualization with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label":year, "value": year}for year in years
                   ],
                 multi=False,
                 value=2019,
                 style={'width': "25%"}
                 ),
    dcc.Slider(id="slct_week",
              step=None
              ),
    html.Hr(),

    html.Div(id='display-selected-values'),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])

# take the selected year to build the slider info (weeks) 
@app.callback(
    Output('slct_week', 'marks'),
    Output('slct_week', 'min'),
    Output('slct_week', 'max'),
    Output('slct_week', 'value'),
    Input('slct_year', 'value'))
def set_week_options(selected_year):
    week = data[data['year']==selected_year]['week_year'].value_counts().keys().sort_values(ascending=True)
    string = list(map(str, week)) 
    dictionary = dict(zip(week, string))
    return dictionary, week[0], week[-1], week[0]

@app.callback(
    Output('display-selected-values', 'children'),
    Input('slct_year', 'value'),
    Input('slct_week', 'value'))
def set_display_children(selected_year, selected_week):
    return u'{} week in {}'.format(selected_week, selected_year,)



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
    Input(component_id='slct_week', component_property='value')]
)
 

def update_graph(option_slctd, week_slctd):
    
    container = "The year chosen by user was: {}".format(option_slctd)
    df = data.copy()
    df = df[(df["year"] == option_slctd) & (df["week_year"] == week_slctd)]

    # Plotly Express
    fig = go.Figure(go.Densitymapbox(lat=df.lat, 
                                     lon=df.long, 
                                     z=df.tempC,
                                     radius=10))
   
    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=180)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    

    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)







