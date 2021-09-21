#Script for Test_Data_File_v3 to TDMS test fileimport pandas as pdimport numpy as npfrom nptdms import TdmsWriter, GroupObject, ChannelObjectimport osfrom datetime import datetimeimport timedef write_NMR(index, dataframe, step):    ProbeName = "NMR"    ProbeID = "Metrolab Technology SA,PT2026,25,elC2D1B2-arm1.21-dsp2.8-cpld1.9-pa3.7-opt00000000\n"    Status = "OK"    timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[index], '%Y-%m-%d %H:%M:%S')    Timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')    Fluxdensity = (dataframe['B_NMR'].iloc[index]).round(6)    NMR_array = np.array([f"ProbeName:{ProbeName}", f"ProbeID:{ProbeID}", f"FluxDensity:{Fluxdensity}",                          f"Status:{Status}", f"Timestamp:{Timestamp}"])    NMRchannel = ChannelObject(f'{step}','NMRProbe', NMR_array)    return NMRchanneldef write_Hall(index, dataframe, step):    names = ['SP1', 'SP2', 'SP3', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5']    def find_values(index,dataframe,name):        address = ''        temp = (dataframe[f'HP_{name}_Temperature'].iloc[index]).round(6)        Z_field = (dataframe[f'HP_{name}_Bz_Meas'].iloc[index]).round(6)        Y_field = (dataframe[f'HP_{name}_By_Meas'].iloc[index]).round(6)        X_field = (dataframe[f'HP_{name}_Bx_Meas'].iloc[index]).round(6)        Br_field =(dataframe[f'HP_{name}_Br'].iloc[index]).round(6)        Bphi_field = (dataframe[f'HP_{name}_Bphi'].loc[index]).round(6)        Bz = (dataframe[f'HP_{name}_Bz'].loc[index]).round(6)        Z_volt = (dataframe[f'HP_{name}_Vz'].iloc[index]).round(6)        Y_volt = (dataframe[f'HP_{name}_Vy'].iloc[index]).round(6)        X_volt = (dataframe[f'HP_{name}_Vx'].iloc[index]).round(6)        Z_location = (dataframe[f'HP_{name}_Z'].iloc[index]).round(6)        Y_location = (dataframe[f'HP_{name}_Y'].iloc[index]).round(6)        X_location = (dataframe[f'HP_{name}_X'].iloc[index]).round(6)        status = 'OK'        Sensorname = f'{name}'        SensorID = dataframe[f'HP_{name}_ID'].iloc[index]        timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[index], '%Y-%m-%d %H:%M:%S')        Timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')        array = np.array([f'Address:{address}', f'Temperature:{temp}', f'Z.field:{Z_field}',                           f'Y.field:{Y_field}', f'X.field:{X_field}',                          f'Br.field:{Br_field}', f'Bphi.field:{Bphi_field}', f'Bz:{Bz}',                          f'Z.volt:{Z_volt}', f'Y.volt:{Y_volt}', f'X.volt:{X_volt}', f'Z.location:{Z_location}',                          f'Y.location:{Y_location}', f'X.location:{X_location}', f'Status:{status}',                           f'Sensor.name:{Sensorname}', f'Sensor.ID:{SensorID}', f'Timestamp:{Timestamp}'])        return array    list_of_halls = np.array([])    for name in names:        x = find_values(index, dataframe, name)        list_of_halls = np.append(list_of_halls, x)    HALLchannel = ChannelObject(f'{step}', 'HallProbes', list_of_halls)    return HALLchanneldef write_Timestamp(index, dataframe, step):    timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[index], '%Y-%m-%d %H:%M:%S')    timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')    Timestamp_array = np.array([f'Timestamp:{timestamp}'])    Timestampchannel = ChannelObject(f'{step}', 'Timestamp', Timestamp_array)    return Timestampchanneldef write_Mapper(index,dataframe, step):    timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[index], '%Y-%m-%d %H:%M:%S')    timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')    requestedangle = (dataframe['Mapper_Angle'].iloc[index]).round(6)    home = ''    angle = (dataframe['Mapper_Angle'].iloc[index]).round(6)    mapperposition = (dataframe['Mapper_Z'].iloc[index]).round(6)    Mapper_array = np.array([f'Timestamp:{timestamp}', f'RequestedAngle:{requestedangle}', f'Home:{home}',                             f'Angle:{angle}', f'Position:{mapperposition}'])    Mapperchannel = ChannelObject(f'{step}','Mapper',Mapper_array)    return Mapperchanneldef write_Current(index, dataframe, step):    timestamp = ''    requestedcurrent = '0.000000'    PS_current = dataframe['PS_Current'].iloc[index]    DS_current = dataframe['DS_Current'].loc[index]    TS_current = dataframe['TS_Current'].loc[index]    Current_array = np.array([f'Timestamp:{timestamp}', f'RequestedCurrent:{requestedcurrent}', f'PS_Current:{PS_current}', f'DS_Current:{DS_current}', f'TS_Current:{TS_current}'])    Currentchannel = ChannelObject(f'{step}', 'Current', Current_array)    return Currentchanneldef write_QC(index, dataframe, step):    item1 = ''    item2 = ''    QC_array = np.array([f'{item1}', f'{item2}'])    QCchannel = ChannelObject(f'{step}', 'QC', QC_array)    return QCchanneldef write_stepID(index, dataframe, step):    groupid = dataframe['GroupID'].iloc[index]    Step_array = np.array([f'{groupid}'])    StepIDchannel = ChannelObject(f'{step}', 'StepID', Step_array)    return StepIDchanneldef write_reflector(index, dataframe, reflector):    usercoords = ''    status = 'None'    reflectorid = f'{reflector}'    z = (dataframe[f'Reflect_{reflector}_z'].loc[index]).round(6)    theta = (dataframe[f'Reflect_{reflector}_theta'].loc[index]).round(6)    rho = (dataframe[f'Reflect_{reflector}_rho'].loc[index]).round(6)    array = np.array([f'Reflector User Coordinates:{usercoords}', f'Status:{status}', f'Reflector ID:{reflectorid}',                        f'z (mm):{z}', f'theta (rad):{theta}', f'rho (mm):{rho}'])    return arraydef write_measuredcoordinates(index, dataframe, step):    reflectors = ['BP_A', 'BP_B', 'BP_C', 'BP_D']    reflectors2 = ['SP_A', 'SP_B', 'SP_C', 'SP_D']    reflector_array = np.array([])    for reflector in reflectors:        x = write_reflector(index, dataframe, reflector)        reflector_array = np.append(reflector_array, x)    for reflector in reflectors2:        x = write_reflector(index, dataframe, reflector)        reflector_array = np.append(reflector_array, x)    MeasReflectorchannel = ChannelObject(f'{step}', 'Measured Coordinates', reflector_array)    return MeasReflectorchanneldef write_predictedcoordinates(index, dataframe, step):    reflectors = ['BP_A', 'BP_B', 'BP_C', 'BP_D']    reflectors2 = ['SP_A', 'SP_B', 'SP_C', 'SP_D']    reflector_array = np.array([])    for reflector in reflectors:        x = write_reflector(index, dataframe, reflector)        reflector_array = np.append(reflector_array, x)    for reflector in reflectors2:        x = write_reflector(index, dataframe, reflector)        reflector_array = np.append(reflector_array, x)    PredictedReflectorchannel = ChannelObject(f'{step}', 'Predicted Coordinates', reflector_array)    return PredictedReflectorchanneldef write_group(index, dataframe, step, tdms_writer):    timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[index], '%Y-%m-%d %H:%M:%S')    timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')    group = GroupObject(f"{step}", properties={        "name": "FMSSystemTest_v3",        "Time": f"{timestamp}", })    wholegroup = tdms_writer.write_segment(        [group, write_Timestamp(index, dataframe, step), write_stepID(index, dataframe, step), write_NMR(index, dataframe, step),         write_Hall(index, dataframe, step),         write_Mapper(index, dataframe, step),         write_Current(index, dataframe, step),         write_QC(index, dataframe, step), write_measuredcoordinates(index, dataframe, step),         write_predictedcoordinates(index, dataframe, step)])    return wholegroupdef write_ID(dataframe):    id = 'R_2021'    id_array = np.array([f'{id}'])    IDchannel = ChannelObject('run:R_2021', 'ID', id_array)    return IDchanneldef write_Time(dataframe):    timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[0], '%Y-%m-%d %H:%M:%S')    timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')    time_array = np.array([f'{timestamp}'])    Timechannel = ChannelObject('run:R_2021', 'Time',time_array)    return Timechanneldef write_magnet(dataframe):    magnet = 'Argonne'    magnet_array = np.array([f'{magnet}'])    Magnetchannel = ChannelObject('run:R_2021', 'magnet', magnet_array)    return Magnetchanneldef write_measurement(dataframe):    meas = 'FMS'    measurement_array = np.array([f'{meas}'])    Measurementchannel = ChannelObject('run:R_2021', 'measurement', measurement_array)    return Measurementchanneldef write_configuration(dataframe):    config = 'C:\\Users\\fms-local\\Development\\FMS\\emma_daq\\Property\\Config\\Devel\\FMS_SystemTestNorthwestern2021.ini'    config_array = np.array([f'{config}'])    Configchannel = ChannelObject('run:R_2021', 'configuration', config_array)    return Configchanneldef write_user(dataframe):    user = 'Northwestern'    user_array = np.array([f'{user}'])    Userchannel = ChannelObject('run:R_2021', 'user', user_array)    return Userchanneldef write_script(dataframe):    script = 'FMS_SystemTestNorthwestern2021.py'    script_array = np.array([f'{script}'])    scriptchannel = ChannelObject('run:R_2021', 'script', script_array)    return scriptchanneldef write_scriptparameters(dataframe):    sp = 'FMS.dat'    sp_array = np.array([f'{sp}'])    spchannel = ChannelObject('run:R_2021', 'scriptParameters', sp_array)    return spchanneldef write_scriptfolder(dataframe):    sf = 'C:\\Users\\fms-local\\Development\\FMS\\emma_daq\\Script\\Scripts'    sf_array = np.array([f'{sf}'])    sfchannel = ChannelObject('run:R_2021', 'scriptFolder', sf_array)    return sfchanneldef write_file(dataframe):    file = 'C:\\FMS\\data\\Northwestern\\FMSSystemTest_R_2021.tdms'    file_array = np.array([f'{file}'])    filechannel = ChannelObject('run:R_2021', 'File', file_array)    return filechanneldef write_system(dataframe):    system = 'FMS'    system_array = np.array([f'{system}'])    systemchannel = ChannelObject('run:R_2021', 'system', system_array)    return systemchanneldef write_initalilizationgroup(dataframe, tdms_writer):    group = GroupObject("run:R_2021", properties={       })    wholegroup = tdms_writer.write_segment([group, write_ID(dataframe), write_Time(dataframe), write_magnet(dataframe),                                            write_measurement(dataframe), write_configuration(dataframe),                                            write_user(dataframe), write_script(dataframe),                                            write_scriptparameters(dataframe), write_scriptfolder(dataframe),                                            write_file(dataframe), write_system(dataframe)])    return wholegroupdef write_ID2(index, dataframe, sequence):    id = dataframe['SeqID'].iloc[index]    id_array = np.array([f'{id}'])    idchannel = ChannelObject(f'{sequence}', 'ID', id_array)    return idchanneldef write_QC2(index, dataframe, sequence):    item1 = ''    item2 = ''    QC_array = np.array([f'{item1}', f'{item2}'])    QCchannel = ChannelObject(f'{sequence}', 'QC', QC_array)    return QCchanneldef write_QCstring(index, dataframe, sequence):    item1 = ''    QCstring_array = np.array([f'{item1}'])    QCstringchannel = ChannelObject(f'{sequence}', 'QC String', QCstring_array)    return QCstringchanneldef write_Timestamp2(index, dataframe, sequence):    timestamp2 = datetime.strptime(dataframe['TIMESTAMP'].iloc[index], '%Y-%m-%d %H:%M:%S')    timestamp = datetime.strftime(timestamp2, '%m/%d/%Y %I:%M:%S %p')    Timestamp_array = np.array([f'Timestamp:{timestamp}'])    Timestampchannel2 = ChannelObject(f'{sequence}', 'Timestamp', Timestamp_array)    return Timestampchannel2def write_StartSequence(index, dataframe, sequence):    status = 'Success'    id1 = 'Slave Down'    id2 = 'Slave UP'    id3 = 'Master UP'    startseq_array = np.array(['Reflector User Coordinates:', f'Status:{status}', f'Reflector ID:{id1}', 'z (mm):',                               'theta (rad):',                               'rho (mm):', f'Status:{status}', f'Reflector ID:{id2}', 'z (mm):','theta (rad):',                               'rho (mm):', f'Status:{status}',                               f'Reflector ID:{id3}','z (mm):', 'theta (rad):', 'rho (mm):', 'Timestamp:'])    seqstartchannel = ChannelObject(f'{sequence}', "Start of Sequence", startseq_array)    return seqstartchanneldef write_EndSequence(index, dataframe, sequence):    status = 'Success'    id1 = 'Slave Down'    id2 = 'Slave UP'    id3 = 'Master UP'    endseq_array = np.array(        ['Reflector User Coordinates:', f'Status:{status}', f'Reflector ID:{id1}', 'z (mm):', 'theta (rad):',         'rho (mm):', f'Status:{status}', f'Reflector ID:{id2}', 'z (mm):', 'theta (rad):', 'rho (mm):',         f'Status:{status}',         f'Reflector ID:{id3}', 'z (mm):', 'theta (rad):', 'rho (mm):', 'Timestamp:'])    seqendchannel = ChannelObject(f'{sequence}', 'End of Sequence', endseq_array)    return seqendchanneldef write_sequencegroup(index, dataframe, step, sequence, tdms_writer):    group = GroupObject(f"{sequence}", properties={    })    wholegroup = tdms_writer.write_segment([group, write_ID2(index, dataframe, sequence),                                            write_QC2(index, dataframe, sequence),                                            write_QCstring(index, dataframe,sequence),                                            write_Timestamp2(index, dataframe, sequence),                                            write_StartSequence(index, dataframe, sequence),                                            write_EndSequence(index, dataframe, sequence)])    return wholegroupprint("TestDatatoTDMS __name__ is set to: {}" .format(__name__))if __name__ == "__main__":    scriptdir = os.path.dirname(os.path.realpath(__file__))    datadir = os.path.join(scriptdir, '..', 'data/')    #df = pd.read_pickle(datadir + "DSFM_test_data_v5.pkl")    df = pd.read_pickle('/home/shared_data/FMS_Monitor/DSFM_test_data_1e-4_noise_v6.pkl')    #time_delay = 5    time_delay = 0    #with TdmsWriter("../data/TestDataV2.tdms", 'w') as tdms_writer:    with TdmsWriter('/home/shared_data/FMS_Monitor/TestDataV2.tdms', 'w') as tdms_writer:        dataframe  = df        dataframe["digit_one"] = 0        dataframe["digit_two"] = 0        dataframe["GroupID"] = 'step:0.0.0'  # step.digittwo.digitone        dataframe["SeqID"] = 'seq:0.0'        write_initalilizationgroup(dataframe, tdms_writer)    #starting_index = 500    # starting_index = 100    starting_index = 3400    for index, row in df.iterrows():        with TdmsWriter('/home/shared_data/FMS_Monitor/TestDataV2.tdms', 'a') as tdms_writer:            # create the stepID, stored in new column GroupID            if index == 0:                idlastrow = 0            else:                idlastrow = df.loc[index - 1, "digit_one"]            if index == 0:                df.loc[index, "digit_two"] = 1            if idlastrow == 16:                df.loc[index, "digit_one"] = number = 1                df.loc[index, "digit_two"] = df.loc[index - 1, "digit_two"] + 1            else:                df.loc[index, "digit_one"] = number = idlastrow + 1            if index != 0 and idlastrow != 16:                df.loc[index, "digit_two"] = df.loc[index - 1, "digit_two"]                # write new group for sequence            seconddigit = df["digit_two"].iloc[index]            df.loc[index, "GroupID"] = f'{seconddigit}.{number}'            df.loc[index, "SeqID"] = f'{seconddigit}'            # write the group for the GroupID            step = f'step:1.{df["GroupID"].iloc[index]}'            sequence = f'seq:1.{df["SeqID"].iloc[index]}'            if number != 16:                write_group(index, dataframe, step, tdms_writer)            if number == 16:                write_group(index, dataframe, step, tdms_writer)                write_sequencegroup(index, dataframe, step, sequence, tdms_writer)            print(f"Step {index} written")            #if index > starting_index:            ### time.sleep(time_delay)            print("Time delay done")        if index > starting_index:            time.sleep(time_delay)