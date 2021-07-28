import dash  # use Dash version 1.16.0 or higher for this app to work
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# data



# latout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id = 'selectVirus', value='Measles',multi=False,
            options=[
                {'label':'avian','value':'avian'},
                {'label':'dengue','value':'dendue'},
                {'label':'ebola','value':'ebola'},
                {'label':'flu','value':'flu'},
                {'label':'lassa','value':'measles'},
                {'label':'mumps','value':'mumps'},
                {'label':'measles','value':'measles'},
                {'label':'zika','value':'zika'}
            ],className='six columns'),
        dcc.RangeSlider(
            id='yearRange',
            min=1977,
            max=2016,
            value=[1977,2016],
            step=None,
            marks={
                1977:'1977',
                1982:'1982',
                1987:'1987',
                1992:'1992',
                1997:'1997',
                2002:'2002',
                2007:'2007',
                2012:'2012',
                2016:'2016'
         }, className='six columns')
    ]),
    html.Div([
        dcc.Graph(id='virusNumber-graph', figure={}, className='six columns'),
        dcc.Graph(id='tree-graph', figure={}, className='six columns')
    ]),
    html.Div([
        dcc.Graph(id='map-graph', figure={}, className='six columns'),
        dcc.Graph(id='distribution-graph', figure={}, className='six columns')

    ])
])

'''
#callback
@app.callback(
    Output(component_id='virusNumber-graph', component_property='figure'),
    Input(component_id='selectVirus', component_property='value'),
    Input(component_id='yearRange', component_property='value'),
    prevent_initial_call=False
)
def update_graph(cccc):
    dff = df[df.country.isin(ccc)]
    fig = px.line(data_frame=dff, x= , y= )
    return fig
    
'''

if __name__ == '__main__':
    app.run_server(debug=True)