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
        ],value = 'SP1'

    ),
    dcc.Dropdown(
        id='value-dropdown',
        options=[
            {'label': 'Bz', 'value': 'Bz_Meas'},
            {'label': 'By', 'value': 'By_Meas'},
            {'label': 'Bx', 'value': 'Bx_Meas'},
            {'label': 'Br', 'value': 'Br'},
            {'label': 'Bphi', 'value': 'Bphi'}
        ], value = 'Bz_Meas'
    ),

        html.Div([
        html.Div([
            html.H3('Plot of Expected and Measured Field'),
            dcc.Graph(id='display-expected-values')
        ], className="six columns"),
        # html.Div([
        #     html.H3('Plot of Measured Values'),
        #     dcc.Graph(id='display-measured-values') ],
        #  className="six columns"),
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
        ], value = 'SP1'
     ),
        html.Div([
        html.Div([
            html.H3('Histogram of Bz'),
            dcc.Graph(id='histogram-of-bz')
        ], className="six columns"),
        html.Div([
                html.H3('Histogram of Br'),
                dcc.Graph(id='histogram-of-br')],
                className="six columns"),], ),
        html.Div([
        html.Div([
                html.H3('Histogram of Bx'),
                dcc.Graph(id='histogram-of-bx')],
                className="six columns"),
        html.Div([
                html.H3('Histogram of By'),
                dcc.Graph(id='histogram-of-by')],
                className="six columns"),], ),
        html.Div([
        html.Div([
                html.H3('Histogram of B_NMR'),
                dcc.Graph(id='histogram-of-bnmr')],
                className="six columns"),])


    ])

#Callback for expected values
@app.callback(
    Output('display-expected-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'), Input('interval-component', 'n_intervals')])
def update_output1(input_probe, input_value, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")

    hall_probe = input_probe
    field_value = input_value
    measured_field = df_raw[f'HP_{hall_probe}_{field_value}']
    measured_field = measured_field.astype(np.float)
    numb = len(measured_field)
    expected_field = df_expected[f'HP_{hall_probe}_{field_value}'][:numb]
    expected_field = expected_field.astype(np.float)

    fig1 = px.scatter(df_raw, x= 'TIMESTAMP', y = [expected_field, measured_field])
    #fig1.update_traces(marker=dict(color='purple'))
    fig1.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    return  fig1

#Callback for measured values
# @app.callback(
#     Output('display-measured-values', 'figure'),
#     [Input('probe-dropdown', 'value'),
#      Input('value-dropdown', 'value'),
#      Input('interval-component', 'n_intervals')])
# def update_output1(input_probe, input_value, n_intervals):
#     df_raw = load_data("liveupdates.pkl")
#
#     hall_probe = input_probe
#     field_value = input_value
#
#     fig2 = px.scatter(df_raw, x='TIMESTAMP', y=f'HP_{hall_probe}_{field_value}')
#     fig2.update_traces(marker=dict(color='orange'))
#     fig2.update_xaxes(
#         tickangle=60,
#         title_text="Time",
#         title_font={"size": 20},
#         title_standoff=25)
#     return fig2

#Callback for delta
@app.callback(
    Output('display-delta-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(input_probe, input_value, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")


    hall_probe = input_probe
    field_value = input_value
    measured = df_raw[f'HP_{hall_probe}_{field_value}']
    measured = measured.astype(np.float)
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_{field_value}'][: numb]
    expected = expected.astype(np.float)
    delta = measured - expected

    fig3 = px.line(df_raw, x='TIMESTAMP', y= delta)
    fig3.update_traces(marker=dict(color='yellow'))
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

##Histogram of Bz
@app.callback(
    Output('histogram-of-bz', 'figure'),
    [Input('probe-dropdown2', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")

    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_Bz_Meas']
    measured = measured.astype(np.float)
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_Bz_Meas'][: numb]
    expected = expected.astype(np.float)
    delta = measured - expected

    fig4 = px.histogram(df_raw, x= delta)
    fig4.update_traces(marker=dict(color='red'))
    fig4.update_xaxes(
        tickangle=60,
        title_text="Delta Bz",
        title_font={"size": 20},
        title_standoff=25)
    fig4.update_yaxes(
        title_text=f"Count",
        title_font={"size": 20},
        title_standoff=25)
    return fig4

##Histogram of Br
@app.callback(
    Output('histogram-of-br', 'figure'),
    [Input('probe-dropdown2', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")

    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_Br']
    measured = measured.astype(float)
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_Br'][:numb]
    expected = expected.astype(float)
    delta = measured - expected

    fig5 = px.histogram(df_raw, x= delta)
    fig5.update_traces(marker=dict(color='blue'))
    fig5.update_xaxes(
        tickangle=60,
        title_text="Delta Br",
        title_font={"size": 20},
        title_standoff=25)
    fig5.update_yaxes(
        title_text= "Count",
        title_font={"size": 20},
        title_standoff=25)
    return fig5
##Histogram of Bx
@app.callback(
    Output('histogram-of-bx', 'figure'),
    [Input('probe-dropdown2', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")

    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_Bx_Meas']
    measured = measured.astype(float)
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_Bx_Meas'][:numb]
    expected = expected.astype(float)
    delta = measured - expected

    fig6 = px.histogram(df_raw, x= delta)
    fig6.update_traces(marker=dict(color='green'))
    fig6.update_xaxes(
        tickangle=60,
        title_text="Delta Bx",
        title_font={"size": 20},
        title_standoff=25)
    fig6.update_yaxes(
        title_text= "Count",
        title_font={"size": 20},
        title_standoff=25)
    return fig6

##Histogram of By
@app.callback(
        Output('histogram-of-by', 'figure'),
        [Input('probe-dropdown2', 'value'),
         Input('interval-component', 'n_intervals')])
def update_output1(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")


    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_By_Meas']
    measured = measured.astype(np.float)
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_By_Meas'][: numb]
    expected = expected.astype(np.float)
    delta = measured - expected

    fig7 = px.histogram(df_raw, x=delta)
    fig7.update_traces(marker=dict(color='purple'))
    fig7.update_xaxes(
        tickangle=60,
        title_text="Delta By",
        title_font={"size": 20},
        title_standoff=25)
    fig7.update_yaxes(
        title_text=f"Count",
        title_font={"size": 20},
        title_standoff=25)
    return fig7

#Histogram of B_NMR
@app.callback(Output('histogram-of-bnmr', 'figure'),
        [Input('probe-dropdown2', 'value'),
         Input('interval-component', 'n_intervals')])
def update_output1(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")

    hall_probe = input_probe
    measured = df_raw['B_NMR']
    measured = measured.astype(np.float)
    numb = len(measured)
    expected = df_expected['B_NMR'][:numb]
    expected = expected.astype(np.float)
    delta = measured - expected

    fig7 = px.histogram(df_raw, x= delta)
    fig7.update_traces(marker=dict(color='brown'))
    fig7.update_xaxes(
        tickangle=60,
        title_text="Delta B_NMR",
        title_font={"size": 20},
        title_standoff=25)
    fig7.update_yaxes(
        title_text=f"Count",
        title_font={"size": 20},
        title_standoff=25)
    return fig7

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8030)