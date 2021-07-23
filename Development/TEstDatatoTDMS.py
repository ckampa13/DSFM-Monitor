#Script for Test_Data_File_v2 to TDMS test file

import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, RootObject, GroupObject, ChannelObject

df = pd.read_pickle("/Users/Lillie/Downloads/DSFM_Test_Data/DSFM_test_data_v3.pkl")


def write_NMR(index, dataframe):
    ProbeName = "NMR"
    ProbeID = "Metrolab Technology SA,PT2026,25,elC2D1B2-arm1.21-dsp2.8-cpld1.9-pa3.7-opt00000000\n"
    Status = "OK"
    Timestamp = dataframe['TIMESTAMP'].loc[index]
    Fluxdensity = dataframe['B_NMR'].loc[index]
    NMR_array = np.array([f'ProbeName:{ProbeName}', f"ProbeID:{ProbeID}",f"FluxDensity:{Fluxdensity}", f"Status:{Status}", f"Timestamp:{Timestamp}" ])
    return NMR_array

def write_Hall(index, dataframe):
    SP1address = ''
    SP1temp = dataframe['HP_SP1_Temperature'].loc[index]
    SP1_Z_field = dataframe['HP_SP1_Bz_Meas'].loc[index]
    SP1_Y_field = dataframe['HP_SP1_By_Meas'].loc[index]
    SP1_X_field = dataframe['HP_SP1_Bx_Meas'].loc[index]
    SP1_Z_volt = dataframe['HP_SP1_Vz'].loc[index]
    SP1_Y_volt = dataframe['HP_SP1_Vy'].loc[index]
    SP1_X_volt = dataframe['HP_SP1_Vx'].loc[index]
    SP1_status = 'OK'
    SP1_Sensorname = 'SP1'
    SP1_SensorID = dataframe['HP_SP1_ID'].loc[index]
    SP1_Timestamp = dataframe['TIMESTAMP'].loc[index]

    SP2address = ''
    SP2temp = dataframe['HP_SP2_Temperature'].loc[index]
    SP2_Z_field = dataframe['HP_SP2_Bz_Meas'].loc[index]
    SP2_Y_field = dataframe['HP_SP2_By_Meas'].loc[index]
    SP2_X_field = dataframe['HP_SP2_Bx_Meas'].loc[index]
    SP2_Z_volt = dataframe['HP_SP2_Vz'].loc[index]
    SP2_Y_volt = dataframe['HP_SP2_Vy'].loc[index]
    SP2_X_volt = dataframe['HP_SP2_Vx'].loc[index]
    SP2_status = 'OK'
    SP2_Sensorname = 'SP2'
    SP2_SensorID = dataframe['HP_SP2_ID'].loc[index]
    SP2_Timestamp = dataframe['TIMESTAMP'].loc[index]

    SP3address = ''
    SP3temp = dataframe['HP_SP3_Temperature'].loc[index]
    SP3_Z_field = dataframe['HP_SP3_Bz_Meas'].loc[index]
    SP3_Y_field = dataframe['HP_SP3_By_Meas'].loc[index]
    SP3_X_field = dataframe['HP_SP3_Bx_Meas'].loc[index]
    SP3_Z_volt = dataframe['HP_SP3_Vz'].loc[index]
    SP3_Y_volt = dataframe['HP_SP3_Vy'].loc[index]
    SP3_X_volt = dataframe['HP_SP3_Vx'].loc[index]
    SP3_status = 'OK'
    SP3_Sensorname = 'SP3'
    SP3_SensorID = dataframe['HP_SP3_ID'].loc[index]
    SP3_Timestamp = dataframe['TIMESTAMP'].loc[index]

    BP1address = ''
    BP1temp = dataframe['HP_BP1_Temperature'].loc[index]
    BP1_Z_field = dataframe['HP_BP1_Bz_Meas'].loc[index]
    BP1_Y_field = dataframe['HP_BP1_By_Meas'].loc[index]
    BP1_X_field = dataframe['HP_BP1_Bx_Meas'].loc[index]
    BP1_Z_volt = dataframe['HP_BP1_Vz'].loc[index]
    BP1_Y_volt = dataframe['HP_BP1_Vy'].loc[index]
    BP1_X_volt = dataframe['HP_BP1_Vx'].loc[index]
    BP1_status = 'OK'
    BP1_Sensorname = 'BP1'
    BP1_SensorID = dataframe['HP_BP1_ID'].loc[index]
    BP1_Timestamp = dataframe['TIMESTAMP'].loc[index]

    BP2address = ''
    BP2temp = dataframe['HP_BP2_Temperature'].loc[index]
    BP2_Z_field = dataframe['HP_BP2_Bz_Meas'].loc[index]
    BP2_Y_field = dataframe['HP_BP2_By_Meas'].loc[index]
    BP2_X_field = dataframe['HP_BP2_Bx_Meas'].loc[index]
    BP2_Z_volt = dataframe['HP_BP2_Vz'].loc[index]
    BP2_Y_volt = dataframe['HP_BP2_Vy'].loc[index]
    BP2_X_volt = dataframe['HP_BP2_Vx'].loc[index]
    BP2_status = 'OK'
    BP2_Sensorname = 'BP2'
    BP2_SensorID = dataframe['HP_BP2_ID'].loc[index]
    BP2_Timestamp = dataframe['TIMESTAMP'].loc[index]

    BP3address = ''
    BP3temp = dataframe['HP_BP3_Temperature'].loc[index]
    BP3_Z_field = dataframe['HP_BP3_Bz_Meas'].loc[index]
    BP3_Y_field = dataframe['HP_BP3_By_Meas'].loc[index]
    BP3_X_field = dataframe['HP_BP3_Bx_Meas'].loc[index]
    BP3_Z_volt = dataframe['HP_BP3_Vz'].loc[index]
    BP3_Y_volt = dataframe['HP_BP3_Vy'].loc[index]
    BP3_X_volt = dataframe['HP_BP3_Vx'].loc[index]
    BP3_status = 'OK'
    BP3_Sensorname = 'BP3'
    BP3_SensorID = dataframe['HP_BP3_ID'].loc[index]
    BP3_Timestamp = dataframe['TIMESTAMP'].loc[index]

    BP4address = ''
    BP4temp = dataframe['HP_BP4_Temperature'].loc[index]
    BP4_Z_field = dataframe['HP_BP4_Bz_Meas'].loc[index]
    BP4_Y_field = dataframe['HP_BP4_By_Meas'].loc[index]
    BP4_X_field = dataframe['HP_BP4_Bx_Meas'].loc[index]
    BP4_Z_volt = dataframe['HP_BP4_Vz'].loc[index]
    BP4_Y_volt = dataframe['HP_BP4_Vy'].loc[index]
    BP4_X_volt = dataframe['HP_BP4_Vx'].loc[index]
    BP4_status = 'OK'
    BP4_Sensorname = 'BP4'
    BP4_SensorID = dataframe['HP_BP4_ID'].loc[index]
    BP4_Timestamp = dataframe['TIMESTAMP'].loc[index]

    BP5address = ''
    BP5temp = dataframe['HP_BP5_Temperature'].loc[index]
    BP5_Z_field = dataframe['HP_BP5_Bz_Meas'].loc[index]
    BP5_Y_field = dataframe['HP_BP5_By_Meas'].loc[index]
    BP5_X_field = dataframe['HP_BP5_Bx_Meas'].loc[index]
    BP5_Z_volt = dataframe['HP_BP5_Vz'].loc[index]
    BP5_Y_volt = dataframe['HP_BP5_Vy'].loc[index]
    BP5_X_volt = dataframe['HP_BP5_Vx'].loc[index]
    BP5_status = 'OK'
    BP5_Sensorname = 'BP1'
    BP5_SensorID = dataframe['HP_BP5_ID'].loc[index]
    BP5_Timestamp = dataframe['TIMESTAMP'].loc[index]

    Hall_array = np.array([f'Address:{SP1address}', f'Temperature:{SP1temp}', f'Z.field:{SP1_Z_field}', f'Y.field:{SP1_Y_field}', f'X.field:{SP1_X_field}', f'Z.zolt:{SP1_Z_volt}',f'Y.volt:{SP1_Y_volt}', f'X.volt:{SP1_X_volt}', f'Status:{SP1_status}', f'Sensor.name:{SP1_Sensorname}', f'Sensor.ID:{SP1_SensorID}', f'Timestamp:{SP1_Timestamp}',
                          f'Address:{SP2address}', f'Temperature:{SP2temp}', f'Z.field:{SP2_Z_field}', f'Y.field:{SP2_Y_field}', f'X.field:{SP2_X_field}', f'Z.zolt:{SP2_Z_volt}',f'Y.volt:{SP2_Y_volt}', f'X.volt:{SP2_X_volt}', f'Status:{SP2_status}', f'Sensor.name:{SP2_Sensorname}', f'Sensor.ID:{SP2_SensorID}', f'Timestamp:{SP2_Timestamp}',
                          f'Address:{SP3address}', f'Temperature:{SP3temp}', f'Z.field:{SP3_Z_field}', f'Y.field:{SP3_Y_field}', f'X.field:{SP3_X_field}', f'Z.zolt:{SP3_Z_volt}',f'Y.volt:{SP3_Y_volt}', f'X.volt:{SP3_X_volt}', f'Status:{SP3_status}', f'Sensor.name:{SP3_Sensorname}', f'Sensor.ID:{SP3_SensorID}', f'Timestamp:{SP3_Timestamp}',
                          f'Address:{BP1address}', f'Temperature:{BP1temp}', f'Z.field:{BP1_Z_field}', f'Y.field:{BP1_Y_field}', f'X.field:{BP1_X_field}', f'Z.zolt:{BP1_Z_volt}',f'Y.volt:{BP1_Y_volt}', f'X.volt:{BP1_X_volt}', f'Status:{BP1_status}', f'Sensor.name:{BP1_Sensorname}', f'Sensor.ID:{BP1_SensorID}', f'Timestamp:{BP1_Timestamp}',
                          f'Address:{BP2address}', f'Temperature:{BP2temp}', f'Z.field:{BP2_Z_field}', f'Y.field:{BP2_Y_field}', f'X.field:{BP2_X_field}', f'Z.zolt:{BP2_Z_volt}',f'Y.volt:{BP2_Y_volt}', f'X.volt:{BP2_X_volt}', f'Status:{BP2_status}', f'Sensor.name:{BP2_Sensorname}', f'Sensor.ID:{BP2_SensorID}', f'Timestamp:{BP2_Timestamp}',
                          f'Address:{BP3address}', f'Temperature:{BP3temp}', f'Z.field:{BP3_Z_field}', f'Y.field:{BP3_Y_field}', f'X.field:{BP3_X_field}', f'Z.zolt:{BP3_Z_volt}',f'Y.volt:{BP3_Y_volt}', f'X.volt:{BP3_X_volt}', f'Status:{BP3_status}', f'Sensor.name:{BP3_Sensorname}', f'Sensor.ID:{BP3_SensorID}', f'Timestamp:{BP3_Timestamp}',
                          f'Address:{SP1address}', f'Temperature:{SP1temp}', f'Z.field:{BP4_Z_field}', f'Y.field:{BP4_Y_field}', f'X.field:{BP4_X_field}', f'Z.zolt:{BP4_Z_volt}',f'Y.volt:{BP4_Y_volt}', f'X.volt:{BP4_X_volt}', f'Status:{BP4_status}', f'Sensor.name:{BP4_Sensorname}', f'Sensor.ID:{BP4_SensorID}', f'Timestamp:{BP4_Timestamp}',
                          f'Address:{SP1address}', f'Temperature:{SP1temp}', f'Z.field:{BP5_Z_field}', f'Y.field:{BP5_Y_field}', f'X.field:{BP5_X_field}', f'Z.zolt:{BP5_Z_volt}',f'Y.volt:{BP5_Y_volt}', f'X.volt:{BP5_X_volt}', f'Status:{BP5_status}', f'Sensor.name:{BP5_Sensorname}', f'Sensor.ID:{BP5_SensorID}', f'Timestamp:{BP5_Timestamp}'])
    return Hall_array

def write_Timestamp(index, dataframe):
    timestamp = dataframe['TIMESTAMP'].loc[index]
    Timestamp_array = np.array(f'Timestamp:{timestamp}')
    return Timestamp_array


########

with TdmsWriter("TestDataV2.tdms") as tdms_writer:
    dff = df.to_numpy()

    for i in range((len(dff))):
        group = GroupObject("Step_X_Z", properties={
            "name": "FMSSystemTest_v2",
            "Time": "start_time",
        })
        channel1 = ChannelObject('Step_X_Z', 'Timestamp', dff[i,[0]], )
        #    channel2 = ChannelObject('group_name', 'StepID', dff[1,[0]]
        channel3 = ChannelObject('Step_X_Z', 'NMRProbe', dff[i,[1,2,3,4]])
        channel4 = ChannelObject('Step_X_Z', 'HallProbes', dff[i,[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,10,71,72,73,74,75,76]])
        tdms_writer.write_segment([group,channel1,channel3,channel4])




with TdmsFile.open("TestDataV2.tdms") as tdms_file:
    all_groups = tdms_file.groups()
    print(all_groups)
    #Accessing a group which for now is Step_X_Z with no numbers
    print(tdms_file["Step_X_Z"].channels())
    print("This is contents of Timestamp Channel:", tdms_file["Step_X_Z"]["Timestamp"][:])
    print("this is contents of NMRProbe Channel:", tdms_file["Step_X_Z"]["NMRProbe"][:])
    print("This is contents of HallProbes Channel:", tdms_file["Step_X_Z"]["HallProbes"][:])
#    print(tdms_file["group_name"].properties["prop2"]) #accessing properties

#New Section
#
# my_df.reset_index(drop=True, inplace=True)
#
# for index, row in my_df.iterrows():
#     if index % 16 == 0:
#         my_df.loc[index, "value"] = value_I_want