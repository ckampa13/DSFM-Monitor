import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import base64
import numpy as np

#Dashboard with 3 graphs and 1 image of Mapper Propeller


# Read data from a csv
df = pd.read_csv('/Users/Lillie/Downloads/DSFM_test_data.csv')

# Create Figure 1 using Bx

fig = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='Bx', opacity=0.7)


fig.update_layout(title="", autosize=True,
                  #width=500, height=500,
                  margin=dict(l=100, r=75, b=75, t=150))

fig.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    #width=700,
                    margin=dict(r=30, b=20, l=30, t=20))

#Create Figure 2 using By
fig2 = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='By', opacity=0.7)

fig2.update_layout(title="", autosize=True,
                  #width=500, height=500,
                  margin=dict(l=25, r=20, b=35, t=20))

fig2.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    #width=300,
                    margin=dict(r=20, b=10, l=10, t=10))

#Create figure 3 using Bz
fig3 = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='Bz', opacity=0.7)

fig3.update_layout(title="", autosize=True,
                  #width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig3.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    #width=700,
                    margin=dict(r=20, b=10, l=10, t=10))
#figure 4 temperature plot
temp_values = [71.2, 72.3, 72.5, 71.9, 72.2, 72.23, 73.3, 73.2]
time = np.arange(8,16)
fig4 = px.scatter(df, x= time, y=temp_values)
fig4.update_layout(scene = dict(
    xaxis_title='Time in minutes',
    yaxis_title='Temperature of Hall Probe'))
#add image
image_filename = '/Users/Lillie/Desktop/Mu2e/DSFMimage1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename2 = '/Users/Lillie/Desktop/DSFM_Test_Data/dsfm overhead image.png'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Create Dash App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div(children=[html.Div([
        html.H1(children = 'State of the FMS Display')])]),
        html.Div([ html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))],className ="four columns"),
        html.Div([ html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()))],className ="four columns"),
        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Hall Probe 1', 'value': 'NYC'},
            {'label': 'Hall Probe 2', 'value': 'MTL'},
            {'label': 'Hall Probe 3', 'value': 'SF'},
            {'label': 'Hall Probe 4', 'value': 'SF'},
            {'label': 'Hall Probe 5', 'value': 'SF'},
            {'label': 'Hall Probe 6', 'value': 'SF'},
            {'label': 'Hall Probe 7', 'value': 'SF'},
            {'label': 'Hall Probe 8', 'value': 'SF'}
        ],
        value='NYC'
    ),
    html.Div([
        html.Div([
            html.H3('Bx'),
            dcc.Graph(id='graph1', figure= fig)
        ], className="three columns"),

        html.Div([
            html.H3('By'),
            dcc.Graph(id='graph2', figure=fig2)
        ], className="three columns"),
        html.Div([
            html.H3('Bz'),
            dcc.Graph(id='graph3', figure=fig3)
        ], className="three columns"),
        html.Div([
            html.H3('Temperature'),
            dcc.Graph(id='graph4', figure=fig4)
        ], className="three columns"),

    ], className="row")
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)




#Return dash app
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8070)
