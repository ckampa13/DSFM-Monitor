import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import os
import dash_table
import plotly.express as px
from PIL import Image
from dash.dependencies import Input, Output

#opening the pickle file
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
pklfile_raw = 'liveupdates.pkl'
# pklfile_raw = 'IntegrationTests/liveupdates.pkl'

# datadir = '/home/shared_data/FMS_Monitor/'
#df_raw = pd.read_pickle(datadir + "liveupdates.pkl")

def load_data(filename):
    df_raw = pd.read_pickle(datadir + f"{filename}")
    return df_raw
df_raw = load_data(pklfile_raw)

#formatting new dataframes

df_NMR = df_raw[['TIMESTAMP', 'B_NMR']].copy()  #'X_NMR', 'Y_NMR', 'Z_NMR',
hall_probe_cols = []

for name in df_raw.columns:
    if "HP_" in name:
        hall_probe_cols.append(name)
df_Hall = df_raw[['TIMESTAMP']+ hall_probe_cols]

#print(df_Hall)


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
#print("this is B_field dataframe", df_Bfield)
def load_FMS_df(df_raw):
    columns_in_FMS = [ 'Probe_Name', 'Vx', 'Vy', 'Vz', 'Br', 'Bphi', 'Bz_Meas', 'Temperature', 'X', 'Y', 'Z']

    fms_dict = {key: [] for key in columns_in_FMS}
    for probe in probe_ids:
        fms_dict['Probe_Name'].append(probe)
        for col in columns_in_FMS:
            if col == 'Probe_Name':
               pass
            else:
                name = f'HP_{probe}_{col}'
                x = df_raw[f'HP_{probe}_{col}'].iloc[-1]
                # if 'Temperature' in name:
                #     x  = x.astype(np.float)
                #     y = round(x, 2)
                #     fms_dict[col].append(y)
                # if 'Br' or 'Bphi' or 'Bz_Meas' in name:
                #     x = x.astype(np.float)
                #     y = '{:.3e}'.format(x)
                #     fms_dict[col].append(y)
                if 'Temperature' in name:
                    x = x.round(1)
                if 'Br' or 'Bz' or 'Bphi' in name:
                    x = x.round(4)
                fms_dict[col].append(x)
# for key in fms_dict.keys():
#     fms_dict[key] = np.concatenate(fms_dict[key])

    df_FMS = pd.DataFrame(fms_dict)
    return df_FMS
#print(df_FMS)
df_FMS = load_FMS_df(df_raw)

def load_magnet_df(df_raw):
    columns_in_df = ['B_NMR', 'PS_Current', 'TS_Current', "DS_Current"]
    magnet_dict = {key: [] for key in columns_in_df}
    for col in columns_in_df:
        x = df_raw[col].iloc[-1]
        magnet_dict[col].append(x)
    df_magnet = pd.DataFrame(magnet_dict)
    return df_magnet

df_magnet = load_magnet_df(df_raw)

df_dict = {'raw': df_raw, 'NMR': df_NMR, 'Hall Probes': df_Hall, 'Field at Location': df_Bfield, 'State of FMS': df_FMS, 'Currents': df_magnet}

####Images
image_filename = datadir + 'DSFMimage1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

probes = datadir + 'DSFM-Sketch.png'
encoded_probes = base64.b64encode(open(probes, 'rb').read())

z_loc = 400
df_FMS.to_dict('records')
# datadir2 = r'/home/shared_data/FMS_Monitor/'
datadir2 = datadir
#load images
img_coil = Image.open(datadir2 + 'coils.png')
img_mapper = Image.open(datadir2 + 'DSFM_YZ_sketch.png')
img_xy = Image.open(datadir2 + 'X-Y coords.png')
img_prop = Image.open(datadir2 + 'Reflector Map Sketch New.png')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
stylesheet_href= ["https://s3-us-west-2.amazonaws.com/colors-css/2.2.0/colors.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
        html.Div(children=[html.Div([
        html.H1(children = 'State of the FMS')])]),
        dcc.Interval(
            id='interval-component',
            interval=4*1000,
            n_intervals = 0
        ),
        html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_probes.decode()), style={'height':'80%'} )], className="four columns"),
        html.Div([  # html.H3(children = 'Hall Probe Status Datatable'),
        dash_table.DataTable(
            id='table-magnet',
            # data= data,
            columns=[{"name": i, "id": i, "type": 'numeric'} for i in df_magnet.columns],
            sort_action='native',
            editable=True,
            style_data_conditional= [
                {
                    'if' : {
                        'column_id': 'B_NMR'
                    }, 'backgroundColor': 'green',
                        'color' : 'white'
                    },
{
                    'if' : {
                        'column_id': 'Probe_Name'
                    }, 'backgroundColor': 'green',
                        'color' : 'white'
                    },
{
                    'if' : {
                        'column_id': 'PS_Current'
                    }, 'backgroundColor': 'green',
                        'color' : 'white'
                    },
{
                    'if' : {
                        'column_id': 'DS_Current'
                    }, 'backgroundColor': 'green',
                        'color' : 'white'
                    },
{
                    'if' : {
                        'column_id': 'TS_Current'
                    }, 'backgroundColor': 'green',
                        'color' : 'white'
                    }

            ]




            ) ]),


        html.Div([     #html.H3(children = 'Hall Probe Status Datatable'),
        dash_table.DataTable(
        id='table',
        #data= data,
        columns=[{"name": i, "id": i, "type": 'numeric'} for i in df_FMS.columns],
        sort_action='native',
        editable=True,
        style_data_conditional=[
             {
                 'if': {
                     'column_id': 'Probe_Name',
                     'filter_query' : "{Probe_Name} eq 'SP1'",

                 },
                 'backgroundColor': 'green',
                 'color': 'white'
             },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'SP2'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'SP3'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'BP1'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'BP2'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'BP3'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'BP4'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            },
            {
                'if': {
                    'column_id': 'Probe_Name',
                    'filter_query': "{Probe_Name} eq 'BP5'",

                },
                'backgroundColor': 'green',
                'color': 'white'
            }
        ]

        ),]),


        html.Div([
        html.Div([
            html.H3('Mapper Z Location'),
            dcc.Graph(id='solenoid-mapper')
        ], className="six columns"),
        html.Div([
            html.H3('Mapper Angle'),
            dcc.Graph(id='mapper-angle')
        ], className="six columns"),]),


        dcc.Dropdown(
        id='demo-dropdown',
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
        value='SP1'
    ),



       html.Div([
        html.Div([
            html.H3('Bz [T]'),
            dcc.Graph(id='display-selected-values')
        ], className="six columns"),
        html.Div([
            html.H3('Br [T]'),
            dcc.Graph(id='display-selected-values2')
        ], className="six columns"), ], className="row"),
        html.Div([
            html.Div([
                html.H3('Bphi [T]'),
                dcc.Graph(id='display-selected-values3')
            ], className="six columns"),
            html.Div([
                html.H3('Temperature [C]'),
                dcc.Graph(id='display-selected-values4')
            ], className="six columns"), ],className = "row"),


])

#Callback 1 for plot Bxz_Meas
@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [Input('demo-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_output1(value, interval):

    df_raw = load_data(pklfile_raw)

    hall_probe = value

    fig1 = px.scatter(df_raw, x= 'TIMESTAMP', y = f'HP_{hall_probe}_Bz_Meas')
    fig1.update_traces(marker=dict(color='purple'))
    fig1.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    fig1.update_layout(uirevision='constant')
    return  fig1

# @app.callback(Output('display-selected-values', 'figure'),
#               [Input('interval-component', 'interval')])
# def update_graph_scatter():
#
#     return {'data': traces}


#Callback 2 for plot Br
@app.callback(
    dash.dependencies.Output('display-selected-values2', 'figure'),
    [Input('demo-dropdown', 'value'),
     Input('interval-component', 'n_intervals')])
def update_layout2(value, interval):
    df_raw = load_data(pklfile_raw)

    hall_probe = value

    fig2 = px.scatter(df_raw, x='TIMESTAMP', y = f'HP_{hall_probe}_Br')
    fig2.update_traces(marker=dict(color='maroon'))
    fig2.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    fig2.update_layout(uirevision='constant')
    return fig2

#Callback 3 for plot Bphi
@app.callback(
    dash.dependencies.Output('display-selected-values3', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'), dash.dependencies.Input('interval-component', 'n_intervals')])
def update_layout3(value, interval):
    df_raw = load_data(pklfile_raw)


    hall_probe = value

    fig3 = px.scatter(df_raw, x='TIMESTAMP', y=f'HP_{hall_probe}_Bphi')
    fig3.update_traces(marker=dict(color='lime'))
    fig3.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    fig3.update_layout(uirevision='constant')
    return fig3

#Callback 4 for plot temperature
@app.callback(
    dash.dependencies.Output('display-selected-values4', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'), dash.dependencies.Input('interval-component', 'n_intervals')])
def update_layout3(value, interval):
    df_raw = load_data(pklfile_raw)

    hall_probe = value
    fig4 = px.scatter(df_raw, x='TIMESTAMP', y= f'HP_{hall_probe}_Temperature')
    fig4.update_traces(marker=dict(color='orange'))
    fig4.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
    fig4.update_layout(uirevision='constant')
    return fig4

#Callback 5 for Solenoid img----Come back to this when using live data
@app.callback(
    dash.dependencies.Output('solenoid-mapper', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_layout3(interval):
    # plot coils
    df_raw = load_data(pklfile_raw)
    #figimg = go.Figure()
    figimg = px.imshow(img_coil)
    #z_loc = df_raw['Mapper_Z'].iloc[-1].split('.')
    z_loc = (float(df_raw['Mapper_Z'].iloc[-1]) - 3.75)/(16 - 4)

    #z_loc_convert = '0.' + z_loc[0] + z_loc[1]
    # plot mapper towards tracker
    '''
    figimg.add_layout_image(dict(
        source=img_coil,
        x = 0.7,
        y = 0.3,
        sizex = 1,
        sizey = 1,
        sizing = 'fill'

    )
    )
    '''
    figimg.add_layout_image(dict(
        source=img_mapper,
        x=z_loc,
        y=0.35,
    )
    )
    figimg.update_layout_images(dict(
        xref='paper',
        yref='paper',
        sizex=0.3,
        sizey=0.3,
        xanchor='right',
        yanchor='bottom',
    ))
    figimg.update_layout(
        xaxis={'fixedrange': True},
        yaxis={'fixedrange': True}
    )
    figimg.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    figimg.update_layout(yaxis={'visible': False, 'showticklabels': False},
                        xaxis={'visible': False, 'showticklabels': False})

    figimg.update_layout(uirevision='constant')
    return figimg

# Datatable callback
@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_table(interval):
    df_raw = load_data(pklfile_raw)
    df_FMS = load_FMS_df(df_raw) #edit
    data = df_FMS.to_dict('records')
    return data
# magnet data callback
@app.callback(
    dash.dependencies.Output('table-magnet', 'data'),
    [dash.dependencies.Input('interval-component', 'n_intervals')])
def update_table(interval):
    df_raw = load_data(pklfile_raw)
    df = load_magnet_df(df_raw) #edit
    data = df.to_dict('records')
    return data

#Callback for Mapper Angle plot
@app.callback(
    dash.dependencies.Output('mapper-angle', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_mapperplot(n):
    df_raw = load_data(pklfile_raw)
    #figimgpropeller = px.imshow(img_xy)
    figimgpropeller = go.Figure()
    angle = float(df_raw['Mapper_Angle'].iloc[-1])
    angle = np.degrees(angle) - 45
    #img_prop = Image.open(datadir + 'Reflector Map Sketch.png')
    img = img_prop.rotate(angle)
    figimgpropeller.add_layout_image(dict(
        source=img_xy,
        x=0.77,
        y=0.03,
        layer='below'
    ))
    figimgpropeller.add_layout_image(dict(
        source=img,
        # x=0.74,
        x=0.745,
        # y=0.03,
        y=0.0,
    )
    )
    figimgpropeller.update_layout_images(dict(
        xref='paper',
        yref='paper',
        sizex=0.9,
        sizey=0.9,
        xanchor='right',
        yanchor='bottom',
        #uirevision = 'constant'          #Add some property here maybe?
    ))
    figimgpropeller.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    figimgpropeller.update_layout(yaxis={'visible': False, 'showticklabels': False},
                                  xaxis={'visible': False, 'showticklabels': False})

    figimgpropeller.update_layout(uirevision='constant')
    return figimgpropeller

#Running the dashboard
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug= True, port=8070)
