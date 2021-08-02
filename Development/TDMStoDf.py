import pandas as pd
from nptdms import TdmsFile

tdms_file = TdmsFile.open("../data/TestDataV2.tdms")
df = pd.DataFrame(tdms_file)
print(df)