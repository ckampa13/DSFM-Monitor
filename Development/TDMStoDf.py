import pandas as pd
from nptdms import TdmsFile
import pickle

tdms_file = TdmsFile.read("../data/TestDataV2.tdms")

with TdmsFile.open('../data/TestDataV2.tdms') as tdms_file:
    all_groups = tdms_file.groups()
    dataframe = pd.DataFrame()
    for groups in all_groups:
        group = groups.name
        df = tdms_file[group].as_dataframe()
        all_channels = tdms_file[group].channels()
        for channel in all_channels:
            channels = channel.name
            dff = tdms_file[group][channels].as_dataframe()
            df.append(dff)
        dataframe.append(df)

    with open("/Users/Lillie/Documents/GitHub/DSFM-Monitor/Development/Newpickle.py", 'wb') as f:
        pickle.dump(df, f)

