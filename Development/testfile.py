import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, GroupObject, ChannelObject
import pickle
import pandas as pd

import os
#import plotly_express as px
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
#     print(tdms_file["step:1.200.16"]['Mapper'][:])

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

#print("This is df from Cole's original pickle",   df_original['HP_BP1_Bz_Meas'].iloc[-1])
# print("This is new pickle from TDMStoDFraw",   df_raw.columns[:50])


#value = 'Bz_Meas'
# scriptdir = os.path.dirname(os.path.realpath(__file__))
# datadir = os.path.join(scriptdir, '..', 'data/')
# picklefile = pd.read_pickle(datadir + "8-9.pkl")
#picklefile = pd.read_pickle('/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/8-9.pkl')
#fig2 = px.scatter(picklefile, x = picklefile['TIMESTAMP'], y = [picklefile[f'HP_BP5_{value}'],picklefile[f'HP_BP4_{value}'], picklefile[f'HP_BP3_{value}'],picklefile[f'HP_BP2_{value}'], picklefile[f'HP_BP1_{value}']] )
#fig2 = px.scatter(picklefile, x = picklefile['TIMESTAMP'], y = [picklefile[f'HP_SP1_{value}'],picklefile[f'HP_SP2_{value}'], picklefile[f'HP_SP3_{value}']] )
#fig2 = px.scatter(picklefile, )

# fig2.update_xaxes(
#         tickangle = 60,
#         title_text = "Time",
#         title_font = {"size": 20},
#         title_standoff = 25)
'''
groupnamelist = []
with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
    groups = tdms_file.groups()
    for group in groups:
        groupname = group.name
        if groupname == 'run:R_2021' or groupname[2] == 'q':
            pass
        # if groupname in previous_group_names:
        #     pass
        else:
            groupnamelist.append(groupname)
            #previous_group_names.append(groupname)

    for name in groupnamelist:
        #print(tdms_file[f'{name}']['HallProbes'][:])

        for chunk in tdms_file.data_chunks():
            group_chunk = chunk[f'{name}']
            print(np.array(group_chunk.channels()[:], dtype=object))

            # channel_chunk = chunk[f'{name}']['HallProbes']
            # array = np.array(channel_chunk[:])
            # if array.size > 0:
            #     print(array)

print(groupnamelist)
'''
datadir = '/home/shared_data/FMS_Monitor/'

def load_data(filename):
    df_raw = pd.read_pickle(datadir + f"{filename}")
    return df_raw

df_raw = load_data("liveupdates.pkl")

time_last_minute = (df_raw['TIMESTAMP'].iloc[-1]).minute
time_last_hour = (df_raw['TIMESTAMP'].iloc[-1]).hour

time_interval_minutes = 5
minutes = time_last_minute - time_interval_minutes
print((df_raw['TIMESTAMP'].iloc[1]).minute)

#data_since_tim = df_raw.query('TIMESTAMP.minute >= @minutes')
#data_since_tim = df_raw['TIMESTAMP'],minute
print(df_raw[:51])


