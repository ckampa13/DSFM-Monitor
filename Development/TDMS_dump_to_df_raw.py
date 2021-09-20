import pandas as pd
from nptdms import TdmsFile
import pickle
import numpy as np
import os
import time

filename = '/home/shared_data/FMS_Monitor/TDMS_dump.pkl'
filename2 = '/home/shared_data/FMS_Monitor/liveupdates.pkl'
df = pd.read_pickle(filename)

# first dictionary with list comprehensions
probes = ('SP1', 'SP2', 'SP3','BP1', 'BP2', 'BP3', 'BP4', 'BP5')



map_dict = {f"HP_{probe}_Bz_Meas":[f"HallProbes_Z.field_{probe}", True, -100] for probe in probes}
map_dict.update({f"HP_{probe}_Bx_Meas":[f"HallProbes_X.field_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_By_Meas":[f"HallProbes_Y.field_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_X":[f"HallProbes_X.location_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Y":[f"HallProbes_Y.location_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Z":[f"HallProbes_Z.location_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Br":[f"HallProbes_Br.field_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Bphi":[f"HallProbes_Bphi.field_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Bz":[f"HallProbes_Bz_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Vx":[f"HallProbes_X.volt_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Vy":[f"HallProbes_Y.volt_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Vz":[f"HallProbes_Z.volt_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Temperature":[f"HallProbes_Temperature_{probe}", True, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Address":[f"HallProbes_Address_{probe}", False, -100] for probe in probes})
map_dict.update({f"HP_{probe}_Status":[f"HallProbes_Status_{probe}", False, -100] for probe in probes})
#map_dict.update({f"HP_{probe}_Sensor.name":[f"HallProbes_Sensor.name_{probe}", False, -100] for probe in probes})
map_dict.update({f"TIMESTAMP":[f"HallProbes_Timestamp_SP1", False, -100]})
map_dict.update({f"PS_Current":["Current_PS_Current", True, -100]})
map_dict.update({f"TS_Current":["Current_TS_Current", True, -100]})
map_dict.update({f"DS_Current":["Current_DS_Current", True, -100]})
map_dict.update({f"B_NMR":[f"NMRProbe_FluxDensity", True, -100]})
map_dict.update({f"Mapper_Angle":[f"Mapper_Angle", True, -100]})
map_dict.update({f"Mapper_Z":[f"Mapper_Position", True, -100]})

print(map_dict)

# loop through mapping dictionary
df_raw_dict = {}
for key in map_dict.keys():
    item =  map_dict[key]
    if item[0] in df.columns:
        if item[2] == True:
            df[item[0]] = df[item[0]].astype[float]
            #df_raw_dict[key] = df[item[0]]
            df_raw_dict.update({key: df[item[0]]})
        if item[2] == False:
            df_raw_dict.update({key: df[item[0]]})
          #       df_raw_dict[key] = df[item[0]]

    else:
        print(f"not found {key}")

#for checking the column names
for value in df.columns:
    if 'Mapper' in value:
        print(value)
print(df_raw_dict)


# dataframe + pickle file
df = pd.DataFrame(df_raw_dict)
df.to_pickle(filename2)


