import dash
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
#import dash_bio as dashbio
from dash_html_components.Br import Br
from dash_html_components.Div import Div
from dash_html_components.Hr import Hr
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_table
from dash.exceptions import PreventUpdate

# get relative data folder

def getOutputCSV(fileName = "output.csv"):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../").resolve()
    dfg = pd.read_csv(DATA_PATH.joinpath(fileName))
    return dfg

output_data = getOutputCSV()

table_interact = dash_table.DataTable(
                            id='datatable-interactivity1',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
                                for i in output_data.columns
                            ],
                            data=output_data.to_dict('records'),  # the contents of the table
                            editable=False,              # allow editing of data inside all cells
                            filter_action="native",     # allow filtering of data by user ('native') or not ('none')
                            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
                            sort_mode="single",         # sort across 'multi' or 'single' columns
                            column_selectable="multi",  # allow users to select 'multi' or 'single' columns
                            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
                            row_deletable=False,         # choose if user can delete a row (True) or not (False)
                            selected_columns=[],        # ids of columns that user selects
                            selected_rows=[],           # indices of rows that user selects
                            page_action="native",       # all data is passed to the table up-front or not ('none')
                            page_current=0,             # page number that user is on
                            page_size=12,                # number of rows visible per page
                            style_cell={                # ensure adequate header width when text is shorter than cell's text
                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                            },
                            style_data={                # overflow cells' content into multiple lines
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_header={
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            }
                        )

#---------------------------------------------
layout = dbc.Container([
    html.H1('Output', style={"textAlign": "center"}),  #title

    dbc.Row([
            dbc.Col([
                #html.Button(id="view-button1", children="View results"),
                #html.Br(),
                #html.Br(),
                html.Div(table_interact, id= "output-csv"),
                
            ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],no_gutters=True, justify='around'),

    dbc.Row([
             dbc.Col([
                html.Br(),
                dbc.Button(id='btn-csv1',
                            children=[html.I(className="fa fa-download mr-1"), "Download to CSV"],
                            color="info",
                            className="mt-1"
                                    ),
                html.Br(),
                html.Br(),
                html.Button(id="submit-button-filter1", children="Create Graph"),
                dcc.Download(id="download-component-csv1"),

             ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],no_gutters=True, justify='around'),

    # For Graph
    dbc.Row([
             dbc.Col([
                html.Br(),
                html.Div(id='graph-container1'),
             ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],no_gutters=True, justify='around'),


    

    ], fluid=True)


#-----------------------------------------------------------------------
# for download button
@app.callback(
    Output("download-component-csv1", "data"),
    Input("btn-csv1", "n_clicks"),
    State('datatable-interactivity1', "derived_virtual_data"),
    prevent_initial_call=True,
)
def func(n_clicks,all_rows_data):
    dff = pd.DataFrame(all_rows_data)

    return dcc.send_data_frame(dff.to_csv, "output.csv")

#-----------------------------------
@app.callback(
    Output("graph-container1", "children"),
    Input("submit-button-filter1", "n_clicks"),
    State('datatable-interactivity1', "derived_virtual_data"),
    prevent_initial_call=True,
)
def func(n_clicks,all_rows_data):
    if n_clicks is None:
        return dash.no_update
    else:
        dff = pd.DataFrame(all_rows_data)
        dff['100-RF normalise'] = 100 - dff['RF normalise']
        #print(dff['Gene'].unique())

        graphs = []

        for gene in dff['Gene'].unique():
            dfg = dff[dff['Gene'] == gene]

            scatter_outpot = px.scatter(
                data_frame=dfg,
                x="Position ASM",
                y="Bootstrap moyen",
                size = "100-RF normalise",
                size_max=10,
                color = "Arbre phylogeographique",
                opacity = 0.5,
                hover_data=['Gene'],
                facet_col="Arbre phylogeographique",
                facet_col_wrap=2,
                title="phylogeographic analysis of {}".format(gene),
                
                #symbol = "Arbre phylogeographique",
                )
            graphs.append(dcc.Graph(figure=scatter_outpot))

        return graphs

#------------------------------------------------

