import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

#simple DSFM test with test data
# Read data from a csv
df = pd.read_csv('/Users/Lillie/Downloads/DSFM_test_data.csv')


fig = px.scatter_3d(df, x='X', y='Y', z='Z',
              color='Bx', opacity=0.7)


fig.update_layout(title="DSFM Test Data", autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

fig.update_layout(scene = dict(
                    xaxis_title='X axis',
                    yaxis_title='Y axis',
                    zaxis_title='Z axis '),
                    width=700,
                    margin=dict(r=20, b=10, l=10, t=10))
fig.show()

fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter



