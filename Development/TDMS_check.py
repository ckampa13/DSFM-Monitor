import pandas as pd
from nptdms import TdmsFile
import os
from datetime import datetime
from collections import defaultdict
from shutil import copyfile

# directories and outputs
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
# pklfile = datadir + 'TDMS_dump.pkl'
pklfile = datadir + 'TDMS_structure.pkl'

# PUT REAL TDMS FIILENAME HERE
tdms_file_original = datadir + 'TestDataV2.tdms'
tdms_file_copied = datadir + 'COPYTestDataV2.tdms'

def find_default_structure(tdms_filename, default_group='step:1.1.1'):
    with TdmsFile.open(tdms_filename) as tdms_file:
        groups = [g.name for g in tdms_file.groups()]
        # if not default_group in groups:
        #     print(f'WARNING: {default_group} not in TDMS file groups')
        #     return None
        try:
            g_def = tdms_file[default_group]
            channels = [c.name for c in g_def.channels()]
        except Exception as e:
            print(f'WARNING: {default_group} not in TDMS file groups')
            print(e)
            return groups, None, None
        #N_channels = len(channels)
        default_structure = {c:len(g_def[c][:]) for c in channels}
        return groups, channels, default_structure

def check_group_structure(group_name, tdms_file, default_structure):
    # check that it is a step group
    if not 'step' in group_name:
        raise ValueError(f'The input "{group_name}" group is not a valid "step" group')
    g_def = tdms_file[group_name]
    channels = [c.name for c in g_def.channels()]
    struct = {c:len(g_def[c][:]) for c in channels}
    data_qual = True
    if struct != default_structure:
        print(f'WARNING! Group "{group_name}" does not follow the default structure!')
        data_qual = False
    struct['group'] = group_name
    struct['data_quality_passed'] = data_qual
    return struct


if __name__ == '__main__':
    print(f'{datetime.now()} Determining Default Structure:')
    default_group='step:1.1.1'
    # make a copy of the TDMS file
    copyfile(tdms_file_original, tdms_file_copied)
    # check first step for "default" shape
    _ = find_default_structure(tdms_file_copied, default_group)
    groups, channels_expected, default_structure = _
    # test prints
    print('Number of Groups:')
    print(len(groups))
    print('Expected Channels:')
    print(channels_expected)
    print(f'Default structure, from {default_group}')
    print(default_structure)
    print(f'{datetime.now()} Done Determining Default Structure')
    # loop through groups
    print(f'{datetime.now()} Checking Structure of "step" groups:')
    structs = []
    with TdmsFile.open(tdms_file_copied) as tdms_file:
        for group in groups:
            if "step" in group:
                structs.append(check_group_structure(group, tdms_file, default_structure))
    # convert result to pandas dataframe
    df_data_check = pd.DataFrame(structs)
    N = len(df_data_check)
    passed = df_data_check['data_quality_passed'].sum()
    print('Data Quality Dataframe')
    print(df_data_check)
    print(f'{N} steps, {passed} passed, {passed/N * 100:0.1f}% passed')
    print(f'{datetime.now()} Finished Checking Structure of "step" groups')
