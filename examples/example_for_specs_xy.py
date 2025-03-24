from pathlib import Path
from specs_xy_to_kolxpd import convert_specs_prodigy_xy
import traceback


def main():
    data_path = Path("test-files")
    out_path = Path("test-files")
    xy_files = data_path.glob("*.xy")
    for file in xy_files:
        try:
            output = convert_specs_prodigy_xy(file)
            name = file.name[:-3] + ".exp"
            with open(out_path / name, "w") as outfile:
                outfile.write(output)
        except Exception:
            print(f"Failed to convert file {file.name}:")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
