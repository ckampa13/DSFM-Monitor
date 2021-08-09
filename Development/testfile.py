import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, GroupObject, ChannelObject
import pickle
import pandas as pd
import os
import plotly_express as px
import dash


#THIS IS TESTING FOR TDMS STUFF
# with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
#
#     #all_groups = tdms_file.groups()
#     for group in tdms_file.groups():
#         print(group)
#     #print(all_groups)
#     #print(tdms_file["step:1.1.4"]["Measured Coordinates"][:])
#     print(tdms_file["step:1.2.11"].channels())
#     print(tdms_file["step:1.1.1"]['HallProbes'][:])

# df_raw = pd.read_pickle('../data/')
# print(df_raw.columns[110:])
# print(df_raw)



#BELOW HERE IS PICKLE STUFF
# picklefile = open('/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/RawDf:8-5updated.pkl', 'rb')
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# datadir = os.path.join(scriptdir, '..', 'data/')
# df_original = pd.read_pickle(datadir + "DSFM_test_data_v4.pkl")
#
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
df_raw = pd.read_pickle(datadir + "Newpickle.pkl")
#df_raw = pickle.load(picklefile)
#picklefile.close()

# print("This is df from Cole's original pickle",   df_original.columns[:50])
print("This is new pickle from TDMStoDFraw",   df_raw.columns[:50])

fig = px.line(df_raw, x = df_raw['TIMESTAMP'], y = df_raw['HP_SP2_Bz_Meas'])
fig.show()