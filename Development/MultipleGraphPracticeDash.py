import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import base64

#Dashboard with 3 graphs and 1 image of Mapper Propeller


# Read data from a csv
df = pd.read_csv('/Users/Lillie/Downloads/DSFM_test_data.csv')

# Create Figure 1 using Bx

fig = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='Bx', opacity=0.7)


fig.update_layout(title="", autosize=False,
                  width=500, height=500,
                  margin=dict(l=100, r=75, b=75, t=150))

fig.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    width=700,
                    margin=dict(r=30, b=20, l=30, t=20))

#Create Figure 2 using By
fig2 = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='By', opacity=0.7)

fig2.update_layout(title="", autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig2.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))

#Create figure 3 using Bz
fig3 = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='Bz', opacity=0.7)

fig3.update_layout(title="", autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig3.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))

#add image
image_filename = '/Users/Lillie/Desktop/Mu2e/DSFMimage1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


#Create Dash App
app = dash.Dash(__name__)
app.layout = html.Div(children=[html.Div([
    html.H1(children = 'DSFM Test Data'),
    html.Div(children = '''
    Plot using X, Y, Z and the magnetic field in the x direction
    '''),
    dcc.Graph(id = 'graph1', figure=fig, style={'display': 'inline-block'})
]), html.Div([
    html.H1(children = 'DSFM Test Data'),
    html.Div(children = '''
    Plot using X, Y, Z and the magnetic field in the y direction
    '''),
    dcc.Graph(id = 'graph2', figure=fig2, style={'display': 'inline-block'}), ]), html.Div([
    html.H1(children = 'DSFM Test Data'),
    html.Div(children = '''
    Plot using X, Y, Z and the magnetic field in the z direction
    '''),
    dcc.Graph(id = 'graph3', figure=fig3, style={'display': 'inline-block'}), ]), html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))]),
])



#Return dash app
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=8070)
