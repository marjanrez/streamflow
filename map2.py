import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/osamaqureshi/streamflow/master/ca_rs.csv')
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


fig = dict( data=data, layout=layout )    

app.layout  = html.Div([
    html.H2("STREAM FLOW"),
    html.P("""Select a location to display annual stream flow"""),
    html.Div(
        className="div-for-dropdown",
        children=[
            dcc.Dropdown(
                id="location-dropdown",
                options=[
                    {"label": i, "value": i}
                    for i in locations
                ],
                placeholder="Select a location",
            )
        ],
    ),
    dcc.Graph(id='graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)