import plotly.graph_objects as go
from PIL import Image
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
import base64


#attempting to display propeller image as background image in plot

# # Create figure
# import base64
#
# with open("/Users/Lillie/Desktop/Mu2e/DSFMimage1.png", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read()).decode()
# #add the prefix that plotly will want when using the string as source
# encoded_image = "data:image/png;base64," + encoded_string

image_filename = '/Users/Lillie/Desktop/Mu2e/DSFMimage1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())



fig = go.Figure()

# Add trace
fig.add_trace(
    go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
)

# Add images
fig.add_layout_image(
        dict(
            source= 'data:image/png;base64,{}'.format(encoded_image.decode()),
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=4,
            opacity=0.7,
            layer="below")

)

#x axis turn off
fig.update_xaxes(visible=False)

#y axis turn off
fig.update_yaxes(visible=False)

#Legend (not included in this plot)
#fig.update_layout(showlegend=False)



#Write image
pio.write_image(fig, 'fig1.png')

# Set templates
fig.update_layout(template="plotly_white")


#Dash app
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)

