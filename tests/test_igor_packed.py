from pathlib import Path

import igor
from igor.ibw import WaveHeaderV5

testdata = Path(__file__).parent / "testdata"

PXT_SINGLE = testdata / "Sample1-10002.pxt"
PXT_MULTIPLE = testdata / "Sample1-10005.pxt"
PXT_CYCLED = testdata / "Sample1-10026.pxt"
PXT_TR = testdata / "Sample1-10070.pxt"


def test_pxt_single_spectrum():
    pxt = igor.PackedFile(str(PXT_SINGLE))
    assert len(pxt.records) == 1
    ibw = pxt.records[0]

    assert isinstance(ibw.wave_header, WaveHeaderV5)
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

    start_data = [round(x, 2) for x in ibw.data[0:3]]
    assert start_data == [1099.11, 1077.02, 1088.60]

    end_data = [round(x, 2) for x in ibw.data[-3:]]
    assert end_data == [10.87, 12.28, 11.99]

    # size: 4884 byts


def test_pxt_multiple_spectra():
    pxt = igor.PackedFile(str(PXT_MULTIPLE))
    assert len(pxt.records) == 3

    ce_ibw = pxt.records[0]
    rh_ibw = pxt.records[1]
    pt_ibw = pxt.records[2]

    # Ce3d
    assert isinstance(ce_ibw.wave_header, WaveHeaderV5)
    assert ce_ibw.wave_header.bname == "Ce3d_1486-7Sample1-1005"

    assert ce_ibw.wave_header.n_dim[1] == 0
    assert ce_ibw.wave_header.n_dim[2] == 0
    assert ce_ibw.wave_header.n_dim[3] == 0

    rows = ce_ibw.wave_header.n_dim[0]
    assert rows == 1601
    assert ce_ibw.wave_header.npnts == 1601

    start = round(ce_ibw.wave_header.sf_b[0], 8)
    assert start == 940

    delta = round(ce_ibw.wave_header.sf_a[0], 8)
    assert delta == -0.05

    units = ce_ibw.dim_e_units[0]
    assert units == "Binding Energy [eV]"

    data_units = ce_ibw.extended_data_units
    assert data_units == "Counts [a.u.]"

    start_data = [round(x, 1) for x in ce_ibw.data[0:3]]
    assert start_data == [61561.8, 61520.5, 61335.5]

    end_data = [round(x, 1) for x in ce_ibw.data[-3:]]
    assert end_data == [29409.1, 29526.7, 29632.5]

    # Rh3d
    assert isinstance(rh_ibw.wave_header, WaveHeaderV5)
    assert rh_ibw.wave_header.bname == "Rh3d_1486-7Sample1-1005"

    assert rh_ibw.wave_header.n_dim[1] == 0
    assert rh_ibw.wave_header.n_dim[2] == 0
    assert rh_ibw.wave_header.n_dim[3] == 0

    rows = rh_ibw.wave_header.n_dim[0]
    assert rows == 1001
    assert rh_ibw.wave_header.npnts == 1001

    start = round(rh_ibw.wave_header.sf_b[0], 8)
    assert start == 340

    delta = round(rh_ibw.wave_header.sf_a[0], 8)
    assert delta == -0.05

    units = rh_ibw.dim_e_units[0]
    assert units == "Binding Energy [eV]"

    data_units = rh_ibw.extended_data_units
    assert data_units == "Counts [a.u.]"

    start_data = [round(x, 2) for x in rh_ibw.data[0:3]]
    assert start_data == [7931.80, 8022.26, 7855.97]

    end_data = [round(x, 2) for x in rh_ibw.data[-3:]]
    assert end_data == [6394.27, 6288.33, 6345.61]


    # Pt4f
    assert isinstance(pt_ibw.wave_header, WaveHeaderV5)
    assert pt_ibw.wave_header.bname == "Pt4f_1486-7Sample1-1005"

    assert pt_ibw.wave_header.n_dim[1] == 0
    assert pt_ibw.wave_header.n_dim[2] == 0
    assert pt_ibw.wave_header.n_dim[3] == 0

    rows = pt_ibw.wave_header.n_dim[0]
    assert rows == 301
    assert pt_ibw.wave_header.npnts == 301

    start = round(pt_ibw.wave_header.sf_b[0], 8)
    assert start == 80

    delta = round(pt_ibw.wave_header.sf_a[0], 8)
    assert delta == -0.05

    units = pt_ibw.dim_e_units[0]
    assert units == "Binding Energy [eV]"

    data_units = pt_ibw.extended_data_units
    assert data_units == "Counts [a.u.]"

    start_data = [round(x, 2) for x in pt_ibw.data[0:3]]
    assert start_data == [2071.36, 2166.45, 2157.00]

    end_data = [round(x, 2) for x in pt_ibw.data[-3:]]
    assert end_data == [1895.14, 1925.41, 1910.55]


def test_pxt_cycled():
    pxt = igor.PackedFile(str(PXT_CYCLED))

    assert len(pxt.records) == 1
    ibw = pxt.records[0]
    assert ibw.wave_header.bname == "Pt4f_307_cycleSample1-1026"
    assert isinstance(ibw.wave_header, WaveHeaderV5)

    assert ibw.wave_header.n_dim[2] == 0
    assert ibw.wave_header.n_dim[3] == 0

    assert ibw.wave_header.npnts == 9624

    rows = ibw.wave_header.n_dim[0]
    assert rows == 401
    columns = ibw.wave_header.n_dim[1]
    assert columns == 24

    assert rows * columns == ibw.wave_header.npnts

    start = ibw.wave_header.sf_b[0]
    assert start == 86

    delta = round(ibw.wave_header.sf_a[0], 8)
    assert delta == -0.05

    units_dim0 = ibw.dim_e_units[0]
    assert units_dim0 == "Binding Energy [eV]"
    units_dim1 = ibw.dim_e_units[1]
    assert units_dim1 == "Seq. Iteration[a.u.]"

    data_units = ibw.extended_data_units
    assert data_units == "Counts [a.u.]"

    start_data = [round(x, 3) for x in ibw.data[0:3]]
    assert start_data == [547.668, 555.143, 552.331]

    end_data = [round(x, 3) for x in ibw.data[-3:]]
    assert end_data == [310.657, 305.703, 313.602]


def test_pxt_tr():
    pxt = igor.PackedFile(str(PXT_TR))

    assert len(pxt.records) == 1
    ibw = pxt.records[0]
    assert ibw.wave_header.bname == "O1s_650_trSample1-1070"
    assert isinstance(ibw.wave_header, WaveHeaderV5)

    assert ibw.wave_header.n_dim[2] == 0
    assert ibw.wave_header.n_dim[3] == 0

    assert ibw.wave_header.npnts == 228121

    rows = ibw.wave_header.n_dim[0]
    assert rows == 1453
    columns = ibw.wave_header.n_dim[1]
    assert columns == 157

    assert rows * columns == ibw.wave_header.npnts

    start = round(ibw.wave_header.sf_b[0], 3)
    assert start == 540.869

    delta = round(ibw.wave_header.sf_a[0], 8)
    assert delta == -0.00672

    units_dim0 = ibw.dim_e_units[0]
    assert units_dim0 == "Binding Energy [eV]"
    units_dim1 = ibw.dim_e_units[1]
    assert units_dim1 == "Region Iteration[a.u.]"

    data_units = ibw.extended_data_units
    assert data_units == "Counts [a.u.]"

    start_data = [round(x, 7) for x in ibw.data[0:3]]
    assert start_data == [0.0, 0.2246761, 0.0130158]

    end_data = [round(x, 3) for x in ibw.data[-3:]]
    assert end_data == [0.0, 0.0, 0.0]
