import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, GroupObject, ChannelObject
import pickle
import pandas as pd

# with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
#
#     #all_groups = tdms_file.groups()
#     for group in tdms_file.groups():
#         print(group)
#     #print(all_groups)
#     #print(tdms_file["step:1.1.4"]["Measured Coordinates"][:])
#     print(tdms_file["step:1.2.11"].channels())
#     print(tdms_file["step:1.1.1"]['Measured Coordinates'][:])
#
# df_raw = pd.read_pickle('../data/')
# print(df_raw.columns[110:])
# print(df_raw)
#

picklefile = open('/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/RawDf:8-5updated.pkl', 'rb')
df_raw = pickle.load(picklefile)
picklefile.close()

print(df_raw)
