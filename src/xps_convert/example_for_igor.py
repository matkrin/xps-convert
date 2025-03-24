from pathlib import Path

from igor_to_kolxpd import convert_igor

def main():
    # data_path = Path("/home/matthias/Documents/Beamtime_Data_All/raw/")
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

    sample1.sort()
    sample1_1.sort()
    sample2.sort()
    sample2_1.sort()

    convert_igor("Sample1", sample1)
    convert_igor("Sample1-1", sample1_1)
    convert_igor("Sample2", sample2)
    convert_igor("Sample2-1", sample2_1)


if __name__ == "__main__":
    main()
