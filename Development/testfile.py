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
#     print(tdms_file["step:1.1.1"]['Timestamp'][:])

# df_raw = pd.read_pickle('../data/')
# print(df_raw.columns[110:])
# print(df_raw)



#BELOW HERE IS PICKLE STUFF
#picklefile = open('/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/RawDf:8-5updated.pkl', 'rb')
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# datadir = os.path.join(scriptdir, '..', 'data/')
# df_original = pd.read_pickle(datadir + "DSFM_test_data_v4N.pkl")
# #
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# datadir = os.path.join(scriptdir, '..', 'Downloads/')
# df_raw = pd.read_pickle(datadir + "FMSsystemtest.pkl")
#df_raw = pickle.load(picklefile)
#picklefile.close()

#print("This is df from Cole's original pickle",   df_original['TIMESTAMP'][:50])
# print("This is new pickle from TDMStoDFraw",   df_raw.columns[:50])


value = 'Bz_Meas'
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# datadir = os.path.join(scriptdir, '..', 'data/')
# picklefile = pd.read_pickle(datadir + "8-9.pkl")
picklefile = pd.read_pickle('/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/8-9.pkl')
#fig2 = px.scatter(picklefile, x = picklefile['TIMESTAMP'], y = [picklefile[f'HP_BP5_{value}'],picklefile[f'HP_BP4_{value}'], picklefile[f'HP_BP3_{value}'],picklefile[f'HP_BP2_{value}'], picklefile[f'HP_BP1_{value}']] )
fig2 = px.scatter(picklefile, x = picklefile['TIMESTAMP'], y = [picklefile[f'HP_SP1_{value}'],picklefile[f'HP_SP2_{value}'], picklefile[f'HP_SP3_{value}']] )
#fig2 = px.scatter(picklefile, )

fig2.update_xaxes(
        tickangle = 60,
        title_text = "Time",
        title_font = {"size": 20},
        title_standoff = 25)



fig2.show()

