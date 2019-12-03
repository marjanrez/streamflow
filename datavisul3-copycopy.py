import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]
server= app.server
app.title = 'Streamflow Visualization'

# API and datasets
mapbox_access_token = "pk.eyJ1IjoiYWJ5Ym9yZGkiLCJhIjoiY2szcDd4d2U0MDBkaTNubXlhdnlsbzBzZyJ9.KzuRgoQvagYtHr4LqGswfQ"
df= pd.read_csv('/Users/arezoobybordi/Desktop/newStream.csv')


# bootstrap css
#app.css.append_css({'external_url': }) not needed

#Layouts
# Map Layouts

layout_map = dict(
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


#data

data = [ dict(
        type = 'scattermapbox',

        lon = df['LNG_GAGE'],
        lat = df['LAT_GAGE'],


        mode = 'markers',
        marker = dict(
            size = 80,
            opacity = 10,
            reversescale = True,
            autocolorscale = False,
            symbol = 'square',
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),


            color = df['Dryest Day'],
            cmin=0, 
            cmax = df['Dryest Day'].max(),
            colorbar=dict(
               title="Dryest Day"
                    )





        ))]



fig = dict( data=data, layout=layout_map )
app.layout=html.Div([
              html.Div([
                html.H1(children='Map',
                        className='twelve columns')
                ], className= 'row'
                            ),

            #map
              html.Div([

                        dcc.Graph(id= 'map-graph',
                                  animate=True,
                                  style={ 'margin-top' : '20'}
                                  , figure=fig)
                        ], className='twelve columns'


                        )




              ])





if __name__ == '__main__':
    app.run_server(debug=True)
