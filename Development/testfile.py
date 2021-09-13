import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, GroupObject, ChannelObject
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

import os
#import plotly_express as px
import dash


#THIS IS TESTING FOR TDMS STUFF
with TdmsFile.open("/home/shared_data/FMS_Monitor/TestDataV2.tdms") as tdms_file:
#
     all_groups = tdms_file.groups()
     #for group in tdms_file.groups():
         #print(group)
     #print(all_groups)
     print(tdms_file["step:1.1.4"]["HallProbes"][:])
 #    print(tdms_file["step:1.2.11"].channels())
 #    print(tdms_file["step:1.200.16"]['Mapper'][:])

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

df_original = load_data("DSFM_test_data_1e-4_noise_v6.pkl")
def load_Bfield(df_raw):

    probe_ids = ['SP1', 'SP2', 'SP3', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']
    new_column_names = ['ID', 'X', 'Y', 'Z', 'Vx', 'Vy', 'Vz', 'Temperature',
                    'Bx_Meas', 'By_Meas', 'Bz_Meas'
                    ,'Br', 'Bphi', 'Bz' #, 'Bz',
                    ]
    results_dict = {key: [] for key in new_column_names}
    results_dict['TIMESTAMP'] = []

    for probe in probe_ids:
        results_dict['TIMESTAMP'].append(df_raw['TIMESTAMP'].values)
        for col in new_column_names:
             results_dict[col].append(df_raw[f'HP_{probe}_{col}'].values)
    for key in results_dict.keys():
        results_dict[key] = np.concatenate(results_dict[key])
    df_Bfield = pd.DataFrame(results_dict)
    return df_Bfield
df_Bfield = load_Bfield(df_raw)
print("this is df_Bfield", df_Bfield['HP_SP2_Bz_Meas'][:])
print("this is original", df_original['HP_SP1_Br'])
'''
minutes = int(time)
df_raw = load_data("liveupdates.pkl")
df_expected = load_data("DSFM_test_data_no_noise_v6.pkl")
# now = datetime.now()
now = df_raw['TIMESTAMP'].iloc[-1]
min_time = now - timedelta(minutes)
df_time = df_raw.query(f'TIMESTAMP > "{min_time}"')

#time = -1*int(time)  #Throwing a NoneType error with the time variable--fix!



    
measured_field = df_time[f'HP_SP1_Bz_Meas']
measured_field = measured_field.astype(np.float)
#numb = len(measured_field)
time0 = df_time[0]
time1 = df_time[-1]
df_expected_time = df_expected.query(f'"{time0}" <= TIMESTAMP <= "{time1}"')
expected_field = df_expected_time[f'HP_SP1_Bz_Meas']  #[:numb]
expected_field = expected_field.astype(np.float)

#timestamp = df_expected['TIMESTAMP'][-1:time]

fig1 = px.scatter(df_time, x= 'TIMESTAMP', y = [expected_field, measured_field])
    #fig1.update_traces(marker=dict(color='purple'))
fig1.update_xaxes(
            tickangle = 60,
            title_text = "Time",
            title_font = {"size": 20},
            title_standoff = 25)
fig1.update_yaxes(
        tickangle=60,
        title_text=f"Bz_meas",
        title_font={"size": 20},
        title_standoff=25)
#names = cycle(['Expected Value', 'Measured Value'])
#fig1.for_each_trace(lambda t: t.update(name=next(names)))
fig1





#data_since_tim = df_raw.query('TIMESTAMP.minute >= @minutes')
#data_since_tim = df_raw['TIMESTAMP'],minute
print(df_raw[:51])


df = load_data("DSFM_test_data_no_noise_v6.pkl")
print(df)

'''

dff = load_data("DSFM_test_data_1e-4_noise_v6.pkl")
print("this is original df with noise", dff)
print(dff.columns[:40])


