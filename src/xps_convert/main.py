from pathlib import Path
from pprint import pprint

from igor.ibw import WaveHeaderV5
from igor.packed import PackedFile


def convert(sample_files: list[Path]):
    for file in sample_files:
        print(f"{file.name}")
        ptx = PackedFile(str(file))

        for wave in ptx.records:
            assert isinstance(wave.wave_header, WaveHeaderV5)
            assert wave.wave_header.n_dim[2] == 0
            assert wave.wave_header.n_dim[3] == 0

            is_2d = wave.wave_header.n_dim[1] != 0
            name = wave.wave_header.bname
            print(f"{name=}")

            rows = wave.wave_header.n_dim[0]
            columns = wave.wave_header.n_dim[1]  # 0 for 1 dim spectra (not cycled or tr)

            num_data_points = wave.wave_header.npnts
            start = wave.wave_header.sf_b[0]
            print(f"{start=}")
            step = wave.wave_header.sf_a[0]
            print(f"{step=}")
            end = start + (step * (num_data_points - 1))
            print(f"{end=}")
            notes = wave.note
            print("-" * 50)

        print("=" * 80)



def main():
    data_path = Path("/Users/matthias/Documents/raw/")

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
