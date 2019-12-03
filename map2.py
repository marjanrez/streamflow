import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
from plotly import graph_objs as go
from plotly.graph_objs import *

df = pd.read_csv('https://raw.githubusercontent.com/osamaqureshi/streamflow/master/ca_rs.csv')
df1 = pd.read_csv('https://raw.githubusercontent.com/osamaqureshi/streamflow/master/dfirst100.csv')[['site_no','Date','X_00060_00003']]
df2 = pd.read_csv('https://raw.githubusercontent.com/osamaqureshi/streamflow/master/dash.csv')

df['text'] = df['STANAME'] + ', ' + df['DRAIN_SQKM'].astype(str)

app = dash.Dash()
scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]


locations = {}
for site in df2['site_no'].unique():
    lat = df2[df2['site_no']==site]['LAT_GAGE'].values[0]
    lon = df2[df2['site_no']==site]['LNG_GAGE'].values[0]
    locations[site] = {'lat':lat, 'lon':lon}

data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df['LNG_GAGE'],
        lat = df['LAT_GAGE'],
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            colorscale = scl,
            cmin = 0,
            color = df['DRAIN_SQKM'],
            cmax = df['DRAIN_SQKM'].max(),
            colorbar=dict(
                title="DRAIN_SQKM"
            )
        ))]

layout = dict(
        title = 'Stream Flow Locations',
        colorbar = True,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )

def compute_annual_flow(df,site_no):
    date = df['Date'].values

    df['Year'] = [x.split('-')[0] for x in date]
    df['Month'] = [x.split('-')[1] for x in date]
    df['Day'] = [x.split('-')[2] for x in date]

    temp = df[df['site_no'] == site_no]

    years = temp['Year'].unique()
    avg_flow = {}

    for year in temp['Year'].unique()[1:]: avg_flow[year] = 0

    for year in years[1:]:
        flow = temp[temp['Year']==year]['X_00060_00003'].mean()

        avg_flow[year] = flow

    return avg_flow

fig = dict( data=data, layout=layout )    


app.layout = html.Div([
    html.H2("STREAM FLOW"),
    html.P("""Select a location to display annual stream flow"""),  
    dcc.Dropdown(
        id='location-dropdown',
        options=[
            {"label": i, "value": i}
            for i in locations
        ],
        placeholder="Select a location",
        value = None
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(id='graph', figure=fig),
    dcc.Graph(id='flow-graph')  
])


@app.callback(
    Output('dd-output-container', 'children'),
    [Input('location-dropdown', 'value')])
def update_output(value):
    if value is not None:
        return '\nYou have selected "{}"'.format(value)

@app.callback(
    Output('flow-graph', 'figure'),
    [Input('location-dropdown', 'value')])
def update_figure(site):
    if site is None:
        site = 10256500
    avg_flow = compute_annual_flow(df1, site)
    x = list(avg_flow.keys())
    y = list(avg_flow.values())

    trace = [go.Scatter(x=x, y=y, mode='lines',
                                    marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, )]
    return {"data": trace,
            "layout": go.Layout(title="Annual Stream Flow", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Stream Flow ( cubic feet / sec )"}, xaxis={"title": "Year"})}



if __name__ == '__main__':
    app.run_server(debug=True)
