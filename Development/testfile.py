import pandas as pd
from nptdms import TdmsFile
import numpy as np
from nptdms import TdmsWriter, GroupObject, ChannelObject

with TdmsFile.open("../data/TestDataV2.tdms") as tdms_file:
    all_groups = tdms_file.groups()
    #print(all_groups)
    print(tdms_file["Step:1.1.4"].channels())
    #print(tdms_file["Step:1.1.4"]["Mapper"][:])
