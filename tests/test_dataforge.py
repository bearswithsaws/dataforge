# pylint: disable=too-few-public-methods
"""DataForge test suite
"""
import pytest

from dataforge import *  # pylint: disable=W0401,W0614
from dataforge.exceptions import DFRangeException


class TestDFUInt8():
    """Test unsigned int 8-bit"""

    def test(self):
        df_test = DFUInt8(value=0xFF)
        assert b"\xff" == df_test.pack()

        df_test = DFUInt8(value=b"\xaa")
        assert b"\xaa" == df_test.pack()

        with pytest.raises(DFRangeException):
            DFUInt8(value=b"abc")

        # Test that too large of a value is truncated
        df_test = DFUInt8(value=0x105)
        assert b"\x05" == df_test.pack()

        assert df_test.length == 1


class TestDFSInt8():
    """Test signed int 8-bit"""

    def test(self):
        df_test = DFSInt8(value=-1)
        assert b"\xff" == df_test.pack()

        df_test = DFSInt8(value=b"\x7f")
        assert b"\x7f" == df_test.pack()

        with pytest.raises(DFRangeException):
            df_test = DFSInt8(value=b"abc")

        # Test that too large of a value is truncated
        df_test = DFSInt8(value=-0x105)
        assert b"\xfb" == df_test.pack()

        assert df_test.length == 1


class TestDFUInt16():
    """Test unsigned int 16-bit"""

    def test(self):
        df_test = DFUInt16(value=0x1234)
        assert b"\x34\x12" == df_test.pack()

        df_test = DFUInt16(value=0x1234, endian=DFEndian.BIG)
        assert b"\x12\x34" == df_test.pack()

        df_test = DFUInt16(value=b"\xbb\xaa", endian=DFEndian.LITTLE)
        assert b"\xbb\xaa" == df_test.pack()

        df_test = DFUInt16(value=b"\xbb\xaa", endian=DFEndian.BIG)
        assert b"\xaa\xbb" == df_test.pack()

        df_test = DFUInt16(value=1, endian=DFEndian.LITTLE)
        assert b"\x01\x00" == df_test.pack()

        with pytest.raises(DFRangeException):
            df_test = DFUInt16(value=b"abcd")

        # Test that too large of a value is truncated
        df_test = DFUInt16(value=0x100000005)
        assert b"\x05\x00" == df_test.pack()

        assert df_test.length == 2


class TestDFSInt16():
    """Test signed int 16-bit"""

    def test(self):
        df_test = DFSInt16(value=0x1234)
        assert b"\x34\x12" == df_test.pack()

        df_test = DFSInt16(value=0x1234, endian=DFEndian.BIG)
        assert b"\x12\x34" == df_test.pack()

        df_test = DFSInt16(value=b"\xbb\x7f", endian=DFEndian.LITTLE)
        assert b"\xbb\x7f" == df_test.pack()

        df_test = DFSInt16(value=b"\xbb\x7f", endian=DFEndian.BIG)
        assert b"\x7f\xbb" == df_test.pack()

        with pytest.raises(DFRangeException):
            df_test = DFSInt16(value=b"abcd")

        # Test that too large of a value is truncated
        df_test = DFSInt16(value=-0x10005)
        assert b"\xfb\xff" == df_test.pack()

        assert df_test.length == 2


class TestDFUInt32():
    """Test unsigned int 32-bit"""

    def test(self):
        df_test = DFUInt32(value=0x12345678)
        assert b"\x78\x56\x34\x12" == df_test.pack()

        df_test = DFUInt32(value=0x12345678, endian=DFEndian.BIG)
        assert b"\x12\x34\x56\x78" == df_test.pack()

        df_test = DFUInt32(value=b"\xdd\xcc\xbb\xaa", endian=DFEndian.LITTLE)
        assert b"\xdd\xcc\xbb\xaa" == df_test.pack()

        df_test = DFUInt32(value=b"\xdd\xcc\xbb\xaa", endian=DFEndian.BIG)
        assert b"\xaa\xbb\xcc\xdd" == df_test.pack()

        with pytest.raises(DFRangeException):
            df_test = DFUInt32(value=b"abcdef")

        # Test that too large of a value is truncated
        df_test = DFUInt32(value=0x100000005)
        assert b"\x05\x00\x00\x00" == df_test.pack()

        assert df_test.length == 4


class TestDFSInt32():
    """Test signed int 32-bit"""

    def test(self):
        df_test = DFSInt32(value=-1)
        assert b"\xff\xff\xff\xff" == df_test.pack()

        # Test that too large of a value is truncated
        df_test = DFSInt32(value=-0x100000005)
        assert b"\xfb\xff\xff\xff" == df_test.pack()


class TestDFContainer():
    """Test Container"""

    def test(self):
        df_test = DFContainer()
        df_test.add("test", DFUInt32(value=0x1337))
        assert b"\x37\x13\x00\x00" == df_test.pack()

        # Add a sub container
        df_test.add("sub", DFContainer())
        assert b"\x37\x13\x00\x00" == df_test.pack()

        df_test.add("sub.test_sub_container", DFContainer())
        assert b"\x37\x13\x00\x00" == df_test.pack()

        df_test.add("sub.test_sub_container.test", DFUInt16(value=0xAABB))
        assert b"\x37\x13\x00\x00\xbb\xaa" == df_test.pack()

        df_test.add("sub.test_sub_container.another", DFUInt16(value=0xCCDD))
        assert b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc" == df_test.pack()

        df_test.add("upper", DFUInt8(value=b"A"))
        assert b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x41" == df_test.pack()

        df_test.add("sub.inner_insert", DFUInt8(value=b"B"))
        assert b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x42\x41" == df_test.pack()

        df_test = DFContainer()
        df_test.test = DFUInt32(value=0x1337)
        df_test.test2 = DFUInt8(value=b"A")
        df_test.sub = DFContainer()
        df_test.sub.test_sub = DFContainer()
        df_test.sub.test_val = DFUInt16(value=0xAABB)
        df_test.sub.another_sub = DFContainer()
        df_test.sub.another_sub.sub_item = DFUInt8(value=1)
        df_test.sub.another_sub.sub_item2 = DFUInt8(value=2)
        df_test.sub.test_sub.sub_sub = DFContainer()
        df_test.sub.test_sub.sub_sub.deep_value = DFUInt32(value=0xEEFF)


class TestDFContainerShorthand():
    """Test Container shorthand syntax"""

    def test(self):
        # Shorthand
        df_test = DFContainer()
        df_test.test = DFUInt32(value=0x1337)
        assert b"\x37\x13\x00\x00" == df_test.pack()

        # Add a sub caontianer
        df_test.sub = DFContainer()
        assert b"\x37\x13\x00\x00" == df_test.pack()

        df_test.sub.test_sub_container = DFContainer()
        assert b"\x37\x13\x00\x00" == df_test.pack()

        df_test.sub.test_sub_container.test = DFUInt16(value=0xAABB)
        assert b"\x37\x13\x00\x00\xbb\xaa" == df_test.pack()

        df_test.sub.test_sub_container.another = DFUInt16(value=0xCCDD)
        assert b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc" == df_test.pack()

        df_test.upper = DFUInt8(value=b"A")
        assert b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x41" == df_test.pack()

        df_test.sub.inner_insert = DFUInt8(value=b"B")
        assert b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x42\x41" == df_test.pack()

        df_test = DFContainer()
        df_test.add("test", DFUInt32(value=0x1337))
        df_test.add("test2", DFUInt8(value=b"A"))
        df_test.add("sub", DFContainer())
        df_test.add("sub.test_val", DFUInt16(value=0xAABB))
        df_test.add("sub.another_sub", DFContainer())
        df_test.add("sub.another_sub.sub_item", DFUInt8(value=1))
        df_test.add("sub.another_sub.sub_item2", DFUInt8(value=2))
        df_test.add("sub.test.sub_sub", DFContainer())
        df_test.add("sub.test.sub_sub.deep_value", DFUInt32(value=0xEEFF))


class TestDFLength():
    """Test length-counted container"""

    def test(self):
        df_test = DFContainer()
        df_test.len = DFLength(DFUInt16(), DFContainer())
        df_test.len.data = DFUInt32(value=0xAABBCCDD)
        df_test.len.data2 = DFUInt8(value=10)
        assert b"\x05\x00\xdd\xcc\xbb\xaa\x0a" == df_test.pack()

        df_test = DFContainer()
        df_test.len = DFLength(DFUInt16(endian=DFEndian.BIG), DFContainer())
        df_test.len.data = DFUInt32(value=0xAABBCCDD)
        df_test.len.data2 = DFUInt8(value=10)
        assert b"\x00\x05\xdd\xcc\xbb\xaa\x0a" == df_test.pack()


class TestDFLengthRef():
    """Test length-counted container"""

    def test(self):
        df_test = DFContainer()
        df_test.len = DFLengthRef(DFUInt16(), "len_data")
        df_test.len_data = DFContainer()
        df_test.len_data.data = DFUInt32(value=0xAABBCCDD)
        df_test.len_data.data2 = DFUInt8(value=10)
        # print(df_test.pretty_print())
        # print(df_test.pack())
        assert b"\x05\x00\xdd\xcc\xbb\xaa\x0a" == df_test.pack()

        df_test = DFContainer()
        df_test.len = DFLengthRef(DFUInt16(endian=DFEndian.BIG), "len_data")
        df_test.len_data = DFContainer()
        df_test.len_data.data = DFUInt32(value=0xAABBCCDD)
        df_test.len_data.data2 = DFUInt8(value=10)
        assert b"\x00\x05\xdd\xcc\xbb\xaa\x0a" == df_test.pack()

        df_test = DFContainer()
        df_test.something = DFUInt8(value=0x11)
        df_test.sub1 = DFContainer()
        df_test.sub1.thing1 = DFUInt16(value=7)
        df_test.sub1.len = DFLengthRef(DFUInt16(), "sub1.sub2.len_data")
        df_test.sub1.thing2 = DFUInt32(value=9)
        df_test.sub1.sub2 = DFContainer()
        df_test.sub1.sub2.len_data = DFContainer()
        df_test.sub1.sub2.len_data.data = DFUInt32(value=0xAABBCCDD)
        df_test.sub1.sub2.len_data.data2 = DFUInt8(value=10)
        # print(df_test.pretty_print())
        # print(df_test.pack())
        assert(
            b"\x11\x07\x00\x05\x00\x09\x00\x00\x00\xdd\xcc\xbb\xaa\x0a"
            == df_test.pack()
        )


def csum(data: bytes) -> int:
    checksum = 0
    for value in data:
        checksum += value
    return checksum


class TestDFCallableRef():
    """Test callable ref container"""

    def test(self):
        df_test = DFContainer()
        df_test.len = DFCallableRef(DFUInt16(), csum, "csum_data")
        df_test.csum_data = DFContainer()
        df_test.csum_data.data = DFUInt32(value=0xAABBCCDD)
        df_test.csum_data.data2 = DFUInt8(value=10)
        # print(df_test.pretty_print())
        # print(df_test.pack())
        assert b"\x18\x03\xdd\xcc\xbb\xaa\x0a" == df_test.pack()

        df_test = DFContainer()
        df_test.len = DFCallableRef(DFUInt16(endian=DFEndian.BIG), csum, "csum_data")
        df_test.csum_data = DFContainer()
        df_test.csum_data.data = DFUInt32(value=0xAABBCCDD)
        df_test.csum_data.data2 = DFUInt8(value=10)
        assert b"\x03\x18\xdd\xcc\xbb\xaa\x0a" == df_test.pack()

        df_test = DFContainer()
        df_test.something = DFUInt8(value=0x11)
        df_test.sub1 = DFContainer()
        df_test.sub1.thing1 = DFUInt16(value=7)
        df_test.sub1.len = DFCallableRef(DFUInt16(), csum, "sub1.sub2.csum_data")
        df_test.sub1.thing2 = DFUInt32(value=9)
        df_test.sub1.sub2 = DFContainer()
        df_test.sub1.sub2.csum_data = DFContainer()
        df_test.sub1.sub2.csum_data.data = DFUInt32(value=0xAABBCCDD)
        df_test.sub1.sub2.csum_data.data2 = DFUInt8(value=10)
        # print(df_test.pretty_print())
        # print(df_test.pack())
        assert(
            b"\x11\x07\x00\x18\x03\x09\x00\x00\x00\xdd\xcc\xbb\xaa\x0a"
            == df_test.pack()
        )


# class TestPrint():
#     """Test pretty-print"""

#     def test(self):
#         df_test = DFUInt8(value=0x41)
#         print(df_test)

#         df_test = DFContainer()
#         df_test.test = DFUInt32(value=0x1337)
#         df_test.test2 = DFUInt8(value=b"A")
#         df_test.sub = DFContainer()
#         df_test.sub.test_val = DFUInt16(value=0xAABB)
#         df_test.sub.another_sub = DFContainer()
#         df_test.sub.another_sub.sub_item = DFUInt8(value=-1)
#         df_test.sub.test = DFContainer()
#         df_test.sub.another_sub.out_of_order = DFUInt16(value=0x1122)
#         df_test.sub.test.deep_value = DFUInt32(value=1337)
#         df_test.sub.test.sub_sub = DFContainer()
#         df_test.sub.test.sub_sub.deep_value = DFUInt32(value=1337)
#         print(df_test)
#         print(df_test.pack())

#         print("")
#         df_test = DFContainer()
#         df_test.add("test", DFUInt32(value=0x1337))
#         df_test.add("test2", DFUInt8(value=b"A"))
#         df_test.add("sub", DFContainer())
#         df_test.add("sub.test_val", DFUInt16(value=0xAABB))
#         df_test.add("sub.another_sub", DFContainer())
#         df_test.add("sub.another_sub.sub_item", DFUInt8(value=1))
#         df_test.add("sub.another_sub.sub_item2", DFUInt8(value=2))
#         df_test.add("sub.test.sub_sub", DFContainer())
#         df_test.add("sub.test.sub_sub.deep_value", DFUInt32(value=0xEEFF))
#         print(df_test)
#         print(df_test.pack())

#         df_test = DFContainer()
#         df_test.test = DFUInt32(value=0x1337)
#         df_test.test2 = DFUInt8(value=b"A")
#         df_test.sub = DFLength(DFUInt32(), DFContainer())
#         df_test.sub.test_val = DFUInt16(value=0xAABB)
#         df_test.sub.another_sub = DFContainer()
#         df_test.sub.another_sub.sub_item = DFUInt8(value=-1)
#         df_test.sub.test = DFContainer()
#         df_test.sub.another_sub.out_of_order = DFUInt16(value=0x1122)
#         df_test.sub.test.deep_value = DFUInt32(value=1337)
#         df_test.sub.test.sub_sub = DFContainer()
#         df_test.sub.test.sub_sub.deep_value = DFUInt32(value=1337)
#         df_test.sub.buf = DFBuffer(value=b"A" * 100)
#         print(df_test)
#         print(df_test.pack())
