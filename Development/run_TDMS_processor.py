import os
import time
from datetime import datetime
import pandas as pd
from collections import defaultdict
from shutil import copyfile
from nptdms import TdmsFile
# import from each step in the processing
from TDMS_check import find_default_structure, check_group_structure
from TDMS_dump import process_step_channel, make_TDMS_dump
from TDMS_dump_to_df_raw import format_df_raw

# directories and files
scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
pklfile_structure = datadir + 'TDMS_structure.pkl'
pklfile_dump = datadir + 'TDMS_dump.pkl'
pklfile_processed = datadir + 'TDMS_processed.pkl'
pklfile_raw = datadir + 'liveupdates.pkl'

# PUT REAL TDMS FIILENAME HERE
tdms_file_original = datadir + 'TestDataV2.tdms'
tdms_file_copied = datadir + 'COPYTestDataV2.tdms'

# other globals
default_group='step:1.1.1'
time_delay = 5. # seconds
# pseudo-delay (only if we get full TDMS file and want to pretend it's live)
pseudo_delay = 0. # seconds

# FIXME! see below
# this is a dumb object to add a "name" attribute, converted from a string.
# the current processing funtions (TDMS_dump.py) assume "group" and "channel"
# are objects in nptdms, and grabs the "name" attribute
class NAME_OBJ(object):
    def __init__(self, string):
        self.name = string

if __name__ == '__main__':
    default_structure = None
    processed_groups = []
    struct_list = []
    data_list = []
    df_raw = None
    while(True):
        print(f'{datetime.now()} Processing loop start')
        # copy TDMS file
        copyfile(tdms_file_original, tdms_file_copied)
        # find the default structure if it has not been found yet
        if default_structure is None:
            groups, channels, default_structure = find_default_structure(tdms_file_copied, default_group)
            # if still no default structure, wait and start the loop again
            if default_structure is None:
                time.sleep(time_delay)
                print(f'{datetime.now()} Exiting loop: Default group not found\n')
                continue
        # grab only groups with "step" in the name
        step_groups = [g for g in groups if "step" in g]
        # open the copied TDMS file and process
        with TdmsFile.open(tdms_file_copied) as tdms_file:
            # struct_list = []
            # loop through step groups and process, only if they have not been processed yet
            for group in step_groups:
                if group in processed_groups:
                    continue
                else:
                    # FIXME! A bad workaround...
                    group_str = group
                    group = NAME_OBJ(group_str)
                    # convert group to name object
                    # check structure
                    struct = check_group_structure(group_str, tdms_file, default_structure)
                    struct_list.append(struct)
                    # parse channels
                    channels = [s for s in struct.keys() if not s in ['group', 'data_quality_passed']]
                    data_dict = defaultdict(list)
                    # loop through channels to append this row of the dataframe
                    for channel in channels:
                        # FIXME! A bad workaround...
                        channel = NAME_OBJ(channel)
                        # decide how to process group data based on data quality
                        # if struct['data_quality_passed']:
                        data_dict = process_step_channel(tdms_file, group, channel, data_dict)
                    # loop through keys to make key: value rather than key: [value]
                    # FIXME! can make this clearer and faster
                    for key in data_dict.keys():
                        if type(data_dict[key]) is list:
                            data_dict[key] = data_dict[key][0]
                    data_list.append(data_dict)
                    # update list of processed groups
                    processed_groups.append(group_str)
                # pseudo delay
                time.sleep(pseudo_delay)
        # create dataframes and save pickles
        df_struct = pd.DataFrame(struct_list)
        df_dump = pd.DataFrame(data_list)
        df_processed = pd.DataFrame({'group': processed_groups})
        df_raw = format_df_raw(df_dump)
        # pickle
        df_struct.to_pickle(pklfile_structure)
        df_dump.to_pickle(pklfile_dump)
        df_processed.to_pickle(pklfile_processed)
        df_raw.to_pickle(pklfile_raw)

        # pause
        time.sleep(time_delay)
        print(f'{datetime.now()} Exiting loop: processing complete\n')
