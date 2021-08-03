import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pickle
import base64

df = pd.read_pickle("/data/Newpickle.py")

print(df)