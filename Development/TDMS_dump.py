import pandas as pd
from nptdms import TdmsFile
# import pickle
# import numpy as np
import os
# import time
from datetime import datetime
from collections import defaultdict
from shutil import copyfile

# directories and outputs
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
pklfile = datadir + 'TDMS_dump.pkl'

# PUT REAL TDMS FIILENAME HERE
tdms_file_original = datadir + 'TestDataV2.tdms'
tdms_file_copied = datadir + 'COPYTestDataV2.tdms'

def process_channel_general(tdms_file, group, channel, data_dict):
    data = tdms_file[group.name][channel.name][:]
    for element in data:
        data_list = element.split(':')
        key = data_list[0]
        value = ':'.join(data_list[1:])
        data_dict[f'{channel.name}_{key}'].append(value)
    return data_dict

def process_channel_multiple_devices(tdms_file, group, channel, data_dict):
    data = tdms_file[group.name][channel.name][:]
    dict_temp = defaultdict(list)
    dict_temp = process_channel_general(tdms_file, group, channel, dict_temp)
    # DEBUG
    print(dict_temp)
    if channel.name == 'HallProbes':
        dev_key = 'HallProbes_Sensor.name'
        # dev_key = 'Sensor.name'
    else:
        # dev_key = 'Measured Coordinates_Reflector ID'
        dev_key = f'{channel.name}_Reflector ID'
        # dev_key = 'Reflector ID'
    devices = dict_temp[dev_key]
    N_devices = len(devices)
    for index, device in enumerate(devices):
        for key, val in dict_temp.items():
            if (key != dev_key) and (len(val) == N_devices):
                data_dict[f'{key}_{device}'].append(val[index])
    return data_dict

def process_step_channel(tdms_file, group, channel, data_dict):
    if (channel.name == 'HallProbes') or (channel.name == 'Measured Coordinates') or (channel.name == 'Predicted Coordinates'):
        data_dict = process_channel_multiple_devices(tdms_file, group, channel, data_dict)
    elif (channel.name == 'StepID'):
        data_dict['StepID'].append(tdms_file[group.name][channel.name][0])
    elif (channel.name == 'QC'):
        d_ = tdms_file[group.name][channel.name][:]
        if len(''.join(d_)) == 0:
            data_dict['QC'].append('')
        else:
            data_dict['QC'].append(', '.join(d_))
    else:
        data_dict = process_channel_general(tdms_file, group, channel, data_dict)

    return data_dict

def process_all_steps(tdms_filename):
    data_dict = defaultdict(list)

    with TdmsFile.open(tdms_filename) as tdms_file:
        groups = tdms_file.groups()

        for group in groups:
            if 'step' in group.name:
                channels = group.channels()
                for channel in channels:
                    try:
                        data_dict = process_step_channel(tdms_file, group, channel, data_dict)
                    except Exception as e:
                        print(f'{group.name}, {channel.name}')
                        print(e)
    return data_dict

def make_TDMS_dump(tdms_file_copied, pklfile):
    t0 = datetime.now()
    print(f'{t0} Starting TDMS Dump')

    # process the data
    # data_dict = process_all_steps(tdms_file_original)
    data_dict = process_all_steps(tdms_file_copied)
    # create a pandas dataframe and save as a pickle file
    df = pd.DataFrame(data_dict)
    df.to_pickle(pklfile)
    print(df.info())
    tf = datetime.now()
    print(f'{tf} Finished TDMS Dump')
    print(f'Elapsed: {(tf-t0).total_seconds()} s\n')
    return data_dict, df

if __name__ == '__main__':
    # make a copy of the TDMS file
    copyfile(tdms_file_original, tdms_file_copied)
    # process data
    data_dict, df = make_TDMS_dump(tdms_file_copied, pklfile)
