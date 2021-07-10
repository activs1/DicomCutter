import pydicom as pd
import os

PATH = r'E:\projects\DicomCutter\data\2_skull_ct'

dicoms = []

for root, dirs, files in os.walk(PATH):
    for file in files:
        fname = os.path.join(root, file)

        try:
            dcm = pd.dcmread(fname)
            dicoms.append(dcm)
            print(f"Loaded {fname}")
        except Exception:
            print(f"Couldn't load {fname}")

descriptions = []
for dcm in dicoms:
    try:
        descriptions.append(dcm.SeriesInstanceUID)
    except Exception:
        pass

print(set(descriptions))
print(len(set(descriptions)))
