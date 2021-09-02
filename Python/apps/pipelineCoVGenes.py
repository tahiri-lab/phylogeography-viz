import dash
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_html_components.Br import Br
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import os
import base64
import datetime
import io
import pipeline_specific_genes

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# get all the newick files produced 
tree_path = os.listdir()
tree_files = []
for item in tree_path:
    if item.endswith("_newick"):
        tree_files.append(item)

#Study specific genes of SARS-CoV-2
genes_Cov = ['ORF1ab', 'S', 'ORF3a', 'ORF3b','E', 'M', 'ORF6', 'ORF7a','ORF7b','ORF8', 'N', 'ORF10']

#reference gene max length, for the validation of 'sliding window size' and 'step size'
ref_genes_len = {'ORF1ab': 21290, 'S':3825, 'ORF3a':828, 'ORF3b':456,'E':228, 'M':669, 'ORF6':9704, 
                    'ORF7a':366,'ORF7b':132,'ORF8':366, 'N':1260, 'ORF10':117}

layout = dbc.Container([
    html.H1('Phylogenetic Tree', style={"textAlign": "center"}),  #title
    
    # select genes
    dbc.Row([
            dbc.Col([
                html.Br(),
                html.H3("Study specific genes of SARS-CoV-2"),
                dcc.Checklist(id = 'genes_selected2',
                            options =[{'label': x, 'value': x} for x in genes_Cov],
                            value = [genes_Cov[0]],
                            labelStyle={'display': 'inline-block','marginRight':'20px'}),
                html.Br(),
                html.Hr(),
            ],# width={'size':3, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=10, xl=10
            ),
        ], no_gutters=True, justify='around'),

    
     dbc.Row([

        dbc.Col([
            html.Div([
                html.H3("Bootstrap value threshold"),
                dcc.Slider(id='BootstrapThreshold-slider2',
                            min=0,  
                            max=100,
                            step=0.1,
                            marks={
                                0: {'label':'0.0%','style': {'color': '#77b0b1'}},
                                25: {'label':'25.0%','style': {'color': '#77b0b1'}},
                                50: {'label':'50.0%','style': {'color': '#77b0b1'}},
                                75: {'label':'75.0%','style': {'color': '#77b0b1'}},
                                100: {'label':'100.0%','style': {'color': '#77b0b1'}}},
                            value=10),
                html.Div(id='BootstrapThreshold-slider-output-container2')        
            ]),
        ], #width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div([
                html.H3("Robinson and Foulds distance threshold"),
                dcc.Slider(id='RF-distanceThreshold-slider2',
                            min=0,
                            max=100,
                            step=0.1,
                            marks={
                                0: {'label':'0.0%', 'style': {'color': '#77b0b1'}},
                                25: {'label':'25.0%', 'style': {'color': '#77b0b1'}},
                                50: {'label':'50.0%', 'style': {'color': '#77b0b1'}},
                                75: {'label':'75.0%', 'style': {'color': '#77b0b1'}},
                                100: {'label':'100.0%','style': {'color': '#77b0b1'}}},
                            value=10),
                html.Div(id='RFThreshold-slider-output-container2'),       
            ]),
            ], #width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
            ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around
    
    dbc.Row([

        dbc.Col([
            html.Div(id='output-fasta2'),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around 
    
    # for sliding window siza & step size 
    dbc.Row([

        dbc.Col([
            html.Div([
                html.H3("Sliding Window Size"),
                dcc.Input(id = "input_windowSize2", type = "number", min = 0, max = max(ref_genes_len.values())-1,
                    placeholder = "Enter Sliding Window Size", value = 0,
                    style= {'width': '65%','marginRight':'20px'}),  
                html.Div(id='input_windowSize-container2'),    
                    ]),

        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div([
                html.H3("Step Size"),
                dcc.Input(id = "input_stepSize2", type = "number", min = 0, max = max(ref_genes_len.values())-1, 
                    placeholder = "Enter Step Size", value = 0,
                    style= {'width': '65%','marginRight':'20px'}), 
                html.Div(id='input_stepSize-container2'),    
                    ]),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ], no_gutters=True, justify='around'),  # Horizontal:start,center,end,between,around 


# select the files of reference tree
    dbc.Row([
            dbc.Col([
                html.Br(),
                html.Hr(),
                html.H3("Select the file(s) of reference trees"),
                dcc.Checklist(id = 'reference_trees2',
                            options =[{'label': x, 'value': x} for x in tree_files],
                            labelStyle={'display': 'inline-block','marginRight':'20px'}),
            ],# width={'size':3, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=10, xl=10
            ),
        ], no_gutters=True, justify='around'),

    #submit button
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Button(id="submit-button2", children="Submit"),
            html.Br(),
            html.Hr(),
        ],# width={'size':3, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=10, xl=10
        ),
    ], no_gutters=True, justify='around'),

    # for output of pipeline
    dbc.Row([
            dbc.Col([
                dcc.Interval(id='interval2', interval=1 * 1000, n_intervals=0,max_intervals=25*60*1000),
                html.Div(id='interval_container2'),
            ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],no_gutters=True, justify='around'),

    dbc.Row([
            dbc.Col([
                html.Div(id='output-container2'),
            ],xs=12, sm=12, md=12, lg=10, xl=10),

         ],no_gutters=True, justify='around'),
       

        

    

], fluid=True)



#-------------------------------------------------
# view the value chosen
@app.callback(
    dash.dependencies.Output('BootstrapThreshold-slider-output-container2', 'children'),
    [dash.dependencies.Input('BootstrapThreshold-slider2', 'value')])
def update_output(value):
    return 'You have selected {:0.1f}%'.format(value)

@app.callback(
    dash.dependencies.Output('RFThreshold-slider-output-container2', 'children'),
    [dash.dependencies.Input('RF-distanceThreshold-slider2', 'value')])
def update_output(value):
    return 'You have selected {:0.1f}%'.format(value)

@app.callback(
    dash.dependencies.Output('input_windowSize-container2', 'children'),
    [dash.dependencies.Input('input_stepSize2', 'value'),
    dash.dependencies.Input('genes_selected2', 'value')
    ])
def update_output(stepSize,genes):
    len_list = []
    for gen in genes:
        len_list.append(ref_genes_len.get(gen))
    min_len = min(len_list)
    if stepSize == None:
        value_max = min_len - 1
    else:
        value_max = min_len - 1 - stepSize
    return 'The input value must an integer from o to {}'.format(value_max)

@app.callback(
    dash.dependencies.Output('input_stepSize-container2', 'children'),
    [dash.dependencies.Input('input_windowSize2', 'value'),
    dash.dependencies.Input('genes_selected2', 'value')])
def update_output(windowSize,genes):
    len_list = []
    for gen in genes:
        len_list.append(ref_genes_len.get(gen))
    min_len = min(len_list)
    if windowSize == None:
        value_max = min_len - 1
    else:
        value_max = min_len - 1 - windowSize
    return 'The input value must be an integer from 0 to {}'.format(value_max)


#-------------------------------------------------
# run pipeline

@app.callback(
    Output('output-container2', 'children'),
    Input("submit-button2", "n_clicks"),
    State('BootstrapThreshold-slider2','value'),
    State('RF-distanceThreshold-slider2','value'),
    State('input_windowSize2','value'),
    State('input_stepSize2','value'),
    State('reference_trees2','value'),
    State('genes_selected2','value'),
    )

def update_output(n_clicks, bootstrap_threshold, rf_threshold, window_size, step_size, data_names,genes_chosen):
    if n_clicks is None:
        return dash.no_update
    else:
        reference_gene_file = 'output/reference_gene.fasta'
        pipeline_specific_genes.displayGenesOption(window_size, step_size, bootstrap_threshold, rf_threshold, data_names,genes_chosen)

        output_container =  dbc.Card([
            dbc.CardImg(src="/assets/trees-img.jpg", top=True),
            dbc.CardBody([
                html.H4("Done", className="card-title"),
                dcc.Markdown('bootstrap_thrshold :  **{}**'.format(bootstrap_threshold),className="card-text"),
                dcc.Markdown('rf_threshold :  **{}**'.format(rf_threshold),className="card-text"),
                dcc.Markdown('window_size :  **{}**'.format(window_size),className="card-text"),
                dcc.Markdown('step_size :  **{}**'.format(step_size),className="card-text"),
                dcc.Markdown('data_names :  {}'.format(data_names),className="card-text"),
                dcc.Markdown('genes_chosen :  {}'.format(genes_chosen),className="card-text"),
                
                dbc.CardLink("Check Results", href="checkResults"),
                #dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "60%"},       #50rem
),


        return output_container

# add a timer
@app.callback(
    Output('interval_container2', 'children'),
    Input("submit-button2", "n_clicks"),
    Input('interval2', 'n_intervals'),
    State('output-container2', 'children')
    )
def update_interval(n_clicks, n_intervals,output):
    if n_clicks is None:
        return dash.no_update
    else:
        if output == None:
            interval_container = html.Div([
                dcc.Markdown('Program is running **{}** s'.format(n_intervals))
            ])

            return interval_container
        else:
            return dash.no_update