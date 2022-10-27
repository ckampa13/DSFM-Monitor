# want a dash app to easily explore a TDMS file.
# essentially basic features of nptdms, but all accessed via mouse clicks.
import os
import json
from nptdms import TdmsFile
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

# directories and files
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.realpath(os.path.join(scriptdir, '..', 'data'))
available_tdms = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(datadir)) for f in fn]
available_tdms = [f for f in available_tdms if f[-5:] == ".tdms"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(name='tdms_browser', external_stylesheets=external_stylesheets)


def parse_tdms(filename):
    tdms_data = dict()
    try:
        # Assume tdms file input
        with TdmsFile.open(filename) as tdms_file:
            groups = groups_list_of_strings(tdms_file)
            for group in groups:
                tdms_data[group] = dict()
                channels = channels_list_of_strings(tdms_file, group)
                for channel in channels:
                    tdms_data[group][channel] = list(tdms_file[group][channel][:])
    except Exception as e:
        print(e)
        return e

    return tdms_data

def groups_list_of_strings(tdms_file):
    return [i.name for i in tdms_file.groups()]

def channels_list_of_strings(tdms_file, group):
    return [i.name for i in tdms_file[group].channels()]

app.layout = html.Div([
    html.H1('TDMS File Browser'),
    html.H2('File Selection'),
    dcc.Dropdown(id='file-select',
                 options=[{'label':i.lstrip(datadir), 'value':i} for i in available_tdms]),
    html.Div(id='file-output'),
    html.H2('Browse'),
    html.H3('Select a group:'),
    dcc.Dropdown(id='group-select',),
    html.Div(id='group-output',
             style={'white-space': 'pre',
                    'overflow-x': 'scroll',
                    'width': '99vw'
                    },
             ),
    html.H3('Select a channel:'),
    dcc.Dropdown(id='channel-select',),
    html.Div(id='channel-output',
             style={'white-space': 'pre-wrap',
                    'width': '99vw'
                    },
            ),
    # hidden data div
    html.Div(id='tdms-data', style={'display': 'none'}),
])


# file upload
@app.callback(
    Output('tdms-data', 'children'),
    Input('file-select', 'value'),
)
def update_tdms_output(fname):
    if fname is not None:
        tdms_data = parse_tdms(fname)
    else:
        tdms_data = dict()
    return json.dumps(tdms_data)

@app.callback(
    Output('file-output', 'children'),
    Input('file-select', 'value')
)
def update_file_info_output(fname):
    return f"Browsing file: {fname}"

@app.callback(
    Output('group-select', 'options'),
    Input('tdms-data', 'children')
)
def set_group_options(tdms_data):
    if tdms_data is not None:
        tdms_data = json.loads(tdms_data)
        return [{'label': i, 'value': i} for i in tdms_data.keys()]
    else:
        return []

@app.callback(
    Output(component_id='group-output', component_property='children'),
    Input(component_id='group-select', component_property='value'),
    Input('tdms-data', 'children')
)
def update_group_output(input_group, tdms_data):
    if (input_group is not None) and (tdms_data is not None):
        tdms_data = json.loads(tdms_data)
        out_str = f'The selected group, "{input_group}" has the following channels:\n'
        out_str += f'{tdms_data[input_group].keys()}'
    else:
        out_str = ''
    return out_str

@app.callback(
    Output('channel-select', 'options'),
    Input('group-select', 'value'),
    Input('tdms-data', 'children')
)
def set_channel_options(input_group, tdms_data):
    if (tdms_data is not None) and (input_group is not None):
        tdms_data = json.loads(tdms_data)
        return [{'label': i, 'value': i} for i in tdms_data[input_group].keys()]
    else:
        return []


@app.callback(
    Output(component_id='channel-output', component_property='children'),
    Input(component_id='channel-select', component_property='value'),
    Input(component_id='group-select', component_property='value'),
    Input('tdms-data', 'children')
)
def update_channel_output(input_channel, input_group, tdms_data):
    if input_channel is None:
        return ""
    else:
        tdms_data = json.loads(tdms_data)
        entries = tdms_data[input_group][input_channel]
        out_str = f'The selected group/channel, "{input_group}"/"{input_channel}" has the following entries:\n'
        out_str += f'{entries}'
        return out_str

if __name__ == '__main__':
    app.run_server(debug=True)
