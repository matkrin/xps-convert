# xps-convert

Python script to convert Igor .pxt (one export format of Scienta SES) files to
KolXPD .exp files. Thus, this allows to create KolXPD files programmatically for
arbitrary amounts of spectra. You may find it useful if you need to import your
data to KolXPD after, e.g., a beamtime.

## Installation

With [uv](https://docs.astral.sh/uv/):

```bash
uv tool install git+https://github.com/matkrin/xps-convert
```

If you want to install and hack on it, clone the repository and use

```bash
uv tool install --editable .
```

in the project root.

## Usage

To convert an, e.g., .xy-file as exported from Prodigy run:

```bash
xps-convert specs_xy_file.xy
```

You can convert all files in a folder with:

```bash
xps-convert data-folder/*
```

## Writing scripts

You can find examples, how to write script that convert, e.g., many .pxt files
into one single .exp file in the examples folder.
