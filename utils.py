import os
import struct

class ReadableWriteableStream:
    def __init__(self, file):
        self.file = file

    def read(self, size):
        return self.file.read(size)

    def write(self, data):
        self.file.write(data)

    def seek(self, offset, whence=os.SEEK_SET):
        self.file.seek(offset, whence)

    def tell(self):
        return self.file.tell()

    def skip(self, offset):
        self.file.seek(offset, os.SEEK_CUR)

    def read_u8(self):
        return struct.unpack("<B", self.read(1))[0]

    def read_u16(self):
        return struct.unpack("<H", self.read(2))[0]

    def read_u32(self):
        return struct.unpack("<I", self.read(4))[0]

    def read_string(self, size):
        data = self.read(size)
        idx = data.find(b'\x00')
        if idx != -1:
            data = data[:idx]
        return data.decode("utf-8")

class SeekContext:
    def __init__(self, stream):
        self.stream = stream
        self.offset = stream.tell()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.seek(self.offset)

class RelativeSeekContext:
    def __init__(self, stream, offset):
        self.stream = stream
        self.return_offset = stream.tell()
        self.seek_offset = offset

    def __enter__(self):
        self.stream.skip(self.seek_offset)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.seek(self.return_offset)
