import traceback
from pathlib import Path
from typing import Annotated

import typer

from xps_convert.specs_xy_to_kolxpd import convert_specs_prodigy_xy


app = typer.Typer()


@app.command()
def main(
    files: Annotated[list[Path], typer.Argument(help="File(s) to convert")],
) -> None:
    for file in files:
        out_name = file.parent / f"{file.stem}.exp"

        if file.is_file() and file.name.endswith(".xy"):
            try:
                output = convert_specs_prodigy_xy(file)
                with open(out_name, "w") as outfile:
                    _ = outfile.write(output)

            except Exception:
                print(f"Failed to convert file {file.name}:")
                print(traceback.format_exc())


if __name__ == "__main__":
    app()
