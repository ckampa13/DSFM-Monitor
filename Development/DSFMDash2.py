import numpy as np
import pandas as pd
import pickle
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
from dash.dependencies import Input, Output


# Framework for DSFM monitoring system Dash #2 page 1 aka Field Plots

#for the soft link to data file
#scriptdir = os.path.dirname(os.path.realpath(__file__))
#datadir = os.path.join(scriptdir, '..', 'data/')
datadir = '/home/shared_data/FMS_Monitor/'

def load_data(filename):
    df_raw = pd.read_pickle(datadir + f"{filename}")
    return df_raw

#open datafile
df_raw = load_data("liveupdates.pkl")

#write data frame for field plot

probe_ids = ['SP1', 'SP2', 'SP3', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']
new_column_names = ['ID', 'X', 'Y', 'Z', 'Vx', 'Vy', 'Vz', 'Temperature',
                    'Bx_Meas', 'By_Meas', 'Bz_Meas'
                    ,'Br', 'Bphi' #, 'Bz',
                    ]
results_dict = {key: [] for key in new_column_names}
results_dict['TIMESTAMP'] = []

for probe in probe_ids:
    results_dict['TIMESTAMP'].append(df_raw['TIMESTAMP'].values)
    for col in new_column_names:
        results_dict[col].append(df_raw[f'HP_{probe}_{col}'].values)
for key in results_dict.keys():
    results_dict[key] = np.concatenate(results_dict[key])

df_Bfield = pd.DataFrame(results_dict)



# Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div(children=[html.Div([
        html.H1(children = 'DSFM Monitoring System')])]),
        dcc.Interval(
            id='interval-component',
            interval=5*1000,
            n_intervals = 0
        ),

        dcc.Dropdown(
        id='probe-dropdown',
        options=[
            {'label': 'Hall Probe 1 (SP1)', 'value': 'SP1'},
            {'label': 'Hall Probe 2 (SP2)', 'value': 'SP2'},
            {'label': 'Hall Probe 3 (SP3)', 'value': 'SP3'},
            {'label': 'Hall Probe 4 (BP1)', 'value': 'BP1'},
            {'label': 'Hall Probe 5 (BP2)', 'value': 'BP2'},
            {'label': 'Hall Probe 6 (BP3)', 'value': 'BP3'},
            {'label': 'Hall Probe 7 (BP4)', 'value': 'BP4'},
            {'label': 'Hall Probe 8 (BP5)', 'value': 'BP5'}
        ],

    ),
    dcc.Dropdown(
        id='value-dropdown',
        options=[
            {'label': 'Bz', 'value': 'Bz_Meas'},
            {'label': 'By', 'value': 'By_Meas'},
            {'label': 'Bx', 'value': 'Bx_Meas'},
            {'label': 'Br', 'value': 'Br'},
            {'label': 'Bphi', 'value': 'Bphi'}
        ],

    ),

        html.Div([
        html.Div([
            html.H3('Plot of Expected Field'),
            dcc.Graph(id='display-expected-values')
        ], className="six columns"),
        html.Div([
            html.H3('Plot of Measured Values'),
            dcc.Graph(id='display-measured-values') ],
         className="six columns"),
        html.Div([
                html.H3('Plot of Measured minus Expected Field'),
                dcc.Graph(id='display-delta-values')
            ], className="six columns"),
        ]),
        dcc.Dropdown(
        id='probe-dropdown2',
        options=[
            {'label': 'Hall Probe 1 (SP1)', 'value': 'SP1'},
            {'label': 'Hall Probe 2 (SP2)', 'value': 'SP2'},
            {'label': 'Hall Probe 3 (SP3)', 'value': 'SP3'},
            {'label': 'Hall Probe 4 (BP1)', 'value': 'BP1'},
            {'label': 'Hall Probe 5 (BP2)', 'value': 'BP2'},
            {'label': 'Hall Probe 6 (BP3)', 'value': 'BP3'},
            {'label': 'Hall Probe 7 (BP4)', 'value': 'BP4'},
            {'label': 'Hall Probe 8 (BP5)', 'value': 'BP5'}
        ] ),
        html.Div([
        html.Div([
            html.H3('Histogram of Bz'),
            dcc.Graph(id='histogram-of-bz')
        ], className="six columns"),
        html.Div([
                html.H3('Histogram of Br'),
                dcc.Graph(id='histogram-of-br')],
                className="six columns"),

        ]),
    ])

#Callback for expected values
@app.callback(
    Output('display-expected-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'), Input('interval-component', 'n_intervals')])
def update_output1(input_probe, input_value, n_intervals):
    df_raw = load_data("liveupdates.pkl")

    hall_probe = input_probe
    field_value = input_value

    fig1 = px.scatter(df_raw, x= 'TIMESTAMP', y = f'HP_{hall_probe}_{field_value}')
    fig1.update_traces(marker=dict(color='purple'))
    fig1.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    return  fig1

#Callback for measured values
@app.callback(
    Output('display-measured-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(input_probe, input_value, n_intervals):
    df_raw = load_data("liveupdates.pkl")

    hall_probe = input_probe
    field_value = input_value

    fig2 = px.scatter(df_raw, x='TIMESTAMP', y=f'HP_{hall_probe}_{field_value}')
    fig2.update_traces(marker=dict(color='purple'))
    fig2.update_xaxes(
        tickangle=60,
        title_text="Time",
        title_font={"size": 20},
        title_standoff=25)
    return fig2

#Callback for delta
@app.callback(
    Output('display-delta-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(input_probe, input_value, n_intervals):
    df_raw = load_data("liveupdates.pkl")

    hall_probe = input_probe
    field_value = input_value
    measured = df_raw[f'HP_{hall_probe}_{field_value}']
    expected = df_raw[f'HP_{hall_probe}_{field_value}']
    delta = float(measured) - float(expected)

    fig3 = px.line(df_raw, x='TIMESTAMP', y= delta)
    fig3.update_traces(marker=dict(color='purple'))
    fig3.update_xaxes(
        tickangle=60,
        title_text="Time",
        title_font={"size": 20},
        title_standoff=25)
    fig3.update_yaxes(
        title_text=f"Delta {field_value}",
        title_font={"size": 20},
        title_standoff=25)
    return fig3

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8030)