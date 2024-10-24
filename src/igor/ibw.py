from dataclasses import dataclass
from typing import Self

from igor.cursor import Cursor


@dataclass
class BinHeaderV1:
    version: int  # Version number for backwards compatibility.
    wfm_size: int  # The size of the WaveHeader2 data classure plus the wave data plus 16 bytes of padding.
    checksum: int  # Checksum over this header and the wave header.


@dataclass
class BinHeaderV2:
    version: int  # Version number for backwards compatibility.
    wfm_size: int  # The size of the WaveHeader2 data classure plus the wave data plus 16 bytes of padding.
    note_size: int  # The size of the note text.
    pict_size: int  # Reserved. Write zero. Ignore on read.
    checksum: int  # Checksum over this header and the wave header.

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
    version: int  # Version number for backwards compatibility.
    wfm_size: int  # The size of the WaveHeader2 data classure plus the wave data plus 16 bytes of padding.
    note_size: int  # The size of the note text.
    formula_size: int  # The size of the dependency formula, if any.
    pict_size: int  # Reserved. Write zero. Ignore on read.
    checksum: int  # Checksum over this header and the wave header.


@dataclass
class BinHeaderV5:
    version: int  # Version number for backwards compatibility.
    checksum: int  # Checksum over this header and the wave header.
    wfm_size: int  # The size of the WaveHeader5 data classure plus the wave data.
    formula_size: int  # The size of the dependency formula, if any.
    note_size: int  # The size of the note text.
    data_e_units_size: int  # The size of optional extended data units.
    dim_e_units_size: tuple[
        int, int, int, int
    ]  # The size of optional extended dimension units.
    dim_labels_size: tuple[int, int, int, int]  # The size of optional dimension labels.
    s_indices_size: int  # The size of string indicies if this is a text wave.
    options_size_1: int  # Reserved. Write zero. Ignore on read.
    options_size_2: int  # Reserved. Write zero. Ignore on read.

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
    type_: int  # See types (e.g. NT_FP64) above. Zero for text waves.
    next: int
    bname: str
    wh_version: int  # Write 0. Ignore on read.
    src_fldr: int  # Used in memory only. Write zero. Ignore on read.
    file_name: int
    data_units: str
    x_units: str
    npnts: int  # Number of data points in wave.
    a_modified: int  # Used in memory only. Write zero. Ignore on read.
    hs_a: float
    hs_b: float  # X value for point p = hsA*p + hsB
    w_modified: int  # Used in memory only. Write zero. Ignore on read.
    sw_modified: int  # Used in memory only. Write zero. Ignore on read.
    fs_valid: int  # True if full scale values have meaning.
    top_full_scale: float
    bot_full_scale: float  # The min full scale value for wave.
    use_bits: int  # Used in memory only. Write zero. Ignore on read. (char)
    kind_bits: int  # Reserved. Write zero. Ignore on read. (char)
    formula: int
    dep_id: int  # Used in memory only. Write zero. Ignore on read.
    creation_date: int  # DateTime of creation. Not used in version 1 files.
    w_unused: str
    mod_date: int  # DateTime of last modification.
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
        # mut use_bits = [0_u8 1];
        #    cursor.read_exact(&mut use_bits).unwrap()

        kind_bits = cursor.read_u8_le()
        # mut kind_bits = [0_u8 1];
        #    cursor.read_exact(&mut kind_bits).unwrap()

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
    sf_a: tuple[int, int, int, int]
    sf_b: tuple[int, int, int, int]
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
    use_bits: int  # (char)
    kind_bits: int  # (char)
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
        #     mut dim_units = [[0_u8; 4]; 4]
        # for i in dim_units.iter_mut() {
        #     cursor.read_exact(i).unwrap()
        # }

        fs_valid = cursor.read_i16_le()
        whpad3 = cursor.read_i16_le()
        top_full_scale = cursor.read_f64_le()
        bot_full_scale = cursor.read_f64_le()
        data_e_units = cursor.read_u32_le()

        dim_e_units = tuple(cursor.read_u32_le() for _ in range(4))
        dim_labels = tuple(cursor.read_u32_le() for _ in range(4))

        wave_note_h = cursor.read_u32_le()

        wh_unused = [cursor.read_i32_le() for _ in range(16)]
        #     mut wh_unused = [0_i32; 16]
        # for i in wh_unused.iter_mut() {
        #     *i = cursor.read_i32_le()
        # }
        a_modified = cursor.read_i16_le()
        w_modified = cursor.read_i16_le()
        sw_modified = cursor.read_i16_le()

        use_bits = cursor.read_u8_le()
        #     mut use_bits = [0_u8; 1]
        # cursor.read_exact(&mut use_bits).unwrap()

        kind_bits = cursor.read_u8_le()
        #     mut kind_bits = [0_u8; 1]
        # cursor.read_exact(&mut kind_bits).unwrap()
        formula = cursor.read_u32_le()
        dep_id = cursor.read_i32_le()
        whpad4 = cursor.read_i16_le()
        src_fldr = cursor.read_i16_le()
        file_name = cursor.read_u32_le()
        s_indeces = cursor.read_i32_le()

        return cls(
            next,
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
    # creation_date:
    # mod_date:
    npnts: int
    bname: str
    n_dim: tuple[int, int, int, int]
    x_step: tuple[float, float, float, float]
    x_start: tuple[float, float, float, float]
    data_units: str
    data: list[float]
    note: str
    extended_data_units: str | None
    dim_e_units: list[str] | None
    dim_labels: list[str] | None

    def __init__(self, filepath: str):
        with open(filepath, "rb") as f:
            cursor = Cursor(f)
            # file_len = len(f)
            version = cursor.read_i16_le()
            cursor.set_position(0)

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
                    raise ValueError(
                        "Not a version 2 or version 5 bin header or wave header"
                    )

            self.npnts = wave_header.npnts
            type_ = wave_header.type_

            # TODO reshape data maybe
            self.data = self.read_numeric_data(cursor, type_, self.npnts)

            # version 1, 2 and 3 have 16 bytes of padding after numeric wave data
            if version in [1, 2, 3]:
                pos = cursor.position()
                cursor.set_position(pos + 16)

            # Optional Data
            # v1: no optional data
            # v2: wave note data
            # v3: wave note data, wave dependency formula
            # v5: wave dependency formula, wave note data, extended data units data, extended dimension units data, dimension label data, String indices used for text waves only

            self.note = self.read_note(cursor, bin_header.note_size)
            self.extended_data_units = self.read_extended_data_units(cursor, bin_header)
            self.dim_e_units = self.read_dim_e_units(cursor, bin_header)
            self.dim_labels = self.read_dim_labels(cursor, bin_header)
            self.bname = wave_header.bname

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

            # let bname = match &wave_header {
            #     WaveHeader::V2(wh) => wh.bname.trim_matches(char::from(0)).to_string(),
            #     WaveHeader::V5(wh) => wh.bname.trim_matches(char::from(0)).to_string(),
            # };
            # let n_dim = match &wave_header {
            #     WaveHeader::V2(wh) => [wh.npnts, 0, 0, 0],
            #     WaveHeader::V5(wh) => wh.n_dim,
            # };
            # let x_step = match &wave_header {
            #     WaveHeader::V2(wh) => [wh.hs_a, 0_f64, 0_f64, 0_f64],
            #     WaveHeader::V5(wh) => wh.sf_a,
            # };
            # let x_start = match &wave_header {
            #     WaveHeader::V2(wh) => [wh.hs_b, 0_f64, 0_f64, 0_f64],
            #     WaveHeader::V5(wh) => wh.sf_b,
            # };
            # let data_units = match &wave_header {
            #     WaveHeader::V2(wh) => wh.data_units.trim_matches(char::from(0)).to_string(),
            #     WaveHeader::V5(wh) => wh.data_units.trim_matches(char::from(0)).to_string(),
            # };

            # Ok(Ibw {
            #     npnts,
            #     bname,
            #     n_dim,
            #     x_step,
            #     x_start,
            #     data_units,
            #     data,
            #     note,
            #     extended_data_units,
            #     dim_e_units,
            #     dim_labels,
            # })

    def read_numeric_data(
        self, cursor: Cursor, data_type: int, num_data_points: int
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

    def read_note(self, cursor: Cursor, note_size: int) -> str:
        note = ""
        if note_size != 0:
            note = cursor.read_string(note_size).replace("\r", "\n")

        return note

    def read_extended_data_units(self, cursor: Cursor, bin_header: BinHeader) -> str:
        match bin_header:
            case BinHeaderV5(_) if bin_header.data_e_units_size != 0:
                extended_data_units = cursor.read_string(bin_header.data_e_units_size)
            case _:
                extended_data_units = ""

        return extended_data_units

    def read_dim_e_units(self, cursor: Cursor, bin_header: BinHeader) -> list[str]:
        # In C code this is a fixed length array of size 4. Here, it will be of variable length
        dim_e_units: list[str] = []
        if isinstance(bin_header, BinHeaderV5):
            for i in bin_header.dim_e_units_size:
                if i != 0:
                    dim_e_units.append(cursor.read_string(i))

        return dim_e_units

    def read_dim_labels(self, cursor: Cursor, bin_header: BinHeader) -> list[str]:
        # In C code this is a fixed length array of size 4. Here, it will be of variable length
        dim_labels: list[str] = []
        if isinstance(bin_header, BinHeaderV5):
            for i in bin_header.dim_e_units_size:
                if i != 0:
                    dim_labels.append(cursor.read_string(i))

        return dim_labels
