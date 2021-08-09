

###################################ORIGINAL STATE OF FMS PLOTS

####Images
image_filename = '/Users/Lillie/Desktop/Mu2e/DSFMimage1.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename2 = '/Users/Lillie/Desktop/DSFM_Test_Data/dsfm overhead image.png'
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())


with open('/Users/Lillie/Desktop/DSFM_Test_Data/dsfm overhead image.png', "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

#add the prefix that plotly will want when using the string as source
encoded_imagenew = "data:image/png;base64," + encoded_string


#trying to do the plot of the image on the graph
pic = px.line(df_Hall, x = np.arange(0,2), y= np.repeat(15,2))
pic.update_layout(images=[dict(
                  source= encoded_imagenew,
                  xref= "x",
                  yref= "y",
                  x= 0,
                  y= 15,
                  sizex= 50,
                  sizey= 10,
                  sizing= "stretch",
                  opacity= 0.7,
                  layer= "above")])

# fig.add_layout_image(
#     dict(
#         source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
#         xref="paper", yref="paper",
#         x=1, y=1.05,
#         sizex=0.2, sizey=0.2,
#         xanchor="right", yanchor="bottom"
#     )
# )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
        html.Div(children=[html.Div([
        html.H1(children = 'State of the FMS Display')])]),
        html.Div([ html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))],className ="four columns"),
        #html.Div([ html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()))],className ="four columns"),

        html.Div([
            html.H3('Solenoid'),
            dcc.Graph(id='solenoid picture', figure = pic)
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
            html.H3('Bx'),
            dcc.Graph(id='display-selected-values')
        ], className="six columns"),

        html.Div([
            html.H3('By'),
            dcc.Graph(id='display-selected-values2')
        ], className="six columns"),
        html.Div([
            html.H3('Bz'),
            dcc.Graph(id='display-selected-values3')
        ], className="six columns"),
    #     html.Div([
    #         html.H3('Temperature'),
    #         dcc.Graph(id='fig4', figure=fig4)
    #     ], className="six columns"),
    #
     ], className="row")
])

#Callback 1 for plot Bx
@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output1(value):
    hall_probe = value
    fig1 = px.scatter_3d(df_dict['Hall Probes'], x=f'HP_{hall_probe}_X', y=f'HP_{hall_probe}_Y', z=f'HP_{hall_probe}_Z',
                         color=f'HP_{hall_probe}_Bx_Meas')
    return  fig1

#Callback 2 for plot By
@app.callback(
    dash.dependencies.Output('display-selected-values2', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_layout2(value):
    hall_probe = value
    fig2 = px.scatter_3d(df_dict['Hall Probes'], x=f'HP_{hall_probe}_X', y=f'HP_{hall_probe}_Y', z=f'HP_{hall_probe}_Z',
                         color=f'HP_{hall_probe}_By_Meas')
    return fig2

#Callback 3 for plot Bz
@app.callback(
    dash.dependencies.Output('display-selected-values3', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_layout3(value):
    hall_probe = value
    fig3 = px.scatter_3d(df_dict['Hall Probes'], x=f'HP_{hall_probe}_X', y=f'HP_{hall_probe}_Y', z=f'HP_{hall_probe}_Z',
                         color=f'HP_{hall_probe}_Bz_Meas')
    return fig3

##############################################Plots of value verses time

value = 'Br'
picklefile = pd.read_pickle('/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/8-9.pkl')
fig = px.scatter(picklefile, x = picklefile['TIMESTAMP'], y = [picklefile[f'HP_BP5_{value}'],picklefile[f'HP_BP4_{value}'], picklefile[f'HP_BP3_{value}'],picklefile[f'HP_BP2_{value}'], picklefile[f'HP_BP1_{value}']] )
fig2 = px.scatter(picklefile, x = picklefile['TIMESTAMP'], y = [picklefile[f'HP_SP1_{value}'],picklefile[f'HP_SP2_{value}'], picklefile[f'HP_SP3_{value}']] )

