import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
from plotly import graph_objs as go
from plotly.graph_objs import *

df = pd.read_csv('https://raw.githubusercontent.com/osamaqureshi/streamflow/master/newStream.csv')
df1 = pd.read_csv('all80.csv')[['site_no','Date','Streamflow']]
mapbox_access_token = "pk.eyJ1IjoiYWJ5Ym9yZGkiLCJhIjoiY2szcDd4d2U0MDBkaTNubXlhdnlsbzBzZyJ9.KzuRgoQvagYtHr4LqGswfQ"

app = dash.Dash()
app.title = 'Streamflow Visualization'
scl = [[0.0, "rgb(220, 220, 220)"],
                [0.25, "rgb(0,128,0)"],
                [0.5, "rgb(255,255,0)"],
                [0.75, "rgb(255,69,0)"],
                [1.0, "rgb(220,220,220)"]]

df2 = []
locations = {}
for site in df['site_no'].unique():
    lat = df[df['site_no']==site]['LAT_GAGE'].values[0]
    lon = df[df['site_no']==site]['LNG_GAGE'].values[0]
    locations[site] = {'lat':lat, 'lon':lon}
    df2 += [[site,lat,lon]]
df2 = pd.DataFrame(df2, columns = ['site_no','lat','lon'])
graphs = {'Line graph':'Line graph','Bar Chart':'Bar Chart'}

layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Streamflow',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-119.8646,
            lat=37.1138
        ),
        zoom=5,
    )
)

data = [ dict(
        type = 'scattermapbox',
        lon = df2['lon'],
        lat = df2['lat'],
        text = df2['site_no'],
        mode = 'markers',
        opacity=0.7,
        marker = dict(
            size = 10,
            line = {'width': 0.5, 'color': 'rgba(102, 102, 102)'},
            colorscale = scl,
            cmin = 0,
            color = df['Dryest Day'],
            cmax = df['Dryest Day'].max(),
            colorbar=dict(
                title="Dryest Day"
                ))
        )
]

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
        flow = temp[temp['Year']==year]['Streamflow'].mean()

        avg_flow[year] = flow

    return avg_flow

def plot_graph(site,click,graph):
    avg_flow = compute_annual_flow(df1, site)
    x = list(avg_flow.keys())
    y = list(avg_flow.values())

    if graph == 'Line graph':
        trace = [go.Scatter(x=x, y=y, mode='lines',
                                    marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, )]
    elif graph == 'Bar Chart':
        trace = [go.Bar(x=x, y=y)]
    return {"data": trace,
            "layout": go.Layout(title="Annual Stream Flow", colorway=['#abd9e9', '#2c7bb6'],
                                yaxis={"title": "Stream Flow ( cubic feet / sec )"}, xaxis={"title": "Year"})}


fig = dict( data=data, layout=layout)    

app.layout = html.Div([
    html.H2("STREAM FLOW"),
    html.P("""Select a location to display annual stream flow"""),  
    dcc.Dropdown(
        id='location-dropdown',
        options=[
            {"label": i, "value": i}
            for i in locations
        ],
        placeholder="Select a Location",
        value = None
    ),
    dcc.Dropdown(
        id='graph-dropdown',
        options=[
            {"label": i, "value": i}
            for i in graphs
        ],
        placeholder="Select a Graph",
        value = None
    ),
    html.Div([
        dcc.Graph(id= 'map-graph',
            animate=True,
            style={ 'margin-top' : '20'},
            figure=fig)]
    ),
    dcc.Graph(id='flow-graph')
])


@app.callback(
    Output('flow-graph', 'figure'),
    [Input('location-dropdown', 'value'),Input('map-graph', 'clickData'),Input('graph-dropdown', 'value')])
def update_figure(site,click,graph):
    if click is None:
        site = 10256500
    else:
        site = int(click['points'][0]['text'])

    if graph is None:
        graph = 'Line graph'
    return plot_graph(site,click,graph)

if __name__ == '__main__':
    app.run_server(debug=True)