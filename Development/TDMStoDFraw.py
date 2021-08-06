import pandas as pd
from nptdms import TdmsFile
import pickle

#Edits will be made to clean this up!!  yes it is not concise at the moment

tdms_file = TdmsFile.read("../data/TestDataV2.tdms")
groups = tdms_file.groups()


#Bunch of lists
groupnamelist = []
timestamp_values = []
stepid_values = []
stepidnumber_values = []
mapperangle_values = []
mapper_Z_values = []
bnmr_values = []

idsp1_values = []
sp1x_values = []
sp1y_values = []
sp1z_values = []
sp1vx_values = []
sp1vy_values = []
sp1vz_values = []
sp1temp_values = []
sp1bx_values = []
sp1by_values = []
sp1bz_values = []

idsp2_values = []
sp2x_values = []
sp2y_values = []
sp2z_values = []
sp2vx_values = []
sp2vy_values = []
sp2vz_values = []
sp2temp_values = []
sp2bx_values = []
sp2by_values = []
sp2bz_values = []

idsp3_values = []
sp3x_values = []
sp3y_values = []
sp3z_values = []
sp3vx_values = []
sp3vy_values = []
sp3vz_values = []
sp3temp_values = []
sp3bx_values = []
sp3by_values = []
sp3bz_values = []

idbp1_values = []
bp1x_values = []
bp1y_values = []
bp1z_values = []
bp1vx_values = []
bp1vy_values = []
bp1vz_values = []
bp1temp_values = []
bp1bx_values = []
bp1by_values = []
bp1bz_values = []

idbp2_values = []
bp2x_values = []
bp2y_values = []
bp2z_values = []
bp2vx_values = []
bp2vy_values = []
bp2vz_values = []
bp2temp_values = []
bp2bx_values = []
bp2by_values = []
bp2bz_values = []

idbp3_values = []
bp3x_values = []
bp3y_values = []
bp3z_values = []
bp3vx_values = []
bp3vy_values = []
bp3vz_values = []
bp3temp_values = []
bp3bx_values = []
bp3by_values = []
bp3bz_values = []

idbp4_values = []
bp4x_values = []
bp4y_values = []
bp4z_values = []
bp4vx_values = []
bp4vy_values = []
bp4vz_values = []
bp4temp_values = []
bp4bx_values = []
bp4by_values = []
bp4bz_values = []

idbp5_values = []
bp5x_values = []
bp5y_values = []
bp5z_values = []
bp5vx_values = []
bp5vy_values = []
bp5vz_values = []
bp5temp_values = []
bp5bx_values = []
bp5by_values = []
bp5bz_values = []

#add groupnames to group name list
for group in groups:
    groupname = group.name
    groupnamelist.append(groupname)

#do timestamp columns
def write_timestamp(groupname, tdms_file):
    timestamp = tdms_file[f'{groupname}']['Timestamp'].read_data()[0]
    lineelements = timestamp.split(':')
    if lineelements[0] == 'Timestamp':
        column_value = lineelements[1]+ ':'+ lineelements[2]
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
def write_HallProbe(groupname, tdms_file):
    idsp1 =tdms_file[f'{groupname}']['HallProbes'].read_data()[13]
    idsp1_values.append(idsp1.split(':')[1])
    sp1x =tdms_file[f'{groupname}']['HallProbes'].read_data()[10]
    sp1x_values.append(sp1x.split(':')[1])
    sp1y =tdms_file[f'{groupname}']['HallProbes'].read_data()[9]
    sp1y_values.append(sp1y.split(':')[1])
    sp1z =tdms_file[f'{groupname}']['HallProbes'].read_data()[8]
    sp1z_values.append(sp1z.split(':')[1])
    sp1vx=tdms_file[f'{groupname}']['HallProbes'].read_data()[7]
    sp1vx_values.append(sp1vx.split(':')[1])
    sp1vy =tdms_file[f'{groupname}']['HallProbes'].read_data()[6]
    sp1vy_values.append(sp1vy.split(':')[1])
    sp1vz =tdms_file[f'{groupname}']['HallProbes'].read_data()[5]
    sp1vz_values.append(sp1vz.split(':')[1])
    sp1temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[1]
    sp1temp_values.append(sp1temp.split(':')[1])
    sp1bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[4]
    sp1bx_values.append(sp1bx.split(':')[1])
    sp1by = tdms_file[f'{groupname}']['HallProbes'].read_data()[3]
    sp1by_values.append(sp1by.split(':')[1])
    sp1bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[5]
    sp1bz_values.append(sp1bz.split(':')[1])

    idsp2 =tdms_file[f'{groupname}']['HallProbes'].read_data()[28]
    idsp2_values.append(idsp2.split(':')[1])
    sp2x =tdms_file[f'{groupname}']['HallProbes'].read_data()[25]
    sp2x_values.append(sp2x.split(':')[1])
    sp2y =tdms_file[f'{groupname}']['HallProbes'].read_data()[24]
    sp2y_values.append(sp2y.split(':')[1])
    sp2z =tdms_file[f'{groupname}']['HallProbes'].read_data()[23]
    sp2z_values.append(sp2z.split(':')[1])
    sp2vx=tdms_file[f'{groupname}']['HallProbes'].read_data()[22]
    sp2vx_values.append(sp2vx.split(':')[1])
    sp2vy =tdms_file[f'{groupname}']['HallProbes'].read_data()[21]
    sp2vy_values.append(sp2vy.split(':')[1])
    sp2vz =tdms_file[f'{groupname}']['HallProbes'].read_data()[20]
    sp2vz_values.append(sp2vz.split(':')[1])
    sp2temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[16]
    sp2temp_values.append(sp2temp.split(':')[1])
    sp2bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[19]
    sp2bx_values.append(sp2bx.split(':')[1])
    sp2by = tdms_file[f'{groupname}']['HallProbes'].read_data()[18]
    sp2by_values.append(sp2by.split(':')[1])
    sp2bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[17]
    sp2bz_values.append(sp2bz.split(':')[1])

    idsp3 =tdms_file[f'{groupname}']['HallProbes'].read_data()[43]
    idsp3_values.append(idsp3.split(':')[1])
    sp3x =tdms_file[f'{groupname}']['HallProbes'].read_data()[40]
    sp3x_values.append(sp3x.split(':')[1])
    sp3y =tdms_file[f'{groupname}']['HallProbes'].read_data()[39]
    sp3y_values.append(sp3y.split(':')[1])
    sp3z =tdms_file[f'{groupname}']['HallProbes'].read_data()[38]
    sp3z_values.append(sp3z.split(':')[1])
    sp3vx=tdms_file[f'{groupname}']['HallProbes'].read_data()[37]
    sp3vx_values.append(sp3vx.split(':')[1])
    sp3vy =tdms_file[f'{groupname}']['HallProbes'].read_data()[36]
    sp3vy_values.append(sp3vy.split(':')[1])
    sp3vz =tdms_file[f'{groupname}']['HallProbes'].read_data()[35]
    sp3vz_values.append(sp3vz.split(':')[1])
    sp3temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[31]
    sp3temp_values.append(sp3temp.split(':')[1])
    sp3bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[34]
    sp3bx_values.append(sp3bx.split(':')[1])
    sp3by = tdms_file[f'{groupname}']['HallProbes'].read_data()[33]
    sp3by_values.append(sp3by.split(':')[1])
    sp3bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[32]
    sp3bz_values.append(sp3bz.split(':')[1])

    idbp1 =tdms_file[f'{groupname}']['HallProbes'].read_data()[58]
    idbp1_values.append(idbp1.split(':')[1])
    bp1x =tdms_file[f'{groupname}']['HallProbes'].read_data()[55]
    bp1x_values.append(bp1x.split(':')[1])
    bp1y =tdms_file[f'{groupname}']['HallProbes'].read_data()[54]
    bp1y_values.append(bp1y.split(':')[1])
    bp1z =tdms_file[f'{groupname}']['HallProbes'].read_data()[53]
    bp1z_values.append(bp1z.split(':')[1])
    bp1vx=tdms_file[f'{groupname}']['HallProbes'].read_data()[52]
    bp1vx_values.append(bp1vx.split(':')[1])
    bp1vy =tdms_file[f'{groupname}']['HallProbes'].read_data()[51]
    bp1vy_values.append(bp1vy.split(':')[1])
    bp1vz =tdms_file[f'{groupname}']['HallProbes'].read_data()[50]
    bp1vz_values.append(bp1vz.split(':')[1])
    bp1temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[46]
    bp1temp_values.append(bp1temp.split(':')[1])
    bp1bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[49]
    bp1bx_values.append(bp1bx.split(':')[1])
    bp1by = tdms_file[f'{groupname}']['HallProbes'].read_data()[48]
    bp1by_values.append(bp1by.split(':')[1])
    bp1bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[47]
    bp1bz_values.append(bp1bz.split(':')[1])

    idbp2 =tdms_file[f'{groupname}']['HallProbes'].read_data()[73]
    idbp2_values.append(idbp2.split(':')[1])
    bp2x =tdms_file[f'{groupname}']['HallProbes'].read_data()[70]
    bp2x_values.append(bp2x.split(':')[1])
    bp2y =tdms_file[f'{groupname}']['HallProbes'].read_data()[69]
    bp2y_values.append(bp2y.split(':')[1])
    bp2z =tdms_file[f'{groupname}']['HallProbes'].read_data()[68]
    bp2z_values.append(bp2z.split(':')[1])
    bp2vx=tdms_file[f'{groupname}']['HallProbes'].read_data()[67]
    bp2vx_values.append(bp2vx.split(':')[1])
    bp2vy =tdms_file[f'{groupname}']['HallProbes'].read_data()[66]
    bp2vy_values.append(bp2vy.split(':')[1])
    bp2vz =tdms_file[f'{groupname}']['HallProbes'].read_data()[65]
    bp2vz_values.append(bp2vz.split(':')[1])
    bp2temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[61]
    bp2temp_values.append(bp2temp.split(':')[1])
    bp2bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[64]
    bp2bx_values.append(bp2bx.split(':')[1])
    bp2by = tdms_file[f'{groupname}']['HallProbes'].read_data()[63]
    bp2by_values.append(bp2by.split(':')[1])
    bp2bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[62]
    bp2bz_values.append(bp2bz.split(':')[1])

    idbp3 = tdms_file[f'{groupname}']['HallProbes'].read_data()[88]
    idbp3_values.append(idbp3.split(':')[1])
    bp3x = tdms_file[f'{groupname}']['HallProbes'].read_data()[85]
    bp3x_values.append(bp3x.split(':')[1])
    bp3y = tdms_file[f'{groupname}']['HallProbes'].read_data()[84]
    bp3y_values.append(bp3y.split(':')[1])
    bp3z = tdms_file[f'{groupname}']['HallProbes'].read_data()[83]
    bp3z_values.append(bp3z.split(':')[1])
    bp3vx = tdms_file[f'{groupname}']['HallProbes'].read_data()[82]
    bp3vx_values.append(bp3vx.split(':')[1])
    bp3vy = tdms_file[f'{groupname}']['HallProbes'].read_data()[81]
    bp3vy_values.append(bp3vy.split(':')[1])
    bp3vz = tdms_file[f'{groupname}']['HallProbes'].read_data()[80]
    bp3vz_values.append(bp3vz.split(':')[1])
    bp3temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[76]
    bp3temp_values.append(bp3temp.split(':')[1])
    bp3bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[79]
    bp3bx_values.append(bp3bx.split(':')[1])
    bp3by = tdms_file[f'{groupname}']['HallProbes'].read_data()[78]
    bp3by_values.append(bp3by.split(':')[1])
    bp3bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[77]
    bp3bz_values.append(bp3bz.split(':')[1])

    idbp4 = tdms_file[f'{groupname}']['HallProbes'].read_data()[103]
    idbp4_values.append(idbp4.split(':')[1])
    bp4x = tdms_file[f'{groupname}']['HallProbes'].read_data()[100]
    bp4x_values.append(bp4x.split(':')[1])
    bp4y = tdms_file[f'{groupname}']['HallProbes'].read_data()[99]
    bp4y_values.append(bp4y.split(':')[1])
    bp4z = tdms_file[f'{groupname}']['HallProbes'].read_data()[98]
    bp4z_values.append(bp4z.split(':')[1])
    bp4vx = tdms_file[f'{groupname}']['HallProbes'].read_data()[97]
    bp4vx_values.append(bp4vx.split(':')[1])
    bp4vy = tdms_file[f'{groupname}']['HallProbes'].read_data()[96]
    bp4vy_values.append(bp4vy.split(':')[1])
    bp4vz = tdms_file[f'{groupname}']['HallProbes'].read_data()[95]
    bp4vz_values.append(bp4vz.split(':')[1])
    bp4temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[91]
    bp4temp_values.append(bp4temp.split(':')[1])
    bp4bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[94]
    bp4bx_values.append(bp4bx.split(':')[1])
    bp4by = tdms_file[f'{groupname}']['HallProbes'].read_data()[93]
    bp4by_values.append(bp4by.split(':')[1])
    bp4bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[92]
    bp4bz_values.append(bp4bz.split(':')[1])

    idbp5 = tdms_file[f'{groupname}']['HallProbes'].read_data()[118]
    idbp5_values.append(idbp5.split(':')[1])
    bp5x = tdms_file[f'{groupname}']['HallProbes'].read_data()[115]
    bp5x_values.append(bp5x.split(':')[1])
    bp5y = tdms_file[f'{groupname}']['HallProbes'].read_data()[114]
    bp5y_values.append(bp5y.split(':')[1])
    bp5z = tdms_file[f'{groupname}']['HallProbes'].read_data()[113]
    bp5z_values.append(bp5z.split(':')[1])
    bp5vx = tdms_file[f'{groupname}']['HallProbes'].read_data()[112]
    bp5vx_values.append(bp5vx.split(':')[1])
    bp5vy = tdms_file[f'{groupname}']['HallProbes'].read_data()[111]
    bp5vy_values.append(bp5vy.split(':')[1])
    bp5vz = tdms_file[f'{groupname}']['HallProbes'].read_data()[110]
    bp5vz_values.append(bp5vz.split(':')[1])
    bp5temp = tdms_file[f'{groupname}']['HallProbes'].read_data()[106]
    bp5temp_values.append(bp5temp.split(':')[1])
    bp5bx = tdms_file[f'{groupname}']['HallProbes'].read_data()[109]
    bp5bx_values.append(bp5bx.split(':')[1])
    bp5by = tdms_file[f'{groupname}']['HallProbes'].read_data()[108]
    bp5by_values.append(bp5by.split(':')[1])
    bp5bz = tdms_file[f'{groupname}']['HallProbes'].read_data()[107]
    bp5bz_values.append(bp5bz.split(':')[1])

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
idsp1_dict = {"HP_SP1_ID": idsp1_values}
sp1x_dict = {"HP_SP1_X": sp1x_values}
sp1y_dict = {"HP_SP1_Y": sp1y_values}
sp1z_dict = {"HP_SP1_Z": sp1z_values}
sp1vx_dict = {"HP_SP1_Vx": sp1vx_values}
sp1vy_dict = {"HP_SP1_Vy": sp1vy_values}
sp1vz_dict = {"HP_SP1_Vz": sp1vz_values}
sp1temp_dict = {"HP_SP1_Temperature": sp1temp_values}
sp1bx_dict = {"HP_SP1_Bx_Meas": sp1bx_values}
sp1by_dict = {"HP_SP1_By_Meas": sp1by_values}
sp1bz_dict = {"HP_SP1_Bz_Meas": sp1bz_values}

idsp2_dict = {"HP_SP2_ID": idsp2_values}
sp2x_dict = {"HP_SP2_X": sp2x_values}
sp2y_dict = {"HP_SP2_Y": sp2y_values}
sp2z_dict = {"HP_SP2_Z": sp2z_values}
sp2vx_dict = {"HP_SP2_Vx": sp2vx_values}
sp2vy_dict = {"HP_SP2_Vy": sp2vy_values}
sp2vz_dict = {"HP_SP2_Vz": sp2vz_values}
sp2temp_dict = {"HP_SP2_Temperature": sp2temp_values}
sp2bx_dict = {"HP_SP2_Bx_Meas": sp2bx_values}
sp2by_dict = {"HP_SP2_By_Meas": sp2by_values}
sp2bz_dict = {"HP_SP2_Bz_Meas": sp2bz_values}

idsp3_dict = {"HP_SP3_ID": idsp3_values}
sp3x_dict = {"HP_SP3_X": sp3x_values}
sp3y_dict = {"HP_SP3_Y": sp3y_values}
sp3z_dict = {"HP_SP3_Z": sp3z_values}
sp3vx_dict = {"HP_SP3_Vx": sp3vx_values}
sp3vy_dict = {"HP_SP3_Vy": sp3vy_values}
sp3vz_dict = {"HP_SP3_Vz": sp3vz_values}
sp3temp_dict = {"HP_SP3_Temperature": sp3temp_values}
sp3bx_dict = {"HP_SP3_Bx_Meas": sp3bx_values}
sp3by_dict = {"HP_SP3_By_Meas": sp3by_values}
sp3bz_dict = {"HP_SP3_Bz_Meas": sp3bz_values}

idbp1_dict = {"HP_BP1_ID": idbp1_values}
bp1x_dict = {"HP_BP1_X": bp1x_values}
bp1y_dict = {"HP_BP1_Y": bp1y_values}
bp1z_dict = {"HP_BP1_Z": bp1z_values}
bp1vx_dict = {"HP_BP1_Vx": bp1vx_values}
bp1vy_dict = {"HP_BP1_Vy": bp1vy_values}
bp1vz_dict = {"HP_BP1_Vz": bp1vz_values}
bp1temp_dict = {"HP_BP1_Temperature": bp1temp_values}
bp1bx_dict = {"HP_BP1_Bx_Meas": bp1bx_values}
bp1by_dict = {"HP_BP1_By_Meas": bp1by_values}
bp1bz_dict = {"HP_BP1_Bz_Meas": bp1bz_values}

idbp2_dict = {"HP_BP2_ID": idbp2_values}
bp2x_dict = {"HP_BP2_X": bp2x_values}
bp2y_dict = {"HP_BP2_Y": bp2y_values}
bp2z_dict = {"HP_BP2_Z": bp2z_values}
bp2vx_dict = {"HP_BP2_Vx": bp2vx_values}
bp2vy_dict = {"HP_BP2_Vy": bp2vy_values}
bp2vz_dict = {"HP_BP2_Vz": bp2vz_values}
bp2temp_dict = {"HP_BP2_Temperature": bp2temp_values}
bp2bx_dict = {"HP_BP2_Bx_Meas": bp2bx_values}
bp2by_dict = {"HP_BP2_By_Meas": bp2by_values}
bp2bz_dict = {"HP_BP2_Bz_Meas": bp2bz_values}

idbp3_dict = {"HP_BP3_ID": idbp3_values}
bp3x_dict = {"HP_BP3_X": bp3x_values}
bp3y_dict = {"HP_BP3_Y": bp3y_values}
bp3z_dict = {"HP_BP3_Z": bp3z_values}
bp3vx_dict = {"HP_BP3_Vx": bp3vx_values}
bp3vy_dict = {"HP_BP3_Vy": bp3vy_values}
bp3vz_dict = {"HP_BP3_Vz": bp3vz_values}
bp3temp_dict = {"HP_BP3_Temperature": bp3temp_values}
bp3bx_dict = {"HP_BP3_Bx_Meas": bp3bx_values}
bp3by_dict = {"HP_BP3_By_Meas": bp3by_values}
bp3bz_dict = {"HP_BP3_Bz_Meas": bp3bz_values}

idbp4_dict = {"HP_BP4_ID": idbp4_values}
bp4x_dict = {"HP_BP4_X": bp4x_values}
bp4y_dict = {"HP_BP4_Y": bp4y_values}
bp4z_dict = {"HP_BP4_Z": bp4z_values}
bp4vx_dict = {"HP_BP4_Vx": bp4vx_values}
bp4vy_dict = {"HP_BP4_Vy": bp4vy_values}
bp4vz_dict = {"HP_BP4_Vz": bp4vz_values}
bp4temp_dict = {"HP_BP4_Temperature": bp4temp_values}
bp4bx_dict = {"HP_BP4_Bx_Meas": bp4bx_values}
bp4by_dict = {"HP_BP4_By_Meas": bp4by_values}
bp4bz_dict = {"HP_BP4_Bz_Meas": bp4bz_values}

idbp5_dict = {"HP_BP5_ID": idbp5_values}
bp5x_dict = {"HP_BP5_X": bp5x_values}
bp5y_dict = {"HP_BP5_Y": bp5y_values}
bp5z_dict = {"HP_BP5_Z": bp5z_values}
bp5vx_dict = {"HP_BP5_Vx": bp5vx_values}
bp5vy_dict = {"HP_BP5_Vy": bp5vy_values}
bp5vz_dict = {"HP_BP5_Vz": bp5vz_values}
bp5temp_dict = {"HP_BP5_Temperature": bp5temp_values}
bp5bx_dict = {"HP_BP5_Bx_Meas": bp5bx_values}
bp5by_dict = {"HP_BP5_By_Meas": bp5by_values}
bp5bz_dict = {"HP_BP5_Bz_Meas": bp5bz_values}

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

dict = {}
for d in [time_stamp_dict, stepID_dict, stepIDnumb_dict, mapperangle_dict, mapper_Z_dict, bnmr_dict,idsp1_dict,
          sp1x_dict, sp1y_dict, sp1z_dict,sp1vx_dict, sp1vy_dict, sp1vz_dict, sp1temp_dict, sp1bx_dict, sp1by_dict, sp1bz_dict,
          idsp2_dict, sp2x_dict, sp2y_dict,sp2z_dict, sp2vx_dict, sp2vy_dict, sp2vz_dict, sp2temp_dict, sp2bx_dict, sp2by_dict,
          sp2bz_dict, idsp3_dict, sp3x_dict,sp3y_dict, sp3z_dict, sp3vx_dict, sp3vy_dict, sp3vz_dict, sp3temp_dict, sp3bx_dict, sp3by_dict, sp3bz_dict, idbp1_dict, bp1x_dict,
          bp1y_dict, bp1z_dict, bp1vx_dict, bp1vy_dict, bp1vz_dict, bp1temp_dict, bp1bx_dict, bp1by_dict, bp1bz_dict,
          idbp2_dict, bp2x_dict,bp2y_dict, bp2z_dict, bp2vx_dict, bp2vy_dict, bp2vz_dict, bp2temp_dict, bp2bx_dict, bp2by_dict, bp2bz_dict,
          idbp3_dict, bp3x_dict, bp3y_dict, bp3z_dict, bp3vx_dict, bp3vy_dict, bp3vz_dict, bp3temp_dict, bp3bx_dict, bp3by_dict, bp3bz_dict,
          idbp4_dict, bp4x_dict, bp4y_dict, bp4z_dict, bp4vx_dict, bp4vy_dict, bp4vz_dict, bp4temp_dict, bp4bx_dict,bp4by_dict, bp4bz_dict,
          idbp5_dict, bp5x_dict, bp5y_dict, bp5z_dict, bp5vx_dict, bp5vy_dict, bp5vz_dict, bp5temp_dict, bp5bx_dict,
          bp5by_dict, bp5bz_dict,BP_A_rho_dict, BP_A_theta_dict, BP_A_z_dict, BP_B_rho_dict, BP_B_theta_dict, BP_B_z_dict, BP_C_rho_dict, BP_C_theta_dict, BP_C_z_dict,
    BP_D_rho_dict, BP_D_theta_dict, BP_D_z_dict, SP_A_rho_dict, SP_A_theta_dict, SP_A_z_dict, SP_B_rho_dict, SP_B_theta_dict, SP_B_z_dict, SP_C_rho_dict, SP_C_theta_dict, SP_C_z_dict,
    SP_D_theta_dict, SP_D_rho_dict, SP_D_z_dict
          ]:
  dict.update(d)

groupname= []

for value in groupnamelist:
    if value == 'run:R_2021' or value[2]=='q':
        pass
    else:
        groupname.append(value)

#Creating the dataframe
dataframe = pd.DataFrame(data=dict, index=groupname)

#Convert to floats from strings, do not convert if timestamp or ID
for key in dict.keys():
    if key == 'TIMESTAMP' or key[-3:] == '_ID':
        pass
    else:
        dataframe[f'{key}'] = dataframe[f'{key}'].astype(str).astype(float)

#write to datatime
pd.to_datetime(dataframe['TIMESTAMP'])

#dump into pickle
with open("/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/Newpickle.pkl", 'wb') as f:
    pickle.dump(dataframe, f)
