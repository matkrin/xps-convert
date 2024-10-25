from pathlib import Path
from pprint import pprint

import numpy as np

from igor.ibw import WaveHeaderV5
from igor.packed import PackedFile


def convert(sample_files: list[Path]):
    total_item_count = 0
    all_regions = ""
    for file in sample_files:
        print(f"{file.name}")
        ptx = PackedFile(str(file))

        for wave in ptx.records:
            assert isinstance(wave.wave_header, WaveHeaderV5)
            assert wave.wave_header.n_dim[2] == 0
            assert wave.wave_header.n_dim[3] == 0

            is_2d = wave.wave_header.n_dim[1] != 0
            name = wave.wave_header.bname

            rows = wave.wave_header.n_dim[0]
            print(f"{rows=}")
            columns = wave.wave_header.n_dim[1]  # 0 for 1 dim spectra (not cycled or tr)
            print(f"{columns=}")

            num_data_points = wave.wave_header.npnts
            start = wave.wave_header.sf_b[0]
            step = wave.wave_header.sf_a[0]
            end = start + (step * (num_data_points - 1))
            notes = wave.note
            data = np.array(wave.data)
            if is_2d:
                data = data.reshape(columns, rows)
                avg = np.average(data, axis=0)
                print(f"{avg.shape=}")
                print(f"{avg=}")
                inner_2d = ""
                inner_item_count = 0
                for i, spectrum in enumerate(data):
                    inner_2d += create_region(f"{name} - {i+1}", notes, start, end, step, 0, 1, spectrum)
                    inner_item_count += 1

                avg_str = create_region(f"{name} (avg)", notes, start, end, step, inner_item_count, inner_item_count, avg)
                avg_str += inner_2d

                all_regions += avg_str
                total_item_count += 1
            else:
                all_regions += create_region(f"{name}", notes, start, end, step, 0, 0, data)
                total_item_count += 1

    all = wrap_in_top_level_folder("Sample1-1", total_item_count, all_regions)
    with open("Sample1-1.exp", "w") as f:
        _ = f.write(all)


def wrap_in_top_level_folder(title: str, item_count: int, folder_content: str) -> str:
    top_level = f"""[Folder]
KolXPDversion=1.8.0.69
Title={title}
NotesHTML=0
Notes=
timeStart=0
timeEnd=0
Color=0
ItemCount={item_count}
"""
    top_level += folder_content
    top_level += "[EndFolder]"
    return top_level


def create_region(
    region_title: str,
    notes: str,
    start: float,
    end: float,
    step: float,
    item_count: int,
    sweeps: int,
    data: list[float],
) -> str:
    region = f"""[Region]
KolXPDversion=1.8.0.69
Title={region_title}
Notes={notes.replace("\n", "#0D#0A")}
timeStart=0
timeEnd=0
Color=0
ItemCount={item_count}
Start={start}
End={end}
Dwell=100
DwellSmart=100
PassEn=0
ExcitEn=0
Step={step}
Sweeps={sweeps}
NumOfPointSets=5
AxisBindingEn=-1
Smart=0
WF=0
AxisConvUsesWF=0
Udet=1000
LensMode=
UseMonochromator=0
Level=
Cross=1
Asym=0
ChargeShift=0
AreaMult=1
"""
    region += create_data(data, start, end, step)
    region += "[EndRegion]\n"
    return region


def create_data(data: list[float], start: float, end: float, step: float):
    d = f"""[Data]
#Range {end} {start}
#X Eq {start} {step}
"""
    d += "\n".join(str(i) for i in data)
    d += "\n"
    return d


def main():
    data_path = Path("/home/matthias/Documents/Beamtime_Data_All/raw/")

    sample1: list[Path] = []
    sample1_1: list[Path] = []
    sample2: list[Path] = []
    sample2_1: list[Path] = []

    for file in data_path.iterdir():
        if file.is_file() and file.suffix == ".pxt":
            if file.name.startswith("Sample1"):
                if file.name.startswith("Sample1-1"):
                    sample1_1.append(file)
                else:
                    sample1.append(file)
            elif file.name.startswith("Sample2"):
                if file.name.startswith("Sample2-1"):
                    sample2_1.append(file)
                else:
                    sample2.append(file)

    # pprint(sample1)
    # print("-" * 80)
    # pprint(sample1_1)
    # print("-" * 80)
    # pprint(sample2)
    # print("-" * 80)
    # pprint(sample2_1)

    # convert(sample1)
    convert(sample1_1)
    # convert(sample2)
    # convert(sample2_1)


if __name__ == "__main__":
    main()
