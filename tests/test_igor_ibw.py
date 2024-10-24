from pathlib import Path

import igor

testdata = Path(__file__).parent / "testdata"

IBW_MATRIX = testdata / "test_matrix.ibw"

def test_ibw():
    ibw = igor.Ibw(str(IBW_MATRIX))
    assert ibw.npnts == 16
    assert ibw.bname  == "test_matrix"
    assert ibw.n_dim ==  (4, 4, 0, 0)
    assert ibw.x_step ==  (1, 1, 1, 1)
    assert ibw.x_start ==  (0, 0, 0, 0)
    assert ibw.note == "test matrix 4x4"
    assert ibw.extended_data_units == "data_units"
    assert ibw.data[0:3] == [1.0, 5.0, 9.0]
    assert ibw.data[-3:] == [8.0, 12.0, 16.0]
    assert ibw.dim_e_units == ["row_units", "col_units"]
    assert ibw.dim_labels == ["", ""]
