from dataclasses import dataclass
from typing import Self, override

from igor.cursor import Cursor


@dataclass
class BinHeaderV1:
    """Version 1 file header.

    Args:
        version: Version number for backwards compatibility.
        wfm_size: Size of the WaveHeader2 data classure plus the wave data
            plus 16 bytes of padding.
        checksum: Checksum over this header and the wave header.
    """

    version: int
    wfm_size: int
    checksum: int


@dataclass
class BinHeaderV2:
    """Version 2 file header.

    Args:
        version: Version number for backwards compatibility.
        wfm_size: The size of the WaveHeader2 data classure
            plus the wave data plus 16 bytes of padding.
        note_size: The size of the note text.
        pict_size: Reserved. Write zero. Ignore on read.
        checksum: Checksum over this header and the wave header.
    """

    version: int
    wfm_size: int
    note_size: int
    pict_size: int
    checksum: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        version = cursor.read_i16_le()
        wfm_size = cursor.read_i32_le()
        note_size = cursor.read_i32_le()
        pict_size = cursor.read_i32_le()
        checksum = cursor.read_i16_le()

        return cls(
            version,
            wfm_size,
            note_size,
            pict_size,
            checksum,
        )


@dataclass
class BinHeaderV3:
    """Version 3 file header.

    Args:
        version: Version number for backwards compatibility.
        wfm_size: The size of the WaveHeader2 data classure plus the wave data
            plus 16 bytes of padding.
        note_size: The size of the note text.
        formula_size: The size of the dependency formula, if any.
        pict_size: Reserved. Write zero. Ignore on read.
        checksum: Checksum over this header and the wave header.
    """

    version: int
    wfm_size: int
    note_size: int
    formula_size: int
    pict_size: int
    checksum: int


@dataclass
class BinHeaderV5:
    """Version 5 file header.

    Args:
        version: Version number for backwards compatibility.
        checksum: Checksum over this header and the wave header.
        wfm_size: The size of the WaveHeader5 data classure plus the wave data.
        formula_size: The size of the dependency formula, if any.
        note_size: The size of the note text.
        data_e_units_size: The size of optional extended data units.
        dim_e_units_size: The size of optional extended dimension units.
        dim_labels_size: The size of optional dimension labels.
        s_indices_size: The size of string indicies if this is a text wave.
        options_size_1: Reserved. Write zero. Ignore on read.
        options_size_2: Reserved. Write zero. Ignore on read.
    """

    version: int
    checksum: int
    wfm_size: int
    formula_size: int
    note_size: int
    data_e_units_size: int
    dim_e_units_size: tuple[int, int, int, int]
    dim_labels_size: tuple[int, int, int, int]
    s_indices_size: int
    options_size_1: int
    options_size_2: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        version = cursor.read_i16_le()
        checksum = cursor.read_i16_le()
        wfm_size = cursor.read_i32_le()
        formula_size = cursor.read_i32_le()
        note_size = cursor.read_i32_le()
        data_e_units_size = cursor.read_i32_le()

        dim_e_units_size = tuple(cursor.read_i32_le() for _ in range(4))
        dim_labels_size = tuple(cursor.read_i32_le() for _ in range(4))

        s_indices_size = cursor.read_i32_le()
        options_size_1 = cursor.read_i32_le()
        options_size_2 = cursor.read_i32_le()

        return cls(
            version,
            checksum,
            wfm_size,
            formula_size,
            note_size,
            data_e_units_size,
            dim_e_units_size,  # pyright: ignore[reportArgumentType]
            dim_labels_size,  # pyright: ignore[reportArgumentType]
            s_indices_size,
            options_size_1,
            options_size_2,
        )


BinHeader = BinHeaderV1 | BinHeaderV2 | BinHeaderV3 | BinHeaderV5


@dataclass
class WaveHeaderV2:
    """Version 2 wave header.

    Args:

        type_: See types (e.g. NT_FP64) above. Zero for text waves.
        next:
        bname:
        wh_version: Write 0. Ignore on read.
        src_fldr: Used in memory only. Write zero. Ignore on read.
        file_name:
        data_units:
        x_units:
        npnts: Number of data points in wave.
        a_modified: Used in memory only. Write zero. Ignore on read.
        hs_a:
        hs_b: X value for point p = hsA*p + hsB
        w_modified: Used in memory only. Write zero. Ignore on read.
        sw_modified: Used in memory only. Write zero. Ignore on read.
        fs_valid: True if full scale values have meaning.
        top_full_scale:
        bot_full_scale: The min full scale value for wave.
        use_bits: Used in memory only. Write zero. Ignore on read. (char)
        kind_bits: Reserved. Write zero. Ignore on read. (char)
        formula:
        dep_id: Used in memory only. Write zero. Ignore on read.
        creation_date: DateTime of creation. Not used in version 1 files.
        w_unused:
        mod_date: DateTime of last modification.
        wave_note_h:
    """

    type_: int
    next: int
    bname: str
    wh_version: int
    src_fldr: int
    file_name: int
    data_units: str
    x_units: str
    npnts: int
    a_modified: int
    hs_a: float
    hs_b: float
    w_modified: int
    sw_modified: int
    fs_valid: int
    top_full_scale: float
    bot_full_scale: float
    use_bits: int
    kind_bits: int
    formula: int
    dep_id: int
    creation_date: int
    w_unused: str
    mod_date: int
    wave_note_h: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        type_ = cursor.read_i16_le()
        next = cursor.read_u32_le()
        bname = cursor.read_string(20)
        wh_version = cursor.read_i16_le()
        src_fldr = cursor.read_i16_le()
        file_name = cursor.read_u32_le()
        data_units = cursor.read_string(4)
        x_units = cursor.read_string(4)
        npnts = cursor.read_i32_le()
        a_modified = cursor.read_i16_le()
        hs_a = cursor.read_f64_le()
        hs_b = cursor.read_f64_le()
        w_modified = cursor.read_i16_le()
        sw_modified = cursor.read_i16_le()
        fs_valid = cursor.read_i16_le()
        top_full_scale = cursor.read_f64_le()
        bot_full_scale = cursor.read_f64_le()

        use_bits = cursor.read_u8_le()
        kind_bits = cursor.read_u8_le()

        formula = cursor.read_u32_le()
        dep_id = cursor.read_i32_le()
        creation_date = cursor.read_u32_le()
        w_unused = cursor.read_string(2)
        mod_date = cursor.read_u32_le()
        wave_note_h = cursor.read_u32_le()

        return cls(
            type_,
            next,
            bname,
            wh_version,
            src_fldr,
            file_name,
            data_units,
            x_units,
            npnts,
            a_modified,
            hs_a,
            hs_b,
            w_modified,
            sw_modified,
            fs_valid,
            top_full_scale,
            bot_full_scale,
            use_bits,
            kind_bits,
            formula,
            dep_id,
            creation_date,
            w_unused,
            mod_date,
            wave_note_h,
        )


@dataclass
class WaveHeaderV5:
    """Version 5 wave header."""

    next: int
    creation_date: int
    mod_date: int
    npnts: int
    type_: int
    d_lock: int
    whpad1: str
    wh_version: int
    bname: str
    whpad2: int
    data_folder: int
    n_dim: tuple[int, int, int, int]
    sf_a: tuple[float, float, float, float]
    sf_b: tuple[float, float, float, float]
    data_units: str
    dim_units: tuple[
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
        tuple[int, int, int, int],
    ]
    fs_valid: int
    whpad3: int
    top_full_scale: float
    bot_full_scale: float
    data_e_units: int
    dim_e_units: tuple[int, int, int, int]
    dim_labels: tuple[int, int, int, int]
    wave_note_h: int
    wh_unused: tuple[int, int, int, int]
    a_modified: int
    w_modified: int
    sw_modified: int
    use_bits: int  # char
    kind_bits: int  # char
    formula: int
    dep_id: int
    whpad4: int
    src_fldr: int
    file_name: int
    s_indeces: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        next = cursor.read_u32_le()
        creation_date = cursor.read_u32_le()
        mod_date = cursor.read_u32_le()
        npnts = cursor.read_i32_le()
        type_ = cursor.read_i16_le()
        d_lock = cursor.read_i16_le()
        whpad1 = cursor.read_string(6)
        wh_version = cursor.read_i16_le()
        bname = cursor.read_string(32)
        whpad2 = cursor.read_i32_le()
        data_folder = cursor.read_u32_le()

        n_dim = tuple(cursor.read_u32_le() for _ in range(4))
        sf_a = tuple(cursor.read_f64_le() for _ in range(4))
        sf_b = tuple(cursor.read_f64_le() for _ in range(4))

        data_units = cursor.read_string(4)

        dim_units = tuple(
            tuple(cursor.read_u8_le() for _ in range(4)) for _ in range(4)
        )

        fs_valid = cursor.read_i16_le()
        whpad3 = cursor.read_i16_le()
        top_full_scale = cursor.read_f64_le()
        bot_full_scale = cursor.read_f64_le()
        data_e_units = cursor.read_u32_le()

        dim_e_units = tuple(cursor.read_u32_le() for _ in range(4))
        dim_labels = tuple(cursor.read_u32_le() for _ in range(4))

        wave_note_h = cursor.read_u32_le()

        wh_unused = [cursor.read_i32_le() for _ in range(16)]

        a_modified = cursor.read_i16_le()
        w_modified = cursor.read_i16_le()
        sw_modified = cursor.read_i16_le()

        use_bits = cursor.read_u8_le()

        kind_bits = cursor.read_u8_le()

        formula = cursor.read_u32_le()
        dep_id = cursor.read_i32_le()
        whpad4 = cursor.read_i16_le()
        src_fldr = cursor.read_i16_le()
        file_name = cursor.read_u32_le()
        s_indeces = cursor.read_i32_le()

        return cls( next,
            creation_date,
            mod_date,
            npnts,
            type_,
            d_lock,
            whpad1,
            wh_version,
            bname,
            whpad2,
            data_folder,
            n_dim,  # pyright: ignore[reportArgumentType]
            sf_a,  # pyright: ignore[reportArgumentType]
            sf_b,  # pyright: ignore[reportArgumentType]
            data_units,
            dim_units,  # pyright: ignore[reportArgumentType]
            fs_valid,
            whpad3,
            top_full_scale,
            bot_full_scale,
            data_e_units,
            dim_e_units,  # pyright: ignore[reportArgumentType]
            dim_labels,  # pyright: ignore[reportArgumentType]
            wave_note_h,
            wh_unused,  # pyright: ignore[reportArgumentType]
            a_modified,
            w_modified,
            sw_modified,
            use_bits,
            kind_bits,
            formula,
            dep_id,
            whpad4,
            src_fldr,
            file_name,
            s_indeces,
        )


WaveHeader = WaveHeaderV2 | WaveHeaderV5


class Ibw:
    """Class representing an Igore binary wave file (ibw)."""
    # mod_date:
    bname: str
    creation_date: int
    npnts: int
    n_dim: tuple[int, int, int, int]
    x_step: tuple[float, float, float, float]
    x_start: tuple[float, float, float, float]
    data_units: str
    note: str
    extended_data_units: str | None
    dim_e_units: list[str] | None
    dim_labels: list[str] | None
    data: list[float]

    def __init__(self, filepath: str):
        with open(filepath, "rb") as f:
            cursor = Cursor(f)
            wave = read_binary_wave(cursor)
            wave_header = wave.wave_header

            self.npnts = wave_header.npnts
            self.data = wave.data
            self.bname = wave_header.bname
            self.creation_date = wave_header.creation_date
            self.note = wave.note
            self.extended_data_units = wave.extended_data_units
            self.dim_e_units = wave.dim_e_units
            self.dim_labels = wave.dim_labels

            self.n_dim = (
                wave_header.n_dim
                if isinstance(wave_header, WaveHeaderV5)
                else (wave_header.npnts, 0, 0, 0)
            )
            self.x_step = (
                wave_header.sf_a
                if isinstance(wave_header, WaveHeaderV5)
                else (wave_header.hs_a, 0, 0, 0)
            )
            self.x_start = (
                wave_header.sf_b
                if isinstance(wave_header, WaveHeaderV5)
                else (wave_header.hs_b, 0, 0, 0)
            )
            self.data_units = wave_header.data_units

    @override
    def __repr__(self) -> str:
        attributes = "\n".join(
            f"{k} = {v!r}" for k, v in self.__dict__.items() if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({attributes}\n)"


@dataclass
class BinaryWave:
    bin_header: BinHeader
    wave_header: WaveHeader
    note: str
    extended_data_units: str
    dim_e_units: list[str]
    dim_labels: list[str]
    data: list[float]


def read_binary_wave(cursor: Cursor) -> BinaryWave:
    # file_len = len(f)
    current_pos = cursor.position()
    version = cursor.read_i16_le()
    cursor.set_position(current_pos)

    bin_header = None
    wave_header = None
    match version:
        case 2:
            bin_header = BinHeaderV2.from_buffer(cursor)
            wave_header = WaveHeaderV2.from_buffer(cursor)
        case 5:
            bin_header = BinHeaderV5.from_buffer(cursor)
            wave_header = WaveHeaderV5.from_buffer(cursor)
        case _:
            raise ValueError("Not a version 2 or version 5 bin header or wave header")

    # TODO reshape data maybe?
    data = read_numeric_data(cursor, wave_header.type_, wave_header.npnts)

    # Version 1, 2 and 3 have 16 bytes of padding after numeric wave data.
    if version in [1, 2, 3]:
        pos = cursor.position()
        cursor.set_position(pos + 16)

    # Optional Data
    # v1: No optional data
    # v2: Wave note data
    # v3: Wave note data, wave dependency formula
    # v5: Wave dependency formula, wave note data, extended data units data, extended dimension units data, dimension label data, String indices used for text waves only

    note = read_note(cursor, bin_header.note_size)
    extended_data_units = read_extended_data_units(cursor, bin_header)
    dim_e_units = read_dim_e_units(cursor, bin_header)
    dim_labels = read_dim_labels(cursor, bin_header)

    return BinaryWave(
        bin_header,
        wave_header,
        note,
        extended_data_units,
        dim_e_units,
        dim_labels,
        data,
    )


def read_note(cursor: Cursor, note_size: int) -> str:
    note = ""
    if note_size != 0:
        note = cursor.read_string(note_size).replace("\r", "\n")

    return note


def read_extended_data_units(cursor: Cursor, bin_header: BinHeader) -> str:
    match bin_header:
        case BinHeaderV5(_) if bin_header.data_e_units_size != 0:
            extended_data_units = cursor.read_string(bin_header.data_e_units_size)
        case _:
            extended_data_units = ""

    return extended_data_units


def read_dim_e_units(cursor: Cursor, bin_header: BinHeader) -> list[str]:
    # Original: Fixed length array of size 4.
    dim_e_units: list[str] = []
    if isinstance(bin_header, BinHeaderV5):
        for i in bin_header.dim_e_units_size:
            if i != 0:
                dim_e_units.append(cursor.read_string(i))

    return dim_e_units


def read_dim_labels(cursor: Cursor, bin_header: BinHeader) -> list[str]:
    # Original: Fixed length array of size 4.
    dim_labels: list[str] = []
    if isinstance(bin_header, BinHeaderV5):
        for i in bin_header.dim_e_units_size:
            if i != 0:
                dim_labels.append(cursor.read_string(i))

    return dim_labels


def read_numeric_data(
    cursor: Cursor, data_type: int, num_data_points: int
) -> list[float]:
    data = None
    match data_type:
        case 0:
            raise NotImplementedError("Text Wave")
        case 1:
            raise NotImplementedError("Complex")
        case 2:
            data = [cursor.read_f32_le() for _ in range(num_data_points)]
        case 3:
            raise NotImplementedError("Complex 64")
        case 4:
            data = [cursor.read_f64_le() for _ in range(num_data_points)]
        case 5:
            raise NotImplementedError("Complex 128")
        case 8:
            data = [cursor.read_i8_le() for _ in range(num_data_points)]
        case 9:
            raise NotImplementedError("Complex Int8")
        case 0x10:
            data = [cursor.read_i16_le() for _ in range(num_data_points)]
        case 0x11:
            raise NotImplementedError("Complex Int16")
        case 0x20:
            data = [cursor.read_i32_le() for _ in range(num_data_points)]
        case 0x21:
            raise NotImplementedError("Complex Int32")
        case 0x48:
            data = [cursor.read_u8_le() for _ in range(num_data_points)]
        case 0x49:
            raise NotImplementedError("Complex UInt8")
        case 0x50:
            data = [cursor.read_u16_le() for _ in range(num_data_points)]
        case 0x51:
            raise NotImplementedError("Complex UInt16 Data")
        case 0x60:
            data = [cursor.read_u32_le() for _ in range(num_data_points)]
        case 0x61:
            raise NotImplementedError("Complex UInt32 Data")
        case _:
            raise ValueError("Unknown data type")

    return [float(i) for i in data]
