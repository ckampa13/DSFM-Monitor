import pandas as pd
from nptdms import TdmsFile
import pickle
import numpy as np
import os
import time
import time

scriptdir = os.path.dirname(os.path.realpath(__file__))
datadir = os.path.join(scriptdir, '..', 'data/')
#filename = datadir + 'liveupdates.pkl'
filename = '/home/shared_data/FMS_Monitor/liveupdates.pkl'
# with open(filename, 'rb') as file:
#     variable_dict = pickle.load(file)
livedata = True


starttime = time.time()





while livedata == True:
     previous_group_names = []
     groupnamelist = []

     #with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
     with TdmsFile.open('/home/shared_data/FMS_Monitor/TestDataV2.tdms') as tdms_file:
         groups = tdms_file.groups()
         for group in groups:
            groupname = group.name
            if groupname == 'run:R_2021' or groupname[2] == 'q':
                pass
            # if groupname in previous_group_names:
            #     pass
            else:
                groupnamelist.append(groupname)
                previous_group_names.append(groupname)
         dict_halls = {'TIMESTAMP': [], 'B_NMR': [], 'Mapper_Angle': [], 'Mapper_Z': [], 'HP_SP1_ID' : [], 'HP_SP1_X' : [], 'HP_SP1_Y' : [], 'HP_SP1_Z' : [], 'HP_SP1_Vx' : [],
                'HP_SP1_Vy' : [], 'HP_SP1_Vz' : [], 'HP_SP1_Temperature' : [], 'HP_SP1_Bx_Meas' : [], 'HP_SP1_By_Meas' : [], 'HP_SP1_Bz_Meas' : [],
                'HP_SP1_Br' : [], 'HP_SP1_Bphi' : [], 'HP_SP2_ID' : [], 'HP_SP2_X' : [], 'HP_SP2_Y' : [], 'HP_SP2_Z' : [], 'HP_SP2_Vx' : [],
                'HP_SP2_Vy' : [], 'HP_SP2_Vz' : [], 'HP_SP2_Temperature' : [], 'HP_SP2_Bx_Meas' : [], 'HP_SP2_By_Meas' : [], 'HP_SP2_Bz_Meas' : [],
                'HP_SP2_Br' : [], 'HP_SP2_Bphi' : [], 'HP_SP3_ID' : [], 'HP_SP3_X' : [], 'HP_SP3_Y' : [], 'HP_SP3_Z' : [], 'HP_SP3_Vx' : [],
                'HP_SP3_Vy' : [], 'HP_SP3_Vz' : [], 'HP_SP3_Temperature' : [], 'HP_SP3_Bx_Meas' : [], 'HP_SP3_By_Meas' : [], 'HP_SP3_Bz_Meas' : [],
                'HP_SP3_Br' : [], 'HP_SP3_Bphi' : [], 'HP_BP1_ID' : [], 'HP_BP1_X' : [], 'HP_BP1_Y' : [], 'HP_BP1_Z' : [], 'HP_BP1_Vx' : [],
                'HP_BP1_Vy' :[], 'HP_BP1_Vz' : [], 'HP_BP1_Temperature' : [], 'HP_BP1_Bx_Meas' : [], 'HP_BP1_By_Meas' : [], 'HP_BP1_Bz_Meas' : [], 'HP_BP1_Br' : [],
                'HP_BP1_Bphi' : [],'HP_BP2_ID' : [], 'HP_BP2_X' : [],'HP_BP2_Y' : [], 'HP_BP2_Z' : [], 'HP_BP2_Vx' : [], 'HP_BP2_Vy' : [], 'HP_BP2_Vz' : [],
                'HP_BP2_Temperature' : [], 'HP_BP2_Bx_Meas' : [], 'HP_BP2_By_Meas' : [], 'HP_BP2_Bz_Meas' : [], 'HP_BP2_Br' : [], 'HP_BP2_Bphi' : [],'HP_BP3_ID' : [],
                'HP_BP3_X' : [], 'HP_BP3_Y' : [], 'HP_BP3_Z' : [], 'HP_BP3_Vx' : [], 'HP_BP3_Vy' : [], 'HP_BP3_Vz' : [], 'HP_BP3_Temperature': [], 'HP_BP3_Bx_Meas' : [], 'HP_BP3_By_Meas' : [], 'HP_BP3_Bz_Meas' : [],
                'HP_BP3_Br' : [], 'HP_BP3_Bphi' : [], 'HP_BP4_ID' : [], 'HP_BP4_X' : [], 'HP_BP4_Y' : [],'HP_BP4_Z' : [],
                'HP_BP4_Vx' : [], 'HP_BP4_Vy' : [], 'HP_BP4_Vz' : [], 'HP_BP4_Temperature' : [],'HP_BP4_Bx_Meas' : [], 'HP_BP4_By_Meas' : [], 'HP_BP4_Bz_Meas' : [],
                'HP_BP4_Br' : [],'HP_BP4_Bphi' : [], 'HP_BP5_ID' : [], 'HP_BP5_X' : [], 'HP_BP5_Y' : [], 'HP_BP5_Z' : [],'HP_BP5_Vx' : [], 'HP_BP5_Vy' : [],
                'HP_BP5_Vz' : [], 'HP_BP5_Temperature' : [],'HP_BP5_Bx_Meas' : [], 'HP_BP5_By_Meas' : [], 'HP_BP5_Bz_Meas' : [], 'HP_BP5_Br' : [], 'HP_BP5_Bphi' : []}
                #df_halls = pd.DataFrame(dict_halls)
         print("this is dict_halls-should be empty", dict_halls)

         for name in groupnamelist:
            print(name)

            #for chunk in tdms_file.data_chunks():
            print("in chunk loop")
            channel_chunk = tdms_file[f'{name}']['HallProbes']
 #channel_chunk = chunk[f'{name}']['HallProbes']
 #print(channel_chunk)
            array = channel_chunk[:]
            #print(array)
            if array.size > 0: #remove
                new_list = []
                column_list = []  # column_array = np.array([])

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
                print("HallProbe new_array", new_array)
            #print(column_array)
            #print(new_array)
            #print(len(new_array))
                dictH = {'TIMESTAMP': new_array[-1], 'HP_SP1_ID' : new_array[15], 'HP_SP1_X' : new_array[12], 'HP_SP1_Y' : new_array[11], 'HP_SP1_Z' : new_array[10], 'HP_SP1_Vx' : new_array[9],
                'HP_SP1_Vy' : new_array[8], 'HP_SP1_Vz' : new_array[7], 'HP_SP1_Temperature' : new_array[1], 'HP_SP1_Bx_Meas' : new_array[4], 'HP_SP1_By_Meas' : new_array[3], 'HP_SP1_Bz_Meas' : new_array[2],
            'HP_SP1_Br' : new_array[5], 'HP_SP1_Bphi' : new_array[6], 'HP_SP2_ID' : new_array[32], 'HP_SP2_X' : new_array[29], 'HP_SP2_Y' : new_array[28], 'HP_SP2_Z' : new_array[27], 'HP_SP2_Vx' : new_array[26],
            'HP_SP2_Vy' : new_array[25], 'HP_SP2_Vz' : new_array[24], 'HP_SP2_Temperature' : new_array[18], 'HP_SP2_Bx_Meas' : new_array[21], 'HP_SP2_By_Meas' : new_list[20], 'HP_SP2_Bz_Meas' : new_array[19],
            'HP_SP2_Br' : new_array[22], 'HP_SP2_Bphi' : new_array[23], 'HP_SP3_ID' : new_array[49], 'HP_SP3_X' : new_array[46], 'HP_SP3_Y' : new_array[45], 'HP_SP3_Z' : new_array[44], 'HP_SP3_Vx' : new_array[43],
            'HP_SP3_Vy' : new_array[42], 'HP_SP3_Vz' : new_array[41], 'HP_SP3_Temperature' : new_array[35], 'HP_SP3_Bx_Meas' : new_array[38], 'HP_SP3_By_Meas' : new_array[37], 'HP_SP3_Bz_Meas' : new_array[36],
            'HP_SP3_Br' : new_array[39], 'HP_SP3_Bphi' : new_array[40], 'HP_BP1_ID' : new_array[66], 'HP_BP1_X' : new_array[63], 'HP_BP1_Y' : new_array[62], 'HP_BP1_Z' : new_array[61], 'HP_BP1_Vx' : new_array[60],
            'HP_BP1_Vy' : new_array[59], 'HP_BP1_Vz' : new_array[58], 'HP_BP1_Temperature' : new_array[52], 'HP_BP1_Bx_Meas' : new_array[55], 'HP_BP1_By_Meas' : new_array[54], 'HP_BP1_Bz_Meas' : new_array[53], 'HP_BP1_Br' : new_array[56],
            'HP_BP1_Bphi' : new_array[57],'HP_BP2_ID' : new_array[83], 'HP_BP2_X' : new_array[80],'HP_BP2_Y' : new_array[79], 'HP_BP2_Z' : new_array[78], 'HP_BP2_Vx' : new_array[77], 'HP_BP2_Vy' : new_array[76], 'HP_BP2_Vz' : new_array[75],
            'HP_BP2_Temperature' : new_array[69], 'HP_BP2_Bx_Meas' : new_array[72], 'HP_BP2_By_Meas' : new_array[71], 'HP_BP2_Bz_Meas' : new_array[70], 'HP_BP2_Br' : new_array[73], 'HP_BP2_Bphi' : new_array[74],'HP_BP3_ID' : new_array[100],
            'HP_BP3_X' : new_array[97], 'HP_BP3_Y' : new_array[96], 'HP_BP3_Z' : new_array[95], 'HP_BP3_Vx' : new_array[94], 'HP_BP3_Vy' : new_array[93], 'HP_BP3_Vz' : new_array[92], 'HP_BP3_Temperature' : new_array[86], 'HP_BP3_Bx_Meas' : new_array[89],
            'HP_BP3_By_Meas' : new_array[88], 'HP_BP3_Bz_Meas' : new_array[87], 'HP_BP3_Br' : new_array[90], 'HP_BP3_Bphi' : new_array[91], 'HP_BP4_ID' : new_array[117], 'HP_BP4_X' : new_array[114], 'HP_BP4_Y' : new_array[113], 'HP_BP4_Z' : new_array[112],
            'HP_BP4_Vx' : new_array[111], 'HP_BP4_Vy' : new_array[110], 'HP_BP4_Vz' : new_array[109], 'HP_BP4_Temperature' : new_array[103],'HP_BP4_Bx_Meas' : new_array[106], 'HP_BP4_By_Meas' : new_array[105], 'HP_BP4_Bz_Meas' : new_array[104],
            'HP_BP4_Br' : new_array[107],'HP_BP4_Bphi' : new_array[108], 'HP_BP5_ID' : new_array[134], 'HP_BP5_X' : new_array[131], 'HP_BP5_Y' : new_array[130], 'HP_BP5_Z' : new_array[129],'HP_BP5_Vx' : new_array[128], 'HP_BP5_Vy' : new_array[127],
            'HP_BP5_Vz' : new_array[126], 'HP_BP5_Temperature' : new_array[120],'HP_BP5_Bx_Meas' : new_array[123], 'HP_BP5_By_Meas' : new_array[122], 'HP_BP5_Bz_Meas' : new_array[121], 'HP_BP5_Br' : new_array[124], 'HP_BP5_Bphi' : new_array[125]}
            #dict_halls.concatenate(dict)
                for key, val in dictH.items():
                    if key in dict_halls :
                        #if type(dict_halls[key]) == list:
                        dict_halls[key].append(val)
                        # else:
                        #     dict_halls[key] = (dict_halls[key], val)

            #print(dict)
            channel_chunk_NMR = tdms_file[f'{name}']['NMRProbe']
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

                dict_NMR = {"B_NMR": new_array_nmr[2]}  #save NMR location
                for key, val in dict_NMR.items():
                    if key in dict_halls: #add else for errors
                        #if type(dict_halls[key]) == list:
                        dict_halls[key].append(val)
                        # else:
                        #     dict_halls[key] = (dict_halls[key], val)

                    #print(dict_NMR)
                channel_chunk_mapper = tdms_file[f'{name}']['Mapper']
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
                            #if type(dict_halls[key]) == list:
                            dict_halls[key].append(val)
                            # else:
                            #     dict_halls[key] = (dict_halls[key], val)
                #print(dict_halls)

                #print(dict_MAPPER)
            #print(dict_halls)

         df = pd.DataFrame(dict_halls)
         for column in df.columns:
             if column != 'TIMESTAMP' and 'ID' not in column:
                 df[column] = df[column].astype(float)

         #df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
         df["TIMESTAMP"] = pd.to_datetime([str(i) for i in df["TIMESTAMP"]])
         #df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"].astype(str))


         print(dict_halls['TIMESTAMP'])
         #print(df['HP_BP1_Br'])

         df.to_pickle(filename)
         time.sleep(10)

            # with open(filename, 'wb') as file:
            #     pickle.dump(df, file)

     #time.sleep(60.0 - ((time.time()- starttime) % 60.0))







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

