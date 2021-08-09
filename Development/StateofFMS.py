import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import base64
import os
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

#opening the pickle file
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
df_raw = pd.read_pickle(datadir + "8-9.pkl")

#formatting new dataframes
df_NMR = df_raw[['TIMESTAMP', 'B_NMR']].copy()  #'X_NMR', 'Y_NMR', 'Z_NMR',
hall_probe_cols = []

for name in df_raw.columns:
    if "HP_" in name:
        hall_probe_cols.append(name)
df_Hall = df_raw[['TIMESTAMP']+ hall_probe_cols]

print(df_Hall)


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
print("this is B_field dataframe", df_Bfield)

df_dict = {'raw': df_raw, 'NMR': df_NMR, 'Hall Probes': df_Hall, 'Field at Location': df_Bfield, 'test': 0.}

####Images
image_filename = '/Users/Lillie/Desktop/Mu2e/DSFMimage1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename2 = '/Users/Lillie/Desktop/DSFM_Test_Data/dsfm overhead image.png'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())


z_loc = 400

# with open('/Users/Lillie/Desktop/DSFM_Test_Data/dsfm overhead image.png', "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read()).decode()

#add the prefix that plotly will want when using the string as source
# encoded_imagenew = "data:image/png;base64," + encoded_string


#trying to do the plot of the image on the graph
# pic = px.line(df_Hall, x = np.arange(0,2), y= np.repeat(15,2))
# pic.update_layout(images=[dict(
#                   source= encoded_imagenew,
#                   xref= "x",
#                   yref= "y",
#                   x= 0,
#                   y= 15,
#                   sizex= 50,
#                   sizey= 10,
#                   sizing= "stretch",
#                   opacity= 0.7,
#                   layer= "above")])

#load images
img_coil = Image.open(datadir + 'coils.png')
img_mapper = Image.open(datadir + 'DSFM_YZ_sketch.png')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
        html.Div(children=[html.Div([
        html.H1(children = 'State of the FMS Display')])]),
        html.Div([ html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))],className ="four columns"),
        #html.Div([ html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()))],className ="four columns"),

        html.Div([
            html.H3('Solenoid'),
            dcc.Graph(id='solenoid-mapper')
        ], className="six columns"),


        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Hall Probe 1', 'value': 'SP1'},
            {'label': 'Hall Probe 2', 'value': 'SP2'},
            {'label': 'Hall Probe 3', 'value': 'SP3'},
            {'label': 'Hall Probe 4', 'value': 'BP1'},
            {'label': 'Hall Probe 5', 'value': 'BP2'},
            {'label': 'Hall Probe 6', 'value': 'BP3'},
            {'label': 'Hall Probe 7', 'value': 'BP4'},
            {'label': 'Hall Probe 8', 'value': 'BP5'}
        ],
        #value='SP1'
    ),



       html.Div([
        html.Div([
            html.H3('Bz'),
            dcc.Graph(id='display-selected-values')
        ], className="six columns"),
        html.Div([
            html.H3('Br'),
            dcc.Graph(id='display-selected-values2')
        ], className="six columns"),
        html.Div([
            html.H3('Bphi'),
            dcc.Graph(id='display-selected-values3')
        ], className="six columns"),
        html.Div([
            html.H3('Temperature'),
            dcc.Graph(id='display-selected-values4')
        ], className="six columns"),

     ], className="row")
])

#Callback 1 for plot Bxz_Meas
@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output1(value):
    hall_probe = value

    fig1 = px.scatter(df_dict['Hall Probes'], x= 'TIMESTAMP', y = f'HP_{hall_probe}_Bz_Meas')
    return  fig1

#Callback 2 for plot Br
@app.callback(
    dash.dependencies.Output('display-selected-values2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_layout2(value):
    hall_probe = value

    fig2 = px.scatter(df_dict['Hall Probes'], x='TIMESTAMP', y = f'HP_{hall_probe}_Br')
    return fig2

#Callback 3 for plot Bphi
@app.callback(
    dash.dependencies.Output('display-selected-values3', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_layout3(value):
    hall_probe = value

    fig3 = px.scatter(df_dict['Hall Probes'], x='TIMESTAMP', y=f'HP_{hall_probe}_Bphi')
    return fig3

#Callback 4 for plot temperature
@app.callback(
    dash.dependencies.Output('display-selected-values4', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_layout3(value):
    hall_probe = value
    fig4 = px.scatter(df_dict['Hall Probes'], x='TIMESTAMP', y=f'HP_{hall_probe}_Temperature')
    return fig4

#Callback 5 for Solenoid img
@app.callback(
    dash.dependencies.Output('solenoid-mapper', 'figure'),
    [dash.dependencies.Input('df_raw', 'z_loc')])
def update_layout3(z_loc):
    # plot coils
    figimg = px.imshow(img_coil)

    # plot mapper towards tracker
    figimg.add_layout_image(dict(
        source=img_mapper,
        x=z_loc,
        y=0.35,
    )
    )



    return figimg

#Running the dashboard
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8070)