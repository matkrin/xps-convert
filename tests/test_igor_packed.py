from pathlib import Path

import igor

testdata = Path(__file__).parent / "testdata"

PXT_SINGLE = testdata / "Sample1-10002.pxt"
PXT_MULTIPLE = testdata / "Sample1-10005.pxt"
PXT_CYCLED = testdata / "Sample1-10026.pxt"
PXT_TR = testdata / "Sample1-10070.pxt"


def test_pxt_single_spectrum():
    pxt = igor.PackedFile(str(PXT_SINGLE))
    assert len(pxt.records) == 1
    ibw = pxt.records[0]
    assert ibw.wave_header.bname == "survey_307Sample1-1002"

    assert ibw.wave_header.n_dim[1] == 0
    assert ibw.wave_header.n_dim[2] == 0
    assert ibw.wave_header.n_dim[3] == 0

    rows = ibw.wave_header.n_dim[0]
    assert rows == 455
    assert ibw.wave_header.npnts == 455

    start = ibw.wave_header.sf_b[0]
    assert start == 207

    delta = ibw.wave_header.sf_a[0]
    assert delta == -0.5

    units = ibw.dim_e_units[0]
    assert units == "Binding Energy [eV]"

    data_units = ibw.extended_data_units
    assert data_units == "Counts [a.u.]"

    start_data = [f"{x:.2f}" for x in ibw.data[0:3]]
    assert start_data == ["1099.11", "1077.02", "1088.60"]

    end_data = [f"{x:.2f}" for x in ibw.data[-3:]]
    assert end_data == ["10.87", "12.28", "11.99"]

    # size: 4884 byts


def test_pxt_multiple_spectra():
    pxt = igor.PackedFile(str(PXT_MULTIPLE))


def test_pxt_cycled():
    pxt = igor.PackedFile(str(PXT_CYCLED))


def test_pxt_tr():
    pxt = igor.PackedFile(str(PXT_TR))
