import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from itertools import cycle
from mapinterp import get_df_interp_func
import os
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

def load_Bfield(dataframe):
    df_raw = dataframe
    probe_ids = ['SP1', 'SP2', 'SP3', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']
    new_column_names = ['ID', 'X', 'Y', 'Z', 'Vx', 'Vy', 'Vz', 'Temperature',
                    'Bx_Meas', 'By_Meas', 'Bz_Meas'
                    ,'Br', 'Bphi', 'Bz' #, 'Bz',
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
    return df_Bfield




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
                    ,'Br', 'Bphi', #'Bz',
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

##Interpolated data
'''
Br_list = []
Bphi_list = []
Bz_list = []
for row in df_Bfield.itertuples():
    x = df_Bfield.X
    y = df_Bfield.Y
    z = df_Bfield.Z
    Br, Bphi, Bz = get_df_interp_func([x, y, z], df =df_Bfield, gauss =False) #Left off here with the interpolation!!
    Br_list.append(Br)
    Bphi_list.append(Bphi)
    Bz_list.append(Bz)

df_interpolated = pd.DataFrame({'X': df_Bfield.X,
                            'Y': df_Bfield.Y,
                            'Z': df_Bfield.Z,
                            'Br': Br_list,
                            'Bphi': Bphi_list,
                            'Bz': Bz_list})
'''
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
        ),  #html.Div([
   #html.I("Type the length of time into the past you would like to display data from:"),
    #dcc.Input(id="input1", type="number", placeholder="0", style={'marginRight':'10px'}),
    #,
       html.Div(
        [
            html.Div(
                [
                    html.H6("""Select the length of time""",
                            style={'margin-right': '2em'})
                ],

            ),
            dcc.Dropdown(
                 id='time-dropdown',
                options=[
            {'label': 'Last Two Minutes', 'value': '2'},
            {'label': 'Last Four Minutes', 'value': '4'},
            {'label': 'Last Six Minutes', 'value': '6'},
            {'label': 'Last Ten Minutes', 'value': '10'},
            {'label': 'Last Thirty Minutes', 'value': '30'},
            {'label': 'Last Hour', 'value': '60'},
            {'label': 'Last Two Hours', 'value': '120'},
            {'label': 'All Time', 'value': ''}
        ], value = '5',
                placeholder="Time Interval",
                style=dict(
                    width='40%',
                    verticalAlign="middle"
                )
            )
        ],
        style=dict(display='flex')
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
            {'label': 'Bz', 'value': 'Bz'},
            {'label': 'By', 'value': 'By_Meas'},
            {'label': 'Bx', 'value': 'Bx_Meas'},
            {'label': 'Br', 'value': 'Br'},
            {'label': 'Bphi', 'value': 'Bphi'}
        ], value = 'Bz'
    ),
    dcc.Dropdown(
        id='field-values-dropdown',
        options=[
            {'label': 'Bz', 'value': 'Bz'},
            {'label': 'Br', 'value': 'Br'},
            {'label': 'Bphi', 'value': 'Bphi'},
        ], value = 'Bz'
    ),

   # ]),

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

        #html.Div([
           #     html.H3('Interpolated'),
          #      dcc.Graph(id='display-contour-delta')
          #  ], className="six columns"),
        #dcc.Dropdown(
        #id='probe-dropdown2',
        #options=[
           # {'label': 'Hall Probe 1 (SP1)', 'value': 'SP1'},
            #{'label': 'Hall Probe 2 (SP2)', 'value': 'SP2'},
           # {'label': 'Hall Probe 3 (SP3)', 'value': 'SP3'},
           # {'label': 'Hall Probe 4 (BP1)', 'value': 'BP1'},
            #{'label': 'Hall Probe 5 (BP2)', 'value': 'BP2'},
           # {'label': 'Hall Probe 6 (BP3)', 'value': 'BP3'},
           # {'label': 'Hall Probe 7 (BP4)', 'value': 'BP4'},
           # {'label': 'Hall Probe 8 (BP5)', 'value': 'BP5'}
       # ], value = 'SP1'
    # ),
        html.Div([
        html.Div([
            html.H3('Histogram of Bz'),
            dcc.Graph(id='histogram-of-bz')
        ], className="six columns"),
        html.Div([
                html.H3('Histogram of Br'),
                dcc.Graph(id='histogram-of-br')],
                className="six columns"),], className = "row", ),
        html.Div([
        html.Div([
                html.H3('Histogram of Bx'),
                dcc.Graph(id='histogram-of-bx')],
                className="six columns"),
        html.Div([
                html.H3('Histogram of By'),
                dcc.Graph(id='histogram-of-by')],
                className="six columns"),], className = "row", ),
        html.Div([
        html.Div([
                html.H3('Histogram of B_NMR'),
                dcc.Graph(id='histogram-of-bnmr')],
                className="six columns"),],className = "row",),


        html.Div([
        html.Div([
               html.H3('Plot of Expected 3D Contour'),
                dcc.Graph(id='display-contour')
            ], className="six columns"),
        html.Div([
               html.H3('Plot of 2D Contour Measured Values'),
            dcc.Graph(id='display-contour2D')
            ], className="six columns"),], className = "row",),



    ])

#Callback for expected values
@app.callback(
    Output('display-expected-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'), Input('interval-component', 'n_intervals'), Input('time-dropdown', 'value')]) #Input('time-dropdown', 'value')])
def update_output1(input_probe, input_value, n_intervals, time):
    #return {'layout': go.Layout(height=700)}
    minutes = int(time)
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    # now = datetime.now()
    now = df_raw['TIMESTAMP'].iloc[-1]
    min_time = now - timedelta(minutes)
    df_time = df_raw.query(f'TIMESTAMP > "{min_time}"')
    df_time['B_error'] = 1e-4

    #time = -1*int(time)  #Throwing a NoneType error with the time variable--fix!
    hall_probe = input_probe
    field_value = input_value

    measured_field = df_time[f'HP_{hall_probe}_{field_value}']
    measured_field = measured_field.astype(np.float)
    #numb = len(measured_field)
    number = len(measured_field)
    #z_value = df_time['Z'][0]
    #time0 = df_time[0]
    #time1 = df_time[-1]
    #df_expected_time = df_expected.query(f'Z >= "{z_value}"')    #df_expected.query(f'"{time0}" <= TIMESTAMP <= "{time1}"')

    expected_field = df_expected[f'HP_{hall_probe}_{field_value}'][:number]   #[:number]  #[:numb]

    #expected_field = expected_field.astype(np.float)

    timestamp = df_expected['TIMESTAMP'][:number]

    fig1 = px.line(df_expected, x= timestamp, y = expected_field)
    fig1.update_traces(marker=dict(
        color='red'))
    fig2 = px.scatter(df_time, x='TIMESTAMP', y = measured_field, error_y = 'B_error')
    fig2.update_traces(marker=dict(
        color='black'))
    #fig3 = go.Figure(data = fig1.data + fig2.data)
    scatter = go.Scatter(
        x=df_time['TIMESTAMP'],
        y=measured_field,
        mode = 'markers',
        error_y=
        dict(
            type='constant',  # value of error bar given as percentage of y value
            value= 1e-4,
            visible=True))
    line = go.Line(x= df_expected['TIMESTAMP'][:number],y=expected_field, mode= 'lines+markers')
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(scatter)
    fig3.add_trace(line, secondary_y=True)
    #fig1.update_traces(marker=dict(color='purple'))
    fig3.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    fig3.update_yaxes(
        tickangle=60,
        title_text=f"{field_value}",
        title_font={"size": 20},
        title_standoff=25)
    names = cycle(['Measured Value', 'Expected Value'])
    fig3.for_each_trace(lambda t: t.update(name=next(names)))
    fig3.update_layout(uirevision='constant')
    return  fig3

#Callback for delta
@app.callback(
    Output('display-delta-values', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output6(input_probe, input_value, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    field_value = input_value
    measured = df_raw[f'HP_{hall_probe}_{field_value}'].values
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_{field_value}'][:numb].values
    delta = measured - expected
    df_raw['delta'] = delta
    df_raw['B_error'] = 1e-4
    fig3 = px.scatter(df_raw, x='TIMESTAMP', y= 'delta', error_y = 'B_error')
    fig3.update_traces(marker=dict(color='orange'))
    fig3.update_xaxes(
        tickangle=60,
        title_text="Time",
        title_font={"size": 20},
        title_standoff=25)
    fig3.update_yaxes(
        title_text=f"Delta {field_value}",
        title_font={"size": 20},
        title_standoff=25)
    fig3.update_layout(uirevision='constant')
    return fig3
## 3D contour plot
@app.callback(
    Output('display-contour', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'),
     Input('interval-component', 'n_intervals'), Input('field-values-dropdown', 'value')])
def update_outputcontour2(input_probe, input_value, input_intervals, field):
    df = pd.read_pickle("/home/shared_data/Bmaps/Mu2e_DSMap_V13.p")
    field_value = field
    for coord in ['x', 'y', 'z', 'r', 'phi']:
        df.eval(f"B{coord} = B{coord} / 10000", inplace=True)
    df_plane = df.query('(Y==0.) & (R < 0.8) & (4. < Z < 14.)')
    Lz = len(df_plane['Z'].unique())
    Lx = len(df_plane['X'].unique())
    x = df_plane['Z'].values.reshape(Lx, Lz)
    y = df_plane['X'].values.reshape(Lx, Lz)
    z = df_plane[f'{field_value}'].values.reshape(Lx, Lz)
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis', colorbar=dict(title='Bz [T]'))])
    fig.update_layout(title=f'{field_value} vs. X,Z for Y==0', autosize=False,
                      width=500, height=500,
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Z [m]'),
            yaxis=dict(title='X [m]'),
            zaxis=dict(title='Bz [T]'),
            aspectratio=dict(x=2, y=1, z=1),
            aspectmode='manual',
        )
    )
    fig.update_layout(
        scene=dict(
            camera=dict(
                center=dict(x=0,
                            y=0,
                            z=-0.3),
                eye=dict(x=3.44 / 1.2,
                         y=-2.48 / 1.2,
                         z=1.58 / 1.2))
        )
    )

    '''
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    field_value = input_value
    expected = df_expected[f'HP_{hall_probe}_Bz']
    #expected_field = np.reshape(expected, (-1,2))
    expected_Z = df_expected[f'HP_{hall_probe}_Z']
    expected_X = df_expected[f'HP_{hall_probe}_X']
    expected_Y = df_expected[f'HP_{hall_probe}_Y']

    expected = expected.astype(np.float)
    fig = go.Figure(data = [go.Surface(x = expected_Z, y= expected_X, z=expected)])
    #fig = px.density_contour(df_expected, x = expected_Z, y=expected_X, z = expected_Bz)
    '''
    fig.update_layout(uirevision='constant')
    return fig

## 2D Contour plot of measured data
@app.callback(
    Output('display-contour2D', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('value-dropdown', 'value'),
     Input('interval-component', 'n_intervals'),Input('field-values-dropdown', 'value') ])

def update_outputcontour1(input_probe, input_value, input_intervals, field):
    original = load_data("liveupdates.pkl")
    hall_probe = input_probe
    field_value = input_value
    fieldB = field
    df  = load_Bfield(original)
    '''
    for coord in ['X', 'Y', 'Z', 'r', 'phi']:
        df.eval(f"B{coord} = B{coord} / 10000", inplace=True)
        '''
    df_plane = df.query('(Y==0.)  & (4. < Z < 14.)')
    #Lz = len(df_plane['Z'].unique())
    #Lx = len(df_plane['X'].unique())
    #if Lz % 2 == 0 and Lx % 2 == 0:
    x = df_plane['Z']    #.values.reshape(Lx, Lz)
    y = df_plane['X']    #.values.reshape(Lx, Lz)
    z = df_plane[f'{fieldB}']    #.values.reshape(Lx, Lz)
    fig = go.Figure(data=[go.Contour(z=z, x=x, y=y, colorscale='Viridis', colorbar=dict(title='Bz [T]'))])
    fig.update_layout(title=f'{fieldB} vs. X,Z for Y==0', autosize=False,
                      width=500, height=500,
                      margin=dict(l=65, r=50, b=65, t=90))
    #else:
        #dash.no_update
        #fig = go.Figure()
    '''
    expected = df_expected[f'HP_{hall_probe}_Bz']
    #expected_field = np.reshape(expected, (-1,2))
    expected_Z = df_expected[f'HP_{hall_probe}_Z']
    expected_X = df_expected[f'HP_{hall_probe}_X']
    expected_Y = df_expected[f'HP_{hall_probe}_Y']
    #X,Z = meshgrid(expected_X,expected_Z)

    expected = expected.astype(np.float)
    #fig = go.Figure(data = [go.Surface(x = expected_X, y= expected_Z, z=expected)])
    #data = [{ 'x' : X, 'y' :Z, 'z' : expected}]
    #fig = py.plot(data, filename ='liveupdates.pkl')
    fig = px.density_contour(df_expected, x = f'HP_{hall_probe}_Z', y = f'HP_{hall_probe}_X', z = f'HP_{hall_probe}_Bz')'''
    fig.update_layout(uirevision='constant')

    return fig



## 3D interpolation, minus - expected feild

#@app.callback(
    #Output('display-contour-delta', 'figure'),
    #[Input('probe-dropdown', 'value'),
     #Input('value-dropdown', 'value'),
     #Input('interval-component', 'n_intervals')])
#def update_outputcontour(input_probe, input_value, input_intervals):

    #return {'layout': go.Layout(height=700)}
    '''
    df = df_interpolated# pd.read_pickle("/home/shared_data/Bmaps/Mu2e_DSMap_V13.p")
    for coord in ['x', 'y', 'z', 'r', 'phi']:
        df.eval(f"B{coord} = B{coord} / 10000", inplace=True)
    df_plane = df.query('(Y==0.) & (R < 0.8) & (4. < Z < 14.)')
    Lz = len(df_plane['Z'].unique())
    Lx = len(df_plane['X'].unique())
    x = df_plane['Z'].values.reshape(Lx, Lz)
    y = df_plane['X'].values.reshape(Lx, Lz)
    z = df_plane['Bz'].values.reshape(Lx, Lz)
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Viridis', colorbar=dict(title='Bz [T]'))])
    fig.update_layout(title='Bz vs. X,Z for Y==0', autosize=False,
                      width=500, height=500,
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Z [m]'),
            yaxis=dict(title='X [m]'),
            zaxis=dict(title='Bz [Gauss]'),
            aspectratio=dict(x=2, y=1, z=1),
            aspectmode='manual',
        )
    )
    fig.update_layout(
        scene=dict(
            camera=dict(
                center=dict(x=0,
                            y=0,
                            z=-0.3),
                eye=dict(x=3.44 / 1.2,
                         y=-2.48 / 1.2,
                         z=1.58 / 1.2))
        )
    )'''




##Histogram of Bz
@app.callback(
    Output('histogram-of-bz', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output2(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_Bz_Meas'].values
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_Bz_Meas'][:numb].values
    delta = measured - expected
    #print(delta)
    df_raw['delta'] = delta

    fig4 = px.histogram(df_raw, x= 'delta', marginal = 'rug')
    fig4.update_traces(marker=dict(color='red'))
    #fig4.update_xaxes(
       # tickangle=60,
        #title_text="Delta Bz",
        #title_font={"size": 20},
        #title_standoff=25)
   # fig4.update_yaxes(
        #title_text=f"Count",
        #title_font={"size": 20},
        #title_standoff=25)
    fig4.update_traces(alignmentgroup=0, selector=dict(type='histogram'))
    fig4.update_layout(uirevision='constant')
    return fig4

##Histogram of Br
@app.callback(
    Output('histogram-of-br', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output3(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_Br'].values
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_Br'][:numb].values
    delta = measured - expected
    df_raw['delta'] = delta

    fig5 = px.histogram(df_raw, x= 'delta', marginal = 'rug')
    fig5.update_traces(marker=dict(color='blue'))
    #fig5.update_xaxes(
       # tickangle=60,
        #title_text="Delta Br",
       # title_font={"size": 20},
       # title_standoff=25)
    #fig5.update_yaxes(
       # title_text= "Count",
        #title_font={"size": 20},
        #title_standoff=25)
    fig5.update_traces(alignmentgroup=0, selector=dict(type='histogram'))
    fig5.update_layout(uirevision='constant')
    return fig5
##Histogram of Bx

@app.callback(
    Output('histogram-of-bx', 'figure'),
    [Input('probe-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output4(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_Bx_Meas'].values
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_Bx_Meas'][:numb].values
    expected = expected.astype(float)
    delta = measured - expected
    df_raw['delta'] = delta

    fig6 = px.histogram(df_raw, x= 'delta', marginal = 'rug')
    fig6.update_traces(marker=dict(color='green'))
    #fig6.update_xaxes(
       # tickangle=60,
        #title_text="Delta Bx",
        #title_font={"size": 20},
        #title_standoff=25)
    #fig6.update_yaxes(
        #title_text= "Count",
        #title_font={"size": 20},
        #title_standoff=25)
    fig6.update_traces(alignmentgroup=0, selector=dict(type='histogram'))
    fig6.update_layout(uirevision='constant')
    return fig6

##Histogram of By
@app.callback(
        Output('histogram-of-by', 'figure'),
        [Input('probe-dropdown', 'value'),
         Input('interval-component', 'n_intervals')])
def update_output5(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    measured = df_raw[f'HP_{hall_probe}_By_Meas'].values
    numb = len(measured)
    expected = df_expected[f'HP_{hall_probe}_By_Meas'][:numb].values
    delta = measured - expected
    df_raw['delta'] = delta
    fig7 = px.histogram(df_raw, x='delta', marginal = 'rug')
    fig7.update_traces(marker=dict(color='purple'))
    #fig7.update_xaxes(
       # tickangle=60,
        #title_text="Delta By",
        #title_font={"size": 20},
        #title_standoff=25)
    #fig7.update_yaxes(
        #title_text=f"Count",
        #title_font={"size": 20},
        #title_standoff=25)
    fig7.update_traces(alignmentgroup=0, selector=dict(type='histogram'))
    fig7.update_layout(uirevision='constant')
    return fig7

#Histogram of B_NMR
@app.callback(Output('histogram-of-bnmr', 'figure'),
        [Input('probe-dropdown', 'value'),
         Input('interval-component', 'n_intervals')])
def update_output6(input_probe, n_intervals):
    df_raw = load_data("liveupdates.pkl")
    df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
    hall_probe = input_probe
    measured = df_raw['B_NMR'].values
    measured = measured.astype(np.float)
    numb = len(measured)
    expected = df_expected['B_NMR'][:numb].values
    delta = measured - expected
    df_raw['delta'] = delta
    fig8 = px.histogram(df_raw, x= 'delta', marginal = 'rug')
    fig8.update_traces(marker=dict(color='brown'))
    #fig8.update_xaxes(
        #tickangle=60,
        #title_text="Delta B_NMR", #change to mathmatical symbols + units
        #title_font={"size": 20},
        #title_standoff=25)
    #fig8.update_yaxes(
        #title_text=f"Count",
        #title_font={"size": 20},
        #title_standoff=25)
    fig8.update_traces(alignmentgroup=0, selector=dict(type='histogram'))
    fig8.update_layout(uirevision='constant')
    return fig8

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug= True, port=8030)