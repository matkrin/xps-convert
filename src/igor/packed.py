from dataclasses import dataclass
import os
from enum import Enum, auto
from typing import Self

from igor.cursor import Cursor
import igor.ibw


class PackedFileRecordType(Enum):
    """
    Igor writes other kinds of records in a packed experiment file, for storing
    things like pictures, page setup records, and miscellaneous settings. The
    format for these records is quite complex and is not described in PTN003.
    If you are writing a program to read packed files, you must skip any record
    with a record type that is not listed above.
    """

    kUnusedRecord = 0
    kVariablesRecord = auto()        # 1: Contains system numeric variables (e.g., K0) and user numeric and string variables.
    kHistoryRecord = auto()          # 2: Contains the experiment's history as plain text.
    kWaveRecord = auto()             # 3: Contains the data for a wave
    kRecreationRecord = auto()       # 4: Contains the experiment's recreation procedures as plain text.
    kProcedureRecord = auto()        # 5: Contains the experiment's main procedure window text as plain text.
    kUnused2Record = auto()
    kGetHistoryRecord = auto()       # 6: Not a real record but rather, a message to go back and read the history text.
    kPackedFileRecord = auto()       # 7: Contains the data for a procedure file or notebook in a packed form.
    kDataFolderStartRecord = auto()  # 8: Marks the start of a new data folder.
    kDataFolderEndRecord = auto()    # 10: Marks the end of a data folder.


@dataclass
class PackedFileRecordHeader:
    record_type: int  # u16
    version: int  # i16
    num_data_bytes: int  # i32

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        record_type = cursor.read_u16_le() & 0x7FFF
        version = cursor.read_i16_le()
        num_data_bytes = cursor.read_i32_le()
        return cls(record_type, version, num_data_bytes)

@dataclass
class VarHeader1:
    """ This is the header written at the start of the version 1 variables record,
	before the actual variable data.

	The entire variables record on disk consists of:
		PackedFileRecordHeader of type kVariablesRecord

		numSysVars system variables written as floats in order (K0, K1 . . . K19).

		numUserVars user numeric variables, each written as a UserNumVarRec record.

		numUserStrs user string variables, each consisting of a UserStrVarRec record.
    """
    version: int
    num_sys_vars: int
    num_user_vars: int
    num_user_strs: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        version = cursor.read_i16_le()  # Version number is 1 for this header.
        num_sys_vars = cursor.read_i16_le()  # Number of system variables (K0, K1 . . .).
        num_user_vars = cursor.read_i16_le()  # Number of user numeric variables -- may be zero.
        num_user_strs = cursor.read_i16_le()  # Number of user string variables -- may be zero.
        return cls(version, num_sys_vars, num_user_vars, num_user_strs)


@dataclass
class UserStrVarRec1:
    """This header precedes each user string variable in a version 2 variables record. """
    name: str
    str_len: int
    data: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        name = cursor.read_string(32)  # Name of the string variable.
        str_len = cursor.read_i16_le()  # The real size of the following array.
        data = cursor.read_string(1)
        return cls(name, str_len, data)


@dataclass
class VarHeader2:
    """ This is the header written at the start of the version 2 variables record,
	before the actual variable data.

	The entire variables record on disk consists of:
		PackedFileRecordHeader of type kVariablesRecord

		numSysVars system variables written as floats in order (K0, K1 . . . K19).

		numUserVars user numeric variables, each written as a UserNumVarRec record.

		numUserStrs user string variables, each consisting of a UserStrVarRec record.

		numDependentVars user dependent numeric variables, each consisting of a UserDependentVarRec record.

		numDependentStrs user dependent string variables, each consisting of a UserDependentVarRec record.
    """
    version: int
    num_sys_vars: int
    num_user_vars: int
    num_user_strs: int
    num_dependent_vars: int
    num_dependent_strs: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        version = cursor.read_i16_le()
        num_sys_vars = cursor.read_i16_le()
        num_user_vars = cursor.read_i16_le()
        num_user_strs = cursor.read_i16_le()
        num_dependent_vars = cursor.read_i16_le()
        num_dependent_strs = cursor.read_i16_le()
        return cls(version, num_sys_vars, num_user_vars, num_user_strs, num_dependent_vars, num_dependent_strs)


@dataclass
class UserStrVarRec2:
    """ This header precedes each user string variable in a version 2 variables record."""
    name: str
    str_len: int #long
    data: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        name = cursor.read_string(32)
        str_len = cursor.read_i32_le()
        data = cursor.read_string(1)
        return cls(name, str_len, data)


@dataclass
class VarNumRec:
    num_type: int # short
    real_part: float # double
    imag_part: float # double
    reserved: int # long

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        num_type = cursor.read_i16_le()
        real_part = cursor.read_f64_le()
        imag_part = cursor.read_f64_le()
        reserved = cursor.read_i32_le()
        return cls(num_type, real_part, imag_part, reserved)

@dataclass
class UserNumVarRec:
    """ This header precedes each user numeric variable."""
    name: str
    type_: int #short
    num: VarNumRec

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        name = cursor.read_string(32)
        type_ = cursor.read_i16_le()
        num = VarNumRec.from_buffer(cursor)
        return cls(name, type_, num)

@dataclass
class UserDependentVarRec:
    """ This header precedes each user dependent numeric or string variable.
	A dependent variable is one controlled by a dependency formula,
	such as:
		numVar0 := 2*numVar1
    """
    name: str
    type_: int # short
    num: VarNumRec
    formula_len: int # short
    formula: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> Self:
        name = cursor.read_string(32)
        type_ = cursor.read_i16_le()
        num = VarNumRec.from_buffer(cursor)
        formula_len = cursor.read_i16_le()
        formula = cursor.read_string(1)
        return cls(name, type_, num, formula_len, formula)


class PackedFile:
    def __init__(self, filepath: str):
        self.records: list[igor.ibw.BinaryWave] = []
        with open(filepath, "rb") as f:
            file_size = os.path.getsize(filepath)
            cursor = Cursor(f)

            while cursor.position() < file_size:
                file_record_header = PackedFileRecordHeader.from_buffer(cursor)
                print(f"{file_record_header=}")

                match PackedFileRecordType(file_record_header.record_type):
                    # case PackedFileRecordType.kVariablesRecord:
                    #     version = cursor.read_i16_le()
                    #     print(f"{version=}")
                    #     cursor.set_position(cursor.position() - 2)
                    #
                    #     match version:
                    #         case 1:
                    #             var_header = VarHeader1.from_buffer(cursor)
                    #         case 2:
                    #             var_header = VarHeader2.from_buffer(cursor)
                    #         case _:
                    #             raise ValueError(f"Unknown VarHeader version: {version}")
                    #
                    #     print(f"{var_header=}")
                    #     sys_vars = [cursor.read_f32_le() for _ in range(var_header.num_sys_vars)]
                    #     user_vars = [UserNumVarRec.from_buffer(cursor) for _ in range(var_header.num_user_vars)]
                    #
                    #     user_strs: list[UserStrVarRec1 | UserStrVarRec2] = []
                    #     for _ in range(var_header.num_user_strs):
                    #         match version:
                    #             case 1:
                    #                 user_str = UserStrVarRec1.from_buffer(cursor)
                    #             case 2:
                    #                 user_str = UserStrVarRec2.from_buffer(cursor)
                    #
                    #         user_strs.append(user_str)
                    #
                    #     if isinstance(var_header, VarHeader2):
                    #         user_dependent_vars = [UserDependentVarRec.from_buffer(cursor) for _ in range(var_header.num_dependent_vars)]
                    #         user_dependent_strs = [UserDependentVarRec.from_buffer(cursor) for _ in range(var_header.num_dependent_strs)]
                    #
                    #
                    # case PackedFileRecordType.kHistoryRecord:
                    #     history_record = cursor.read_string(file_record_header.num_data_bytes)

                    case PackedFileRecordType.kWaveRecord:
                        position = cursor.position()
                        wave_record = igor.ibw.read_binary_wave(cursor)
                        self.records.append(wave_record)
                        cursor.set_position(position + file_record_header.num_data_bytes)

                    case _:
                        cursor.set_position(cursor.position() + file_record_header.num_data_bytes)

            print(len(self.records))
            for record in self.records:
                print(record)
                print("-" * 80)
