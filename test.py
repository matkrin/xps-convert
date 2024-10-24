from igor import Ibw, PackedFile

ibw = Ibw("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10002survey_307Sample1-1002.ibw")
# print(ibw)

packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10002.pxt")  # single wave
# packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10005.pxt")  # three waves
# packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10026.pxt")  # cycled
# packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10070.pxt")  # tr
print(packed)
