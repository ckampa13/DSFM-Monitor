#Script for Test_Data_File_v2 to TDMS test file

import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

df = pd.read_pickle("/Users/Lillie/Downloads/DSFM_Test_Data/DSFM_test_data_v2.pkl")

#matrix = df.as_matrix(colums=df.columns[1:])
#print(matrix)
#
# root_object = RootObject(properties={
#     "prop1": "foo",
#     "prop2": 3,
# })
# Step_1_1 = GroupObject("Step:1.1", properties=())
# Timestamp = ChannelObject("Step:1.1", "Timestamp", dff[1,[0]], properties=())
#
#
# with TdmsWriter("TestDataV2.tdms") as tdms_writer:
#     tdms_writer.write_segment([root_object, Step_1_1,Timestamp])

#print(dff[:,[0]]) #Prints index zero for every single array, aka the entire first column
#tdms_file = TdmsFile("TestDataV2.tdms")
#tdms_file["Step_1_1"]["Timestamp"][:]


with TdmsWriter("TestDataV2.tdms") as tdms_writer:
    dff = df.to_numpy()
    #Change Z for every row, change X every 17th row and keep for 16 rows
    for i in range((len(dff))):
        group = GroupObject("Step_X_Z", properties={
            "name": "FMSSystemTest_v2",
            "Time": "start_time",
        })
        channel1 = ChannelObject('Step_X_Z', 'Timestamp', dff[i,[0]])
        #    channel2 = ChannelObject('group_name', 'StepID', dff[1,[0]]
        channel3 = ChannelObject('Step_X_Z', 'NMRProbe', dff[i,[1,2,3,4]])
        channel4 = ChannelObject('Step_X_Z', 'HallProbes', dff[i,[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,10,71,72,73,74,75,76]])
        tdms_writer.write_segment([group,channel1,channel3,channel4])
        #print("this is dff", dff[0,[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,10,71,72,73,74,75,76]])
        #print(dff[10,[1,2,3,4]])

# tdms_file = TdmsFile("TestDataV2.tdms")
# all_groups = tdms_file.groups()
# print(all_groups)
# group = tdms_file[""]
# all_group_channels = group.channels()

with TdmsFile.open("TestDataV2.tdms") as tdms_file:
    all_groups = tdms_file.groups()
    print(all_groups)
    #Accessing a group which for now is Step_X_Z with no numbers
    print(tdms_file["Step_X_Z"].channels())
    print(tdms_file["Step_X_Z"]["Timestamp"][:])
    print(tdms_file["Step_X_Z"]["NMRProbe"][:])
    print(tdms_file["Step_X_Z"]["HallProbes"][:])
#    print(tdms_file["group_name"].properties["prop2"]) #accessing properties
