# from igor import Ibw, PackedFile
#
# ibw = Ibw("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10002survey_307Sample1-1002.ibw")
# # print(ibw)
#
# packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10002.pxt")  # single wave
# # packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10005.pxt")  # three waves
# # packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10026.pxt")  # cycled
# # packed = PackedFile("/home/matthias/Documents/Beamtime_Data_All/raw/Sample1-10070.pxt")  # tr
# print(packed)




def create_top_level_folder(title:str, item_count: int) -> str:
    top_level = """[Folder]
KolXPDversion=1.8.0.69
"""
    top_level += f"Title={title}"
    top_level += """
NotesHTML=0
Notes=
timeStart=0
timeEnd=0
Color=0
"""
    top_level += f"ItemCount={item_count}\n"
    return top_level

print(create_top_level_folder("testtitle", 1))
