import pandas as pd
from nptdms import TdmsFile
import pickle
import numpy as np

#Edits will be made to clean this up!!  yes it is not concise at the moment

#tdms_file = TdmsFile.read("../data/TestDataV2.tdms")
#groups = tdms_file.groups()


#Bunch of lists
groupnamelist = []
timestamp_values = []
stepid_values = []
stepidnumber_values = []
mapperangle_values = []
mapper_Z_values = []
bnmr_values = []


#add groupnames to group name list
# for group in groups:
#     groupname = group.name
#     groupnamelist.append(groupname)

#do timestamp columns
def write_timestamp(groupname, tdms_file):
    timestamp = tdms_file[f'{groupname}']['Timestamp'].read_data()[0]
    lineelements = timestamp.split(':')
    if lineelements[0] == 'Timestamp':
        column_value = lineelements[1]+ ':'+ lineelements[2] + ':' + lineelements[3]
        timestamp_values.append(column_value)
#do both step ID columns
def write_stepID(groupname, tdms_file):
    stepID = tdms_file[f'{groupname}']['StepID'].read_data()[0]
    # lineelements = stepID.split(':')
    # stepid_values.append(lineelements[0])
    stepid_values.append(stepID)
    stepIDnub = tdms_file[f'{groupname}']['StepID'].read_data()[0]
    lineelements = stepIDnub.split(':')
    stepidnumber_values.append(lineelements[0])
#Mapper!
def write_mapper(groupname, tdms_file):
    mapperangle = tdms_file[f'{groupname}']['Mapper'].read_data()[3]
    lineelements = mapperangle.split(':')
    mapperangle_values.append(lineelements[1])
    mapperz = tdms_file[f'{groupname}']['Mapper'].read_data()[4]
    lineelements2 = mapperz.split(':')
    mapper_Z_values.append(lineelements2[1])
#NMR
def write_NMR(groupname, tdms_file):
    bnmr = tdms_file[f'{groupname}']['NMRProbe'].read_data()[2]
    lineelements = bnmr.split(':')
    bnmr_values.append(lineelements[1])
#do all the hall probe columns
SP1_ID = []
SP1_X = []
SP1_Y = []
SP1_Z = []
SP1_Vx = []
SP1_Vy = []
SP1_Vz = []
SP1_Temperature = []
SP1_Bx = []
SP1_By = []
SP1_Bz = []
SP1_Br = []
SP1_Bphi = []

SP2_ID = []
SP2_X = []
SP2_Y = []
SP2_Z = []
SP2_Vx = []
SP2_Vy = []
SP2_Vz = []
SP2_Temperature = []
SP2_Bx = []
SP2_By = []
SP2_Bz = []
SP2_Br = []
SP2_Bphi = []

SP3_ID = []
SP3_X = []
SP3_Y = []
SP3_Z = []
SP3_Vx = []
SP3_Vy = []
SP3_Vz = []
SP3_Temperature = []
SP3_Bx = []
SP3_By = []
SP3_Bz = []
SP3_Br = []
SP3_Bphi = []

BP1_ID = []
BP1_X = []
BP1_Y = []
BP1_Z = []
BP1_Vx = []
BP1_Vy = []
BP1_Vz = []
BP1_Temperature = []
BP1_Bx = []
BP1_By = []
BP1_Bz = []
BP1_Br = []
BP1_Bphi = []

BP2_ID = []
BP2_X = []
BP2_Y = []
BP2_Z = []
BP2_Vx = []
BP2_Vy = []
BP2_Vz = []
BP2_Temperature = []
BP2_Bx = []
BP2_By = []
BP2_Bz = []
BP2_Br = []
BP2_Bphi = []

BP3_ID = []
BP3_X = []
BP3_Y = []
BP3_Z = []
BP3_Vx = []
BP3_Vy = []
BP3_Vz = []
BP3_Temperature = []
BP3_Bx = []
BP3_By = []
BP3_Bz = []
BP3_Br = []
BP3_Bphi = []

BP4_ID = []
BP4_X = []
BP4_Y = []
BP4_Z = []
BP4_Vx = []
BP4_Vy = []
BP4_Vz = []
BP4_Temperature = []
BP4_Bx = []
BP4_By = []
BP4_Bz = []
BP4_Br = []
BP4_Bphi = []

BP5_ID = []
BP5_X = []
BP5_Y = []
BP5_Z = []
BP5_Vx = []
BP5_Vy = []
BP5_Vz = []
BP5_Temperature = []
BP5_Bx = []
BP5_By = []
BP5_Bz = []
BP5_Br = []
BP5_Bphi = []



def write_HallProbe(groupname, tdms_file):
    hallprobes = {'SP1': [0, SP1_ID, 0, SP1_X, 0, SP1_Y, 0, SP1_Z, 0, SP1_Vx, 0, SP1_Vy, 0, SP1_Vz, 0, SP1_Temperature, 0, SP1_Bx, 0, SP1_By, 0, SP1_Bz, 0, SP1_Br, 0, SP1_Bphi],
                  'SP2': [17, SP2_ID, 17, SP2_X, 17, SP2_Y, 17, SP2_Z, 17, SP2_Vx, 17, SP2_Vy, 17, SP2_Vz, 17, SP2_Temperature, 17, SP2_Bx, 17, SP2_By, 17, SP2_Bz, 17, SP2_Br, 17, SP2_Bphi],
                  'SP3': [34, SP3_ID, 34, SP3_X, 34, SP3_Y, 34, SP3_Z, 34, SP3_Vx, 34, SP3_Vy, 34, SP3_Vz, 34, SP3_Temperature, 34, SP3_Bx, 34, SP3_By, 34, SP3_Bz, 32, SP3_Br, 34, SP3_Bphi],
                  'BP1': [51, BP1_ID, 51, BP1_X, 51, BP1_Y, 51, BP1_Z, 51, BP1_Vx, 51, BP1_Vy, 51, BP1_Vz, 51, BP1_Temperature, 51, BP1_Bx, 51, BP1_By, 51, BP1_Bz, 51, BP1_Br, 51, BP1_Bphi],
                  'BP2': [68, BP2_ID, 68, BP2_X, 68, BP2_Y, 68, BP2_Z, 68, BP2_Vx, 68, BP2_Vy, 68, BP2_Vz, 68, BP2_Temperature, 68, BP2_Bx, 68, BP2_By, 68, BP2_Bz, 68, BP2_Br, 68, BP2_Bphi],
                  'BP3': [85, BP3_ID, 85, BP3_X, 85, BP3_Y, 85, BP3_Z, 85, BP3_Vx, 85, BP3_Vy, 85, BP3_Vz, 85, BP3_Temperature, 85, BP3_Bx, 85, BP3_By, 85, BP3_Bz, 85, BP3_Br, 85, BP3_Bphi],
                  'BP4': [102,BP4_ID, 102, BP4_X, 102, BP4_Y, 102, BP4_Z, 102, BP4_Vx, 102, BP4_Vy, 102, BP4_Vz, 102, BP4_Temperature, 102, BP4_Bx, 102, BP4_By, 102, BP4_Bz, 102, BP4_Br, 102, BP4_Bphi],
                  'BP5': [119, BP5_ID, 119, BP5_X, 119, BP5_Y, 119, BP5_Z, 119, BP5_Vx, 119, BP5_Vy, 119, BP5_Vz, 119, BP5_Temperature, 119, BP5_Bx, 119, BP5_By, 119, BP5_Bz, 119, BP5_Br, 119, BP5_Bphi]}

#difference of 17
    for hallprobe in hallprobes.keys():
        idsp1 =tdms_file[f'{groupname}']['HallProbes'].read_data()[15 + hallprobes[f'{hallprobe}'][0]]
        hallprobes[f'{hallprobe}'][1].append(idsp1.split(':')[1])
        sp1x =tdms_file[f'{groupname}']['HallProbes'].read_data()[12 +hallprobes[f'{hallprobe}'][2]]
        hallprobes[f'{hallprobe}'][3].append(sp1x.split(':')[1])
        sp1y =tdms_file[f'{groupname}']['HallProbes'].read_data()[11 + hallprobes[f'{hallprobe}'][4]]
        hallprobes[f'{hallprobe}'][5].append(sp1y.split(':')[1])
        sp1z =tdms_file[f'{groupname}']['HallProbes'].read_data()[10 +hallprobes[f'{hallprobe}'][6]]
        hallprobes[f'{hallprobe}'][7].append(sp1z.split(':')[1])
        sp1vx=tdms_file[f'{groupname}']['HallProbes'].read_data()[9 + hallprobes[f'{hallprobe}'][8]]
        hallprobes[f'{hallprobe}'][9].append(sp1vx.split(':')[1])
        sp1vy =tdms_file[f'{groupname}']['HallProbes'].read_data()[8 +hallprobes[f'{hallprobe}'][10]]
        hallprobes[f'{hallprobe}'][11].append(sp1vy.split(':')[1])
        sp1vz =tdms_file[f'{groupname}']['HallProbes'].read_data()[7 + hallprobes[f'{hallprobe}'][12]]
        hallprobes[f'{hallprobe}'][13].append(sp1vz.split(':')[1])
        sp1temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[1 + hallprobes[f'{hallprobe}'][14]]
        hallprobes[f'{hallprobe}'][15].append(sp1temp.split(':')[1])
        sp1bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[6 + hallprobes[f'{hallprobe}'][16]]
        hallprobes[f'{hallprobe}'][17].append(sp1bx.split(':')[1])
        sp1by = tdms_file[f'{groupname}']['HallProbes'].read_data()[5 + hallprobes[f'{hallprobe}'][18]]
        hallprobes[f'{hallprobe}'][19].append(sp1by.split(':')[1])
        sp1bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[2 + hallprobes[f'{hallprobe}'][20]]
        hallprobes[f'{hallprobe}'][21].append(sp1bz.split(':')[1])
        sp1br = tdms_file[f'{groupname}']['HallProbes'].read_data()[5 + hallprobes[f'{hallprobe}'][22]]
        hallprobes[f'{hallprobe}'][23].append(sp1br.split(':')[1])
        sp1bphi = tdms_file[f'{groupname}']['HallProbes'].read_data()[6 + hallprobes[f'{hallprobe}'][24]]
        hallprobes[f'{hallprobe}'][25].append(sp1bphi.split(':')[1])



#reflector lists
BP_A_rho = []
BP_B_rho = []
BP_C_rho = []
BP_D_rho = []
SP_A_rho = []
SP_B_rho = []
SP_C_rho = []
SP_D_rho = []

BP_A_theta = []
BP_B_theta = []
BP_C_theta = []
BP_D_theta = []
SP_A_theta = []
SP_B_theta = []
SP_C_theta = []
SP_D_theta = []

BP_A_z = []
BP_B_z = []
BP_C_z = []
BP_D_z = []
SP_A_z = []
SP_B_z = []
SP_C_z = []
SP_D_z = []


#write all the reflector columns
def write_reflector(groupname, tdms_file):
    reflectors = {'BP_A': [0, BP_A_rho, BP_A_theta, BP_A_z], 'BP_B': [6, BP_B_rho, BP_B_theta, BP_B_z],
                  'BP_C': [12, BP_C_rho, BP_C_theta, BP_C_z], 'BP_D':[18, BP_D_rho, BP_D_theta, BP_D_z]}
    reflectors2 = {'SP_A':[24, SP_A_rho, SP_A_theta, SP_A_z], 'SP_B':[30, SP_B_rho, SP_B_theta, SP_B_z],
                   'SP_C':[36, SP_C_rho, SP_C_theta, SP_C_z], 'SP_D':[42, SP_D_rho, SP_D_theta, SP_D_z]}


    for reflector in reflectors.keys():

        rho = tdms_file[f'{groupname}']['Measured Coordinates'].read_data()[5+ reflectors[f'{reflector}'][0]]
        reflectors[f'{reflector}'][1].append(rho.split(':')[1])
        theta = tdms_file[f'{groupname}']['Measured Coordinates'].read_data()[4+reflectors[f'{reflector}'][0]]
        reflectors[f'{reflector}'][2].append(theta.split(':')[1])
        z = tdms_file[f'{groupname}']['Measured Coordinates'].read_data()[3+reflectors[f'{reflector}'][0]]
        reflectors[f'{reflector}'][3].append(z.split(':')[1])

    for reflector in reflectors2.keys():
        rho = tdms_file[f'{groupname}']['Measured Coordinates'].read_data()[5+reflectors2[f'{reflector}'][0]]
        reflectors2[f'{reflector}'][1].append(rho.split(':')[1])
        theta = tdms_file[f'{groupname}']['Measured Coordinates'].read_data()[4+reflectors2[f'{reflector}'][0]]
        reflectors2[f'{reflector}'][2].append(theta.split(':')[1])
        z = tdms_file[f'{groupname}']['Measured Coordinates'].read_data()[3+reflectors2[f'{reflector}'][0]]
        reflectors2[f'{reflector}'][3].append(z.split(':')[1])



with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
    groups = tdms_file.groups()
    for group in groups:
        groupname = group.name
        groupnamelist.append(groupname)

    for groupname in groupnamelist:
        if groupname == 'run:R_2021' or groupname[2] == 'q':
            pass
        else:
            write_timestamp(groupname, tdms_file)
            write_stepID(groupname, tdms_file)
            write_mapper(groupname, tdms_file)
            write_NMR(groupname, tdms_file)
            write_HallProbe(groupname, tdms_file)
            write_reflector(groupname, tdms_file)




time_stamp_dict = {"TIMESTAMP": timestamp_values}
stepID_dict = {'StepID': stepid_values}
stepIDnumb_dict = {"StepIDinteger": stepidnumber_values}
mapperangle_dict = {"Mapper_Angle": mapperangle_values}
mapper_Z_dict = {"Mapper_Z": mapper_Z_values}
bnmr_dict = {"B_NMR": bnmr_values}

#HALL PROBE DICTIONARIES
idsp1_dict = {"HP_SP1_ID": SP1_ID}
sp1x_dict = {"HP_SP1_X": SP1_X}
sp1y_dict = {"HP_SP1_Y": SP1_Y}
sp1z_dict = {"HP_SP1_Z": SP1_Z}
sp1vx_dict = {"HP_SP1_Vx": SP1_Vx}
sp1vy_dict = {"HP_SP1_Vy": SP1_Vy}
sp1vz_dict = {"HP_SP1_Vz": SP1_Vz}
sp1temp_dict = {"HP_SP1_Temperature": SP1_Temperature}
sp1bx_dict = {"HP_SP1_Bx_Meas": SP1_Bx}
sp1by_dict = {"HP_SP1_By_Meas": SP1_By}
sp1bz_dict = {"HP_SP1_Bz_Meas": SP1_Bz}
sp1br_dict = {"HP_SP1_Br": SP1_Br}
sp1bphi_dict = {"HP_SP1_Bphi": SP1_Bphi}

idsp2_dict = {"HP_SP2_ID": SP2_ID}
sp2x_dict = {"HP_SP2_X": SP2_X}
sp2y_dict = {"HP_SP2_Y": SP2_Y}
sp2z_dict = {"HP_SP2_Z": SP2_Z}
sp2vx_dict = {"HP_SP2_Vx": SP2_Vx}
sp2vy_dict = {"HP_SP2_Vy": SP2_Vy}
sp2vz_dict = {"HP_SP2_Vz": SP2_Vz}
sp2temp_dict = {"HP_SP2_Temperature": SP2_Temperature}
sp2bx_dict = {"HP_SP2_Bx_Meas": SP2_Bx}
sp2by_dict = {"HP_SP2_By_Meas": SP2_By}
sp2bz_dict = {"HP_SP2_Bz_Meas": SP2_Bz}
sp2br_dict = {"HP_SP2_Br": SP2_Br}
sp2bphi_dict = {"HP_SP2_Bphi": SP2_Bphi}

idsp3_dict = {"HP_SP3_ID": SP3_ID}
sp3x_dict = {"HP_SP3_X": SP3_X}
sp3y_dict = {"HP_SP3_Y": SP3_Y}
sp3z_dict = {"HP_SP3_Z": SP3_Z}
sp3vx_dict = {"HP_SP3_Vx": SP3_Vx}
sp3vy_dict = {"HP_SP3_Vy": SP3_Vy}
sp3vz_dict = {"HP_SP3_Vz": SP3_Vz}
sp3temp_dict = {"HP_SP3_Temperature": SP3_Temperature}
sp3bx_dict = {"HP_SP3_Bx_Meas": SP3_Bx}
sp3by_dict = {"HP_SP3_By_Meas": SP3_By}
sp3bz_dict = {"HP_SP3_Bz_Meas": SP3_Bz}
sp3br_dict = {"HP_SP3_Br": SP3_Br}
sp3bphi_dict = {"HP_SP3_Bphi": SP3_Bphi}

idbp1_dict = {"HP_BP1_ID": BP1_ID}
bp1x_dict = {"HP_BP1_X": BP1_X}
bp1y_dict = {"HP_BP1_Y": BP1_Y}
bp1z_dict = {"HP_BP1_Z": BP1_Z}
bp1vx_dict = {"HP_BP1_Vx": BP1_Vx}
bp1vy_dict = {"HP_BP1_Vy": BP1_Vy}
bp1vz_dict = {"HP_BP1_Vz": BP1_Vz}
bp1temp_dict = {"HP_BP1_Temperature": BP1_Temperature}
bp1bx_dict = {"HP_BP1_Bx_Meas": BP1_Bx}
bp1by_dict = {"HP_BP1_By_Meas": BP1_By}
bp1bz_dict = {"HP_BP1_Bz_Meas": BP1_Bz}
bp1br_dict = {"HP_BP1_Br": BP1_Br}
bp1bphi_dict = {"HP_BP1_Bphi": BP1_Bphi}

idbp2_dict = {"HP_BP2_ID": BP2_ID}
bp2x_dict = {"HP_BP2_X": BP2_X}
bp2y_dict = {"HP_BP2_Y": BP2_Y}
bp2z_dict = {"HP_BP2_Z": BP2_Z}
bp2vx_dict = {"HP_BP2_Vx": BP2_Vx}
bp2vy_dict = {"HP_BP2_Vy": BP2_Vy}
bp2vz_dict = {"HP_BP2_Vz": BP2_Vz}
bp2temp_dict = {"HP_BP2_Temperature": BP2_Temperature}
bp2bx_dict = {"HP_BP2_Bx_Meas": BP2_Bx}
bp2by_dict = {"HP_BP2_By_Meas": BP2_By}
bp2bz_dict = {"HP_BP2_Bz_Meas": BP2_Bz}
bp2br_dict = {"HP_BP2_Br": BP2_Br}
bp2bphi_dict = {"HP_BP2_Bphi": BP2_Bphi}


idbp3_dict = {"HP_BP3_ID": BP3_ID}
bp3x_dict = {"HP_BP3_X": BP3_X}
bp3y_dict = {"HP_BP3_Y": BP3_Y}
bp3z_dict = {"HP_BP3_Z": BP3_Z}
bp3vx_dict = {"HP_BP3_Vx": BP3_Vx}
bp3vy_dict = {"HP_BP3_Vy": BP3_Vy}
bp3vz_dict = {"HP_BP3_Vz": BP3_Vz}
bp3temp_dict = {"HP_BP3_Temperature": BP3_Temperature}
bp3bx_dict = {"HP_BP3_Bx_Meas": BP3_Bx}
bp3by_dict = {"HP_BP3_By_Meas": BP3_By}
bp3bz_dict = {"HP_BP3_Bz_Meas": BP3_Bz}
bp3br_dict = {"HP_BP3_Br": BP3_Br}
bp3bphi_dict = {"HP_BP3_Bphi": BP3_Bphi}

idbp4_dict = {"HP_BP4_ID": BP4_ID}
bp4x_dict = {"HP_BP4_X": BP4_X}
bp4y_dict = {"HP_BP4_Y": BP4_Y}
bp4z_dict = {"HP_BP4_Z": BP4_Z}
bp4vx_dict = {"HP_BP4_Vx": BP4_Vx}
bp4vy_dict = {"HP_BP4_Vy": BP4_Vy}
bp4vz_dict = {"HP_BP4_Vz": BP4_Vz}
bp4temp_dict = {"HP_BP4_Temperature": BP4_Temperature}
bp4bx_dict = {"HP_BP4_Bx_Meas": BP4_Bx}
bp4by_dict = {"HP_BP4_By_Meas": BP4_By}
bp4bz_dict = {"HP_BP4_Bz_Meas": BP4_Bz}
bp4br_dict = {"HP_BP4_Br": BP4_Br}
bp4bphi_dict = {"HP_BP4_Bphi": BP4_Bphi}

idbp5_dict = {"HP_BP5_ID": BP5_ID}
bp5x_dict = {"HP_BP5_X": BP5_X}
bp5y_dict = {"HP_BP5_Y": BP5_Y}
bp5z_dict = {"HP_BP5_Z": BP5_Z}
bp5vx_dict = {"HP_BP5_Vx": BP5_Vx}
bp5vy_dict = {"HP_BP5_Vy": BP5_Vy}
bp5vz_dict = {"HP_BP5_Vz": BP5_Vz}
bp5temp_dict = {"HP_BP5_Temperature": BP5_Temperature}
bp5bx_dict = {"HP_BP5_Bx_Meas": BP5_Bx}
bp5by_dict = {"HP_BP5_By_Meas": BP5_By}
bp5bz_dict = {"HP_BP5_Bz_Meas": BP5_Bz}
bp5br_dict = {"HP_BP5_Br": BP5_Br}
bp5bphi_dict = {"HP_BP5_Bphi": BP5_Bphi}
#REFLECTOR DICTIONARIES

BP_A_rho_dict = {"Reflect_BP_A_rho": BP_A_rho}
BP_B_rho_dict = {"Reflect_BP_B_rho": BP_B_rho}
BP_C_rho_dict = {"Reflect_BP_C_rho": BP_C_rho}
BP_D_rho_dict = {"Reflect_BP_D_rho": BP_D_rho}
SP_A_rho_dict = {"Reflect_SP_A_rho": SP_A_rho}
SP_B_rho_dict = {"Reflect_SP_B_rho": SP_B_rho}
SP_C_rho_dict = {"Reflect_SP_C_rho": SP_C_rho}
SP_D_rho_dict = {"Reflect_SP_D_rho": SP_D_rho}

BP_A_theta_dict = {"Reflect_BP_A_theta": BP_A_theta}
BP_B_theta_dict = {"Reflect_BP_B_theta": BP_B_theta}
BP_C_theta_dict = {"Reflect_BP_C_theta": BP_B_theta}
BP_D_theta_dict = {"Reflect_BP_D_theta": BP_D_theta}
SP_A_theta_dict = {"Reflect_SP_A_theta": SP_A_theta}
SP_B_theta_dict = {"Reflect_SP_B_theta": SP_B_theta}
SP_C_theta_dict = {"Reflect_SP_C_theta": SP_C_theta}
SP_D_theta_dict = {"Reflect_SP_D_theta": SP_D_theta}

BP_A_z_dict = {"Reflect_BP_A_z": BP_A_z}
BP_B_z_dict = {"Reflect_BP_B_z": BP_B_z}
BP_C_z_dict = {"Reflect_BP_C_z": BP_C_z}
BP_D_z_dict = {"Reflect_BP_D_z": BP_D_z}
SP_A_z_dict = {"Reflect_SP_A_z": BP_A_z}
SP_B_z_dict = {"Reflect_SP_B_z": BP_B_z}
SP_C_z_dict = {"Reflect_SP_C_z": BP_C_z}
SP_D_z_dict = {"Reflect_SP_D_z": BP_D_z}
groupname= []

for value in groupnamelist:
    if value == 'run:R_2021' or value[2]=='q':
        pass
    else:
        groupname.append(value)

groupname_dict = {"Groupname": groupname}

dict = {}
for d in [time_stamp_dict, groupname_dict, stepID_dict, stepIDnumb_dict, mapperangle_dict, mapper_Z_dict, bnmr_dict,idsp1_dict,
          sp1x_dict, sp1y_dict, sp1z_dict,sp1vx_dict, sp1vy_dict, sp1vz_dict, sp1temp_dict, sp1bx_dict, sp1by_dict, sp1bz_dict, sp1br_dict, sp1bphi_dict,
          idsp2_dict, sp2x_dict, sp2y_dict,sp2z_dict, sp2vx_dict, sp2vy_dict, sp2vz_dict, sp2temp_dict, sp2bx_dict, sp2by_dict,
          sp2bz_dict, sp2br_dict, sp2bphi_dict, idsp3_dict, sp3x_dict,sp3y_dict, sp3z_dict, sp3vx_dict, sp3vy_dict, sp3vz_dict, sp3temp_dict, sp3bx_dict, sp3by_dict, sp3bz_dict, sp3br_dict, sp3bphi_dict, idbp1_dict, bp1x_dict,
          bp1y_dict, bp1z_dict, bp1vx_dict, bp1vy_dict, bp1vz_dict, bp1temp_dict, bp1bx_dict, bp1by_dict, bp1bz_dict, bp1br_dict, bp1bphi_dict,
          idbp2_dict, bp2x_dict,bp2y_dict, bp2z_dict, bp2vx_dict, bp2vy_dict, bp2vz_dict, bp2temp_dict, bp2bx_dict, bp2by_dict, bp2bz_dict, bp2br_dict, bp2bphi_dict,
          idbp3_dict, bp3x_dict, bp3y_dict, bp3z_dict, bp3vx_dict, bp3vy_dict, bp3vz_dict, bp3temp_dict, bp3bx_dict, bp3by_dict, bp3bz_dict, bp3br_dict, bp3bphi_dict,
          idbp4_dict, bp4x_dict, bp4y_dict, bp4z_dict, bp4vx_dict, bp4vy_dict, bp4vz_dict, bp4temp_dict, bp4bx_dict,bp4by_dict, bp4bz_dict,bp4br_dict, bp4bphi_dict,
          idbp5_dict, bp5x_dict, bp5y_dict, bp5z_dict, bp5vx_dict, bp5vy_dict, bp5vz_dict, bp5temp_dict, bp5bx_dict,
          bp5by_dict, bp5bz_dict,bp5br_dict, bp5bphi_dict, BP_A_rho_dict, BP_A_theta_dict, BP_A_z_dict, BP_B_rho_dict, BP_B_theta_dict, BP_B_z_dict, BP_C_rho_dict, BP_C_theta_dict, BP_C_z_dict,
    BP_D_rho_dict, BP_D_theta_dict, BP_D_z_dict, SP_A_rho_dict, SP_A_theta_dict, SP_A_z_dict, SP_B_rho_dict, SP_B_theta_dict, SP_B_z_dict, SP_C_rho_dict, SP_C_theta_dict, SP_C_z_dict,
    SP_D_theta_dict, SP_D_rho_dict, SP_D_z_dict
          ]:
  dict.update(d)



#Creating the dataframe
dataframe = pd.DataFrame(data=dict)
# index=groupname

#Convert to floats from strings, do not convert if timestamp or ID
for key in dict.keys():
    if key == 'TIMESTAMP' or key[-3:] == '_ID' or key == 'Groupname':
        pass
    else:
        dataframe[f'{key}'] = dataframe[f'{key}'].astype(str).astype(float)

#write to datatime
pd.to_datetime(dataframe['TIMESTAMP'],format= '%m/%d/%Y %I:%M:%S %p' )



#dump into pickle
with open("/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/8-9.pkl", 'wb') as f:
    pickle.dump(dataframe, f)

