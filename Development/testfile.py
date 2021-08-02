import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, GroupObject, ChannelObject

with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:

    #all_groups = tdms_file.groups()
    for group in tdms_file.groups():
        print(group)
    #print(all_groups)
    #print(tdms_file["step:1.1.4"]["Measured Coordinates"][:])
    print(tdms_file["step:1.2.11"].channels())
    print(tdms_file["step:1.2.11"]['Current'][:])
