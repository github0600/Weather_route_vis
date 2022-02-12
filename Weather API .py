{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Docs of API\n",
    "https://www.worldweatheronline.com/developer/api/docs/historical-weather-api.aspx#qparameter"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "the code of the API\n",
    "https://github.com/ekapope/WorldWeatherOnline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "pip install plotly"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "pip install wwo-hist"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "from wwo_hist import retrieve_hist_data\n",
    "import pandas as pd\n",
    "import plotly.graph_objects as go\n",
    "import calendar"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "import plotly.express as px  # (version 4.7.0)\n",
    "\n",
    "import dash  # (version 1.12.0) pip install dash\n",
    "import dash_core_components as dcc\n",
    "import dash_html_components as html\n",
    "from dash.dependencies import Input, Output"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "coordinations  = [('37° 52\\' 5.336\" S', '144° 55\\' 40.452\" E'),\n",
    "                ('38° 19\\' 57.125\" S', '144° 54\\' 17.831\" E'),\n",
    "                ('38° 51\\' 34.878\" S', '142° 54\\' 18.281\" E'), \n",
    "                ('37° 50\\' 33.481\" S', '135° 38\\' 20.388\" E'),\n",
    "                ('35° 5\\' 50.501\" S', '128° 48\\' 40.243\" E'), \n",
    "                ('34° 20\\' 7.398\" S', '121° 35\\' 19.757\" E'),\n",
    "                ('34° 55\\' 34.99\" S', '118° 45\\' 4.596\" E'), \n",
    "                ('35° 3\\' 36.441\" S', '115° 51\\' 54.355\" E'),\n",
    "                ('30° 45\\' 16.173\" S', '110° 26\\' 25.532\" E'),\n",
    "                ('12° 5\\' 45.683\" S', '106° 25\\' 8.984\" E'),\n",
    "                ('6° 18\\' 54.271\" S', '105° 33\\' 56.07\" E'), \n",
    "                ('5° 15\\' 14.261\" S', '106° 13\\' 37.411\" E'),\n",
    "                ('3° 42\\' 37.526\" S', '107° 35\\' 13.608\" E'), \n",
    "                ('2° 0\\' 50.122\" S', '107° 12\\' 50.324\" E'),\n",
    "                ('0° 42\\' 51.809\" N', '105° 19\\' 28.118\" E'), \n",
    "                ('1° 18\\' 56.371\" N', '104° 19\\' 31.582\" E'),\n",
    "                ('1° 13\\' 14.328\" N', '103° 52\\' 6.734\" E')]\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Getting the Data from the API"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "def converter(coordinations):\n",
    "    #split the tuples to list\n",
    "    coor_decimal_list = []\n",
    "    for i in range(len(coordinations)):\n",
    "        coor = []\n",
    "        #Convert longtitude and latitude from minutes&seconds to degrees \n",
    "        for j in range(len(coordinations[i])): \n",
    "            #Cleanning the cooridnate to be able to calculate it and convert it it to floats\n",
    "            lis = coordinations[i][j].split(\" \")\n",
    "            degree = int(lis[0].strip(\"°\"))\n",
    "            minutes = int(lis[1].strip(\"'\"))\n",
    "            seconds = float(lis[2].strip('\"'))\n",
    "            \n",
    "            #Calculate the longtitude if south mulitply -1\n",
    "            if lis[3] == 'S' or lis[3] == 's' or lis[3] == 'W' or lis[3] == 'w':\n",
    "                longtitude_converter = -1\n",
    "            else:\n",
    "                longtitude_converter = 1\n",
    "                \n",
    "            #Convert Equation\n",
    "            convert_equation = (degree  + (minutes/60) + (seconds/3600)) * longtitude_converter\n",
    "            #put the longtitude and latitude into a list\n",
    "            coor.append(convert_equation)\n",
    "        cooridination = str(coor[0]) + ',' + str(coor[1])\n",
    "        \n",
    "        #make a list of cooridnation lists\n",
    "        coor_decimal_list.append(cooridination)\n",
    "    return coor_decimal_list"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "These locations not found in the API\n",
    "\n",
    "\n",
    "\n",
    "('35° 5\\' 50.501\" S', '128° 48\\' 40.243\" E'), \n",
    "('30° 45\\' 16.173\" S', '110° 26\\' 25.532\" E'),\n",
    "('12° 5\\' 45.683\" S', '106° 25\\' 8.984\" E'),"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "Retrieving weather data for -37.86814888888889,144.92790333333332\n",
      "\n",
      "\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-06-01 to 2019-06-30\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:00.922808\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-07-01 to 2019-07-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:01.858501\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-08-01 to 2019-08-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:02.764584\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-09-01 to 2019-09-30\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:03.900387\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-10-01 to 2019-10-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:04.771850\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-11-01 to 2019-11-30\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:05.613414\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2019-12-01 to 2019-12-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:06.524274\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2020-01-01 to 2020-01-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:07.435999\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2020-02-01 to 2020-02-29\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:08.255778\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2020-03-01 to 2020-03-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:09.150690\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2020-04-01 to 2020-04-30\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:10.092431\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2020-05-01 to 2020-05-31\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:10.955686\n",
      "Currently retrieving data for -37.86814888888889,144.92790333333332: from 2020-06-01 to 2020-06-01\n",
      "Time elapsed (hh:mm:ss.ms) 0:00:11.182602\n",
      "\n",
      "\n",
      "export -37.86814888888889,144.92790333333332 completed!\n",
      "\n",
      "\n",
      "\n",
      "\n",
     
  

    "frequency=24\n",
    "start_date = '01-JUNE-2019'\n",
    "end_date = '01-JUNE-2020'\n",
    "api_key = '34801822cbb44f8fb8d170233221202'\n",
    "\n",
    "\n",
    "locations_list = converter(coordinations)\n",
    "locations = ['-35.09736138888889,128.81117861111113', '-30.7544925,110.44042555555556', '-12.096023055555555,106.41916222222223']\n",
    "#for i in locations:\n",
    "#   location_list.remove(i)\n",
    "\n",
    "hist_weather_data = retrieve_hist_data(api_key,\n",
    "                                    location_list,\n",
    "                                    start_date,\n",
    "                                    end_date,\n",
    "                                    frequency,\n",
    "                                    location_label = False,\n",
    "                                    store_df = True)\n",
    "\n",
    "#export_csv = True"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Clean Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-25-0f857aa1aef6>:12: FutureWarning: 'loffset' in .resample() and in Grouper() is deprecated.\n",
      "\n",
      ">>> df.resample(freq=\"3s\", loffset=\"8H\")\n",
      "\n",
      "becomes:\n",
      "\n",
      ">>> from pandas.tseries.frequencies import to_offset\n",
      ">>> df = df.resample(freq=\"3s\").mean()\n",
      ">>> df.index = df.index.to_timestamp() + to_offset(\"8H\")\n",
      "\n",
      "  df = df.resample('2W', on='date_time',loffset='1W').mean()\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Can't open file -35.09736138888889,128.81117861111113\n",
      "Can't open file -30.7544925,110.44042555555556\n",
      "Can't open file -12.096023055555555,106.41916222222223\n"
     ]
    }
   ],
   "source": [
    "#locations_list = converter(coordinations)\n",
    "data = pd.DataFrame(columns=['date_time', 'tempC', 'location'])\n",
    "for i in range(len(locations_list)):\n",
    "    #to handle the empty locations\n",
    "    try:\n",
    "        df = pd.read_csv(\"{}.csv\".format(locations_list[i]))[['date_time', 'tempC']]\n",
    "    except:\n",
    "        print(\"Can't open file {}\".format(locations_list[i]))\n",
    "        continue\n",
    "    df['date_time'] = pd.to_datetime(df['date_time'])\n",
    "    df = df.astype({'tempC': 'int32'})\n",
    "    df = df.resample('2W', on='date_time',loffset='1W').mean()\n",
    "    \n",
    "    ##\n",
    "    df['location'] = locations_list[i] \n",
    "    df.reset_index(inplace=True)\n",
    "    data = data.append(df)    "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Get week number in a month"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "data['week_year'] = data['date_time'].dt.isocalendar().week\n",
    "data['year'] = data['date_time'].dt.year\n",
    "data['month'] = data['date_time'].dt.month"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Split location to Longtiude and Latitude"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "data[['lat','long']] = data['location'].str.split(',',expand=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>date_time</th>\n",
       "      <th>tempC</th>\n",
       "      <th>location</th>\n",
       "      <th>week_year</th>\n",
       "      <th>year</th>\n",
       "      <th>month</th>\n",
       "      <th>lat</th>\n",
       "      <th>long</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2019-06-09</td>\n",
       "      <td>14.000000</td>\n",
       "      <td>-37.86814888888889,144.92790333333332</td>\n",
       "      <td>23</td>\n",
       "      <td>2019</td>\n",
       "      <td>6</td>\n",
       "      <td>-37.86814888888889</td>\n",
       "      <td>144.92790333333332</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2019-06-23</td>\n",
       "      <td>14.714286</td>\n",
       "      <td>-37.86814888888889,144.92790333333332</td>\n",
       "      <td>25</td>\n",
       "      <td>2019</td>\n",
       "      <td>6</td>\n",
       "      <td>-37.86814888888889</td>\n",
       "      <td>144.92790333333332</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2019-07-07</td>\n",
       "      <td>13.571429</td>\n",
       "      <td>-37.86814888888889,144.92790333333332</td>\n",
       "      <td>27</td>\n",
       "      <td>2019</td>\n",
       "      <td>7</td>\n",
       "      <td>-37.86814888888889</td>\n",
       "      <td>144.92790333333332</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>2019-07-21</td>\n",
       "      <td>13.357143</td>\n",
       "      <td>-37.86814888888889,144.92790333333332</td>\n",
       "      <td>29</td>\n",
       "      <td>2019</td>\n",
       "      <td>7</td>\n",
       "      <td>-37.86814888888889</td>\n",
       "      <td>144.92790333333332</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2019-08-04</td>\n",
       "      <td>13.214286</td>\n",
       "      <td>-37.86814888888889,144.92790333333332</td>\n",
       "      <td>31</td>\n",
       "      <td>2019</td>\n",
       "      <td>8</td>\n",
       "      <td>-37.86814888888889</td>\n",
       "      <td>144.92790333333332</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   date_time      tempC                               location  week_year  \\\n",
       "0 2019-06-09  14.000000  -37.86814888888889,144.92790333333332         23   \n",
       "1 2019-06-23  14.714286  -37.86814888888889,144.92790333333332         25   \n",
       "2 2019-07-07  13.571429  -37.86814888888889,144.92790333333332         27   \n",
       "3 2019-07-21  13.357143  -37.86814888888889,144.92790333333332         29   \n",
       "4 2019-08-04  13.214286  -37.86814888888889,144.92790333333332         31   \n",
       "\n",
       "   year  month                 lat                long  \n",
       "0  2019      6  -37.86814888888889  144.92790333333332  \n",
       "1  2019      6  -37.86814888888889  144.92790333333332  \n",
       "2  2019      7  -37.86814888888889  144.92790333333332  \n",
       "3  2019      7  -37.86814888888889  144.92790333333332  \n",
       "4  2019      8  -37.86814888888889  144.92790333333332  "
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Visualization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      "Dash is running on http://127.0.0.1:8050/\n",
      "\n",
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    }
   ],
   "source": [
    "app = dash.Dash(__name__)\n",
    "\n",
    "\n",
    "#pp['month'] = pp['month'].apply(lambda x: calendar.month_abbr[x])\n",
    "\n",
    "years = data['year'].value_counts().keys().sort_values(ascending=True)\n",
    "# ------------------------------------------------------------------------------\n",
    "# App layout\n",
    "app.layout = html.Div([\n",
    "\n",
    "    html.H1(\"Weather Visualization with Dash\", style={'text-align': 'center'}),\n",
    "\n",
    "    dcc.Dropdown(id=\"slct_year\",\n",
    "                 options=[\n",
    "                     {\"label\":year, \"value\": year}for year in years\n",
    "                   ],\n",
    "                 multi=False,\n",
    "                 value=2019,\n",
    "                 style={'width': \"25%\"}\n",
    "                 ),\n",
    "    dcc.Slider(id=\"slct_week\",\n",
    "              step=None\n",
    "              ),\n",
    "    html.Hr(),\n",
    "\n",
    "    html.Div(id='display-selected-values'),\n",
    "\n",
    "    html.Div(id='output_container', children=[]),\n",
    "    html.Br(),\n",
    "\n",
    "    dcc.Graph(id='my_bee_map', figure={})\n",
    "\n",
    "])\n",
    "\n",
    "# take the selected year to build the slider info (weeks) \n",
    "@app.callback(\n",
    "    Output('slct_week', 'marks'),\n",
    "    Output('slct_week', 'min'),\n",
    "    Output('slct_week', 'max'),\n",
    "    Output('slct_week', 'value'),\n",
    "    Input('slct_year', 'value'))\n",
    "def set_week_options(selected_year):\n",
    "    week = data[data['year']==selected_year]['week_year'].value_counts().keys().sort_values(ascending=True)\n",
    "    string = list(map(str, week)) \n",
    "    dictionary = dict(zip(week, string))\n",
    "    return dictionary, week[0], week[-1], week[0]\n",
    "\n",
    "@app.callback(\n",
    "    Output('display-selected-values', 'children'),\n",
    "    Input('slct_year', 'value'),\n",
    "    Input('slct_week', 'value'))\n",
    "def set_display_children(selected_year, selected_week):\n",
    "    return u'{} week in {}'.format(selected_week, selected_year,)\n",
    "\n",
    "\n",
    "\n",
    "# ------------------------------------------------------------------------------\n",
    "# Connect the Plotly graphs with Dash Components\n",
    "@app.callback(\n",
    "    [Output(component_id='output_container', component_property='children'),\n",
    "     Output(component_id='my_bee_map', component_property='figure')],\n",
    "    [Input(component_id='slct_year', component_property='value'),\n",
    "    Input(component_id='slct_week', component_property='value')]\n",
    ")\n",
    " \n",
    "\n",
    "def update_graph(option_slctd, week_slctd):\n",
    "    \n",
    "    container = \"The year chosen by user was: {}\".format(option_slctd)\n",
    "    df = data.copy()\n",
    "    df = df[(df[\"year\"] == option_slctd) & (df[\"week_year\"] == week_slctd)]\n",
    "\n",
    "    # Plotly Express\n",
    "    fig = go.Figure(go.Densitymapbox(lat=df.lat, \n",
    "                                     lon=df.long, \n",
    "                                     z=df.tempC,\n",
    "                                     radius=10))\n",
    "   \n",
    "    fig.update_layout(mapbox_style=\"stamen-terrain\", mapbox_center_lon=180)\n",
    "    fig.update_layout(margin={\"r\":0,\"t\":0,\"l\":0,\"b\":0})\n",
    "    \n",
    "    \n",
    "\n",
    "    return container, fig\n",
    "\n",
    "# ------------------------------------------------------------------------------\n",
    "if __name__ == '__main__':\n",
    "    app.run_server(debug=True, use_reloader=False)"
   ]
  },
  
   
