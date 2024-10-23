from io import BufferedReader
import struct
from typing import cast


class Cursor:
    """Class for handeling a buffer"""

    def __init__(self, buffer: BufferedReader):
        self._buffer = buffer

    def position(self) -> int:
        """Get the current postition of the cursor

        Returns:
            int: The current cursor position
        """
        return self._buffer.tell()

    def set_position(self, position: int) -> None:
        """Set the postition of the cursor

        Args:
            position: Byte-position to set
        """
        _ = self._buffer.seek(position)

    def skip(self, bytes_to_skip: int) -> None:
        """Skip bytes of the buffer

        Args:
            bytes_to_skip: Number of bytes to skip
        """
        self.set_position(self._buffer.tell() + bytes_to_skip)

    def read(self, num_bytes: int) -> bytes:
        """Read bytes, while moving cursor

        Args:
            num_bytes: Number of bytes to read

        Returns:
            bytes: The read bytes
        """
        return self._buffer.read(num_bytes)

    def read_string(self, str_len: int) -> str:
        """Read bytes as string

        Args:
            str_len: Length of the string to read

        Returns:
            The read string
        """
        return "".join([chr(i).rstrip("\x00") for i in self._buffer.read(str_len)])
        # bytes_ = self._buffer.read(str_len)
        # return bytes_.decode("utf-8").rstrip("\x00")

    def read_sm4_string(self) -> str:
        """Read bytes as a UTF-16 encoded string. In SM4-files string data
        always contains the length of the string as a u16 number, followed
        by the string itself

        Returns:
            The read string
        """
        length = self.read_u16_le()
        return self.read_string(length * 2).strip()

    def read_u8_le(self) -> int:
        """Read a 8-bit unsigned integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<B", self._buffer.read(1))[0])

    def read_i8_le(self) -> int:
        """Read a 8-bit signed integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<b", self._buffer.read(1))[0])

    def read_u16_le(self) -> int:
        """Read a 16-bit unsigned integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<H", self._buffer.read(2))[0])

    def read_i16_le(self) -> int:
        """Read a 16-bit signed integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<h", self._buffer.read(2))[0])

    def read_u32_le(self) -> int:
        """Read a 32-bit unsigned integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<I", self._buffer.read(4))[0])

    def read_i32_le(self) -> int:
        """Read a 32-bit signed integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<i", self._buffer.read(4))[0])

    def read_u64_le(self) -> int:
        """Read a 64-bit unsigned integer

        Returns:
            The read integer
        """
        return cast(int, struct.unpack("<q", self._buffer.read(8))[0])

    def read_f32_le(self) -> float:
        """Read a 64-bit floating point number

        Returns:
            The read float
        """
        return cast(float, struct.unpack("<f", self._buffer.read(4))[0])

    def read_f64_le(self) -> float:
        """Read a 64-bit floating point number

        Returns:
            The read float
        """
        return cast(float, struct.unpack("<d", self._buffer.read(8))[0])
