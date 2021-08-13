import pandas as pd
from nptdms import TdmsFile
import pickle
import numpy as np
import os

scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
filename = datadir + 'liveupdates.pkl.py'
# with open(filename, 'rb') as file:
#     variable_dict = pickle.load(file)


groupnamelist = []

with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
    groups = tdms_file.groups()
    for group in groups:
        groupname = group.name
        if groupname == 'run:R_2021' or groupname[2] == 'q':
            pass
        else:
            groupnamelist.append(groupname)
    dict_halls = {'TIMESTAMP': [], 'B_NMR': [], 'Mapper_Angle': [], 'Mapper_Z': [], 'SP1_ID' : [], 'SP1_X' : [], 'SP1_Y' : [], 'SP1_Z' : [], 'SP1_Vx' : [],
                'SP1_Vy' : [], 'SP1_Vz' : [], 'SP1_Temperature' : [], 'SP1_Bx' : [], 'SP1_By' : [], 'SP1_Bz' : [],
                'SP1_Br' : [], 'SP1_Bphi' : [], 'SP2_ID' : [], 'SP2_X' : [], 'SP2_Y' : [], 'SP2_Z' : [], 'SP2_Vx' : [],
                'SP2_Vy' : [], 'SP2_Vz' : [], 'SP2_Temperature' : [], 'SP2_Bx' : [], 'SP2_By' : [], 'SP2_Bz' : [],
                'SP2_Br' : [], 'SP2_Bphi' : [], 'SP3_ID' : [], 'SP3_X' : [], 'SP3_Y' : [], 'SP3_Z' : [], 'SP3_Vx' : [],
                'SP3_Vy' : [], 'SP3_Vz' : [], 'SP3_Temperature' : [], 'SP3_Bx' : [], 'SP3_By' : [], 'SP3_Bz' : [],
                'SP3_Br' : [], 'SP3_Bphi' : [], 'BP1_ID' : [], 'BP1_X' : [], 'BP1_Y' : [], 'BP1_Z' : [], 'BP1_Vx' : [],
                'BP1_Vy' :[], 'BP1_Vz' : [], 'BP1_Temperature' : [], 'BP1_Bx' : [], 'BP1_By' : [], 'BP1_Bz' : [], 'BP1_Br' : [],
                'BP1_Bphi' : [],'BP2_ID' : [], 'BP2_X' : [],'BP2_Y' : [], 'BP2_Z' : [], 'BP2_Vx' : [], 'BP2_Vy' : [], 'BP2_Vz' : [],
                'BP2_Temperature' : [], 'BP2_Bx' : [], 'BP2_By' : [], 'BP2_Bz' : [], 'BP2_Br' : [], 'BP2_Bphi' : [],'BP3_ID' : [],
                'BP3_X' : [], 'BP3_Y' : [], 'BP3_Z' : [], 'BP3_Vx' : [], 'BP3_Vy' : [], 'BP3_Vz' : [], 'BP3_Temperature': [], 'BP3_Bx' : [], 'BP3_By' : [], 'BP3_Bz' : [],
                'BP3_Br' : [], 'BP3_Bphi' : [], 'BP4_ID' : [], 'BP4_X' : [], 'BP4_Y' : [],'BP4_Z' : [],
                'BP4_Vx' : [], 'BP4_Vy' : [], 'BP4_Vz' : [], 'BP4_Temperature' : [],'BP4_Bx' : [], 'BP4_By' : [], 'BP4_Bz' : [],
                'BP4_Br' : [],'BP4_Bphi' : [], 'BP5_ID' : [], 'BP5_X' : [], 'BP5_Y' : [], 'BP5_Z' : [],'BP5_Vx' : [], 'BP5_Vy' : [],
                'BP5_Vz' : [], 'BP5_Temperature' : [],'BP5_Bx' : [], 'BP5_By' : [], 'BP5_Bz' : [], 'BP5_Br' : [], 'BP5_Bphi' : []}
    #df_halls = pd.DataFrame(dict_halls)

    for name in groupnamelist:
        for chunk in tdms_file.data_chunks():
            channel_chunk = chunk[f'{name}']['HallProbes']
            array = np.array(channel_chunk[:])
            if array.size > 0:
                new_list = []
                column_list = []  # column_array = np.array([])
                #print(channel_chunk[:])
                for item in array:
                    x = item.split(':')[1]
                    y = item.split(':')[0]
                    if y == 'Timestamp':
                        z = x + ':' + item.split(':')[2] + ':' + item.split(':')[3]
                        new_list.append(z)
                    else:
                        new_list.append(x)  # np.append(arr = new_array, values = x)

                    column_list.append(y)  # np.append(arr = column_array,values = y)
                column_array = np.array(column_list)
                new_array = np.array(new_list)
                #print(column_array)
                #print(new_array)
                #print(len(new_array))
                dict = {'TIMESTAMP': new_array[-1], 'SP1_ID' : new_array[15], 'SP1_X' : new_array[12], 'SP1_Y' : new_array[11], 'SP1_Z' : new_array[10], 'SP1_Vx' : new_array[9],
                'SP1_Vy' : new_array[8], 'SP1_Vz' : new_array[7], 'SP1_Temperature' : new_array[1], 'SP1_Bx' : new_array[4], 'SP1_By' : new_array[3], 'SP1_Bz' : new_array[2],
                'SP1_Br' : new_array[5], 'SP1_Bphi' : new_array[6], 'SP2_ID' : new_array[32], 'SP2_X' : new_array[29], 'SP2_Y' : new_array[28], 'SP2_Z' : new_array[27], 'SP2_Vx' : new_array[26],
                'SP2_Vy' : new_array[25], 'SP2_Vz' : new_array[24], 'SP2_Temperature' : new_array[18], 'SP2_Bx' : new_array[21], 'SP2_By' : new_list[20], 'SP2_Bz' : new_array[19],
                'SP2_Br' : new_array[22], 'SP2_Bphi' : new_array[23], 'SP3_ID' : new_array[49], 'SP3_X' : new_array[46], 'SP3_Y' : new_array[45], 'SP3_Z' : new_array[44], 'SP3_Vx' : new_array[43],
                'SP3_Vy' : new_array[42], 'SP3_Vz' : new_array[41], 'SP3_Temperature' : new_array[35], 'SP3_Bx' : new_array[38], 'SP3_By' : new_array[37], 'SP3_Bz' : new_array[36],
                'SP3_Br' : new_array[39], 'SP3_Bphi' : new_array[40], 'BP1_ID' : new_array[66], 'BP1_X' : new_array[63], 'BP1_Y' : new_array[62], 'BP1_Z' : new_array[61], 'BP1_Vx' : new_array[60],
                'BP1_Vy' : new_array[59], 'BP1_Vz' : new_array[58], 'BP1_Temperature' : new_array[52], 'BP1_Bx' : new_array[55], 'BP1_By' : new_array[54], 'BP1_Bz' : new_array[53], 'BP1_Br' : new_array[56],
                'BP1_Bphi' : new_array[57],'BP2_ID' : new_array[83], 'BP2_X' : new_array[80],'BP2_Y' : new_array[79], 'BP2_Z' : new_array[78], 'BP2_Vx' : new_array[77], 'BP2_Vy' : new_array[76], 'BP2_Vz' : new_array[75],
                'BP2_Temperature' : new_array[69], 'BP2_Bx' : new_array[72], 'BP2_By' : new_array[71], 'BP2_Bz' : new_array[70], 'BP2_Br' : new_array[73], 'BP2_Bphi' : new_array[74],'BP3_ID' : new_array[100],
                'BP3_X' : new_array[97], 'BP3_Y' : new_array[96], 'BP3_Z' : new_array[95], 'BP3_Vx' : new_array[94], 'BP3_Vy' : new_array[93], 'BP3_Vz' : new_array[92], 'BP3_Temperature' : new_array[86], 'BP3_Bx' : new_array[89],
                'BP3_By' : new_array[88], 'BP3_Bz' : new_array[87], 'BP3_Br' : new_array[90], 'BP3_Bphi' : new_array[91], 'BP4_ID' : new_array[117], 'BP4_X' : new_array[114], 'BP4_Y' : new_array[113], 'BP4_Z' : new_array[112],
                'BP4_Vx' : new_array[111], 'BP4_Vy' : new_array[110], 'BP4_Vz' : new_array[109], 'BP4_Temperature' : new_array[103],'BP4_Bx' : new_array[106], 'BP4_By' : new_array[105], 'BP4_Bz' : new_array[104],
                'BP4_Br' : new_array[107],'BP4_Bphi' : new_array[108], 'BP5_ID' : new_array[134], 'BP5_X' : new_array[131], 'BP5_Y' : new_array[130], 'BP5_Z' : new_array[129],'BP5_Vx' : new_array[128], 'BP5_Vy' : new_array[127],
                'BP5_Vz' : new_array[126], 'BP5_Temperature' : new_array[120],'BP5_Bx' : new_array[123], 'BP5_By' : new_array[122], 'BP5_Bz' : new_array[121], 'BP5_Br' : new_array[124], 'BP5_Bphi' : new_array[125]}
                #dict_halls.concatenate(dict)
                for key, val in dict.items():
                    if key in dict_halls :
                        if type(dict_halls[key]) == list:
                            dict_halls[key].append(val)
                        else:
                            dict_halls[key] = (dict_halls[key], val)
            channel_chunk_NMR = chunk[f'{name}']['NMRProbe']
            arrayNMR = np.array(channel_chunk_NMR[:])
            if arrayNMR.size > 0:
                new_list_nmr = []
                column_list_nmr = []  # column_array = np.array([])
                #print(channel_chunk[:])
                for item in arrayNMR:
                    x = item.split(':')[1]
                    y = item.split(':')[0]
                    if y == 'Timestamp':
                        z = x + ':' + item.split(':')[2] + ':' + item.split(':')[3]
                    else:
                        new_list_nmr.append(x)  # np.append(arr = new_array, values = x)
                    column_list_nmr.append(y)  # np.append(arr = column_array,values = y)
                column_array_nmr = np.array(column_list_nmr)
                new_array_nmr = np.array(new_list_nmr)
                dict_NMR = {"B_NMR": new_array_nmr[2]}
                for key, val in dict_NMR.items():
                    if key in dict_halls:
                        if type(dict_halls[key]) == list:
                            dict_halls[key].append(val)
                        else:
                            dict_halls[key] = (dict_halls[key], val)
            channel_chunk_mapper = chunk[f'{name}']['Mapper']
            arrayMAPPER = np.array(channel_chunk_mapper[:])
            if arrayMAPPER.size > 0:
                new_list_map = []
                column_list_map = []  # column_array = np.array([])
                #print(channel_chunk[:])
                for item in arrayMAPPER:
                    x = item.split(':')[1]
                    y = item.split(':')[0]
                    if y == 'Timestamp':
                        z = x + ':' + item.split(':')[2] + ':' + item.split(':')[3]
                    else:
                        new_list_map.append(x)  # np.append(arr = new_array, values = x)
                    column_list_map.append(y)  # np.append(arr = column_array,values = y)
                column_array_map = np.array(column_list_map)
                new_array_map = np.array(new_list_map)

                dict_MAPPER = {"Mapper_Angle": new_array_map[2], "Mapper_Z": new_array_map[3]}
            # for key, val in dict.items():
            #     if key in dict_halls :
            #         if type(dict_halls[key]) == list:
            #             dict_halls[key].append(val)
            #         else:
            #             dict_halls[key] = (dict_halls[key], val)
            # for key, val in dict_NMR.items():
            #     if key in dict_halls :
            #         if type(dict_halls[key]) == list:
            #             dict_halls[key].append(val)
            #         else:
            #             dict_halls[key] = (dict_halls[key], val)
                for key, val in dict_MAPPER.items():
                    if key in dict_halls :
                        if type(dict_halls[key]) == list:
                            dict_halls[key].append(val)
                        else:
                            dict_halls[key] = (dict_halls[key], val)

                #dict.update({column: value for (column, value) in zip(column_array, new_array)})
 #                results_dict = {key: [] for key in column_array}
 #                for col in column_array:
 #                    for value in new_array:
 #                        results_dict[col].append(value)
                # for key in results_dict.keys():
                #     results_dict[key] = np.concatenate(results_dict[key])

                #print(dict)
                #df_halls = df_halls.append(dict, ignore_index=True)
    #print(df_halls)
    df = pd.DataFrame(dict_halls)
    print(df.head())
    with open(filename, 'wb') as file:
         pickle.dump(df, file)