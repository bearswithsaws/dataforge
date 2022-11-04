import logging
import unittest

from dataforge import *


class TestDFUInt8(unittest.TestCase):
    def test(self):
        d = DFUInt8(value=0xFF)
        self.assertTrue(b"\xff" == d.pack())

        d = DFUInt8(value=b"\xaa")
        self.assertTrue(b"\xaa" == d.pack())

        try:
            d = DFUInt8(value=b"abc")
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # try:
        #     d = DFUInt8( value=0x100 )
        # except Exception as e:
        #     self.assertTrue( True )
        # else:
        #     self.assertTrue( False )

        self.assertTrue(d.length == 1)


class TestDFSInt8(unittest.TestCase):
    def test(self):
        d = DFSInt8(value=-1)
        self.assertTrue(b"\xff" == d.pack())

        d = DFSInt8(value=b"\x7f")
        self.assertTrue(b"\x7f" == d.pack())

        try:
            d = DFSInt8(value=b"abc")
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # try:
        #     d = DFUInt8( value=0x100 )
        # except Exception as e:
        #     self.assertTrue( True )
        # else:
        #     self.assertTrue( False )

        self.assertTrue(d.length == 1)


class TestDFUInt16(unittest.TestCase):
    def test(self):
        d = DFUInt16(value=0x1234)
        self.assertTrue(b"\x34\x12" == d.pack())

        d = DFUInt16(value=0x1234, endian=DFEndian.BIG)
        self.assertTrue(b"\x12\x34" == d.pack())

        d = DFUInt16(value=b"\xbb\xaa", endian=DFEndian.LITTLE)
        self.assertTrue(b"\xbb\xaa" == d.pack())

        d = DFUInt16(value=b"\xbb\xaa", endian=DFEndian.BIG)
        self.assertTrue(b"\xaa\xbb" == d.pack())

        try:
            d = DFUInt16(value=b"abcd")
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # try:
        #     d = DFUInt16( value=0x10000 )
        # except Exception as e:
        #     self.assertTrue( True )
        # else:
        #     self.assertTrue( False )

        self.assertTrue(d.length == 2)


class TestDFSInt16(unittest.TestCase):
    def test(self):
        d = DFSInt16(value=0x1234)
        self.assertTrue(b"\x34\x12" == d.pack())

        d = DFSInt16(value=0x1234, endian=DFEndian.BIG)
        self.assertTrue(b"\x12\x34" == d.pack())

        d = DFSInt16(value=b"\xbb\x7f", endian=DFEndian.LITTLE)
        self.assertTrue(b"\xbb\x7f" == d.pack())

        d = DFSInt16(value=b"\xbb\x7f", endian=DFEndian.BIG)
        self.assertTrue(b"\x7f\xbb" == d.pack())

        try:
            d = DFSInt16(value=b"abcd")
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # try:
        #     d = DFSInt16( value=0x10000 )
        # except Exception as e:
        #     self.assertTrue( True )
        # else:
        #     self.assertTrue( False )

        self.assertTrue(d.length == 2)


class TestDFUInt32(unittest.TestCase):
    def test(self):
        d = DFUInt32(value=0x12345678)
        self.assertTrue(b"\x78\x56\x34\x12" == d.pack())

        d = DFUInt32(value=0x12345678, endian=DFEndian.BIG)
        self.assertTrue(b"\x12\x34\x56\x78" == d.pack())

        d = DFUInt32(value=b"\xdd\xcc\xbb\xaa", endian=DFEndian.LITTLE)
        self.assertTrue(b"\xdd\xcc\xbb\xaa" == d.pack())

        d = DFUInt32(value=b"\xdd\xcc\xbb\xaa", endian=DFEndian.BIG)
        self.assertTrue(b"\xaa\xbb\xcc\xdd" == d.pack())

        try:
            d = DFUInt32(value=b"abcdef")
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # try:
        #     d = DFUInt32( value=0x100000000 )
        # except Exception as e:
        #     self.assertTrue( True )
        # else:
        #     self.assertTrue( False )

        self.assertTrue(d.length == 4)


class TestDFSInt32(unittest.TestCase):
    def test(self):
        d = DFSInt32(value=-1)
        self.assertTrue(b"\xff\xff\xff\xff" == d.pack())


class TestDFContainer(unittest.TestCase):
    def test(self):
        d = DFContainer()
        d.add("test", DFUInt32(value=0x1337))
        self.assertTrue(b"\x37\x13\x00\x00" == d.pack())

        # Add a sub caontianer
        d.add("sub", DFContainer())
        self.assertTrue(b"\x37\x13\x00\x00" == d.pack())

        d.add("sub.test_sub_container", DFContainer())
        self.assertTrue(b"\x37\x13\x00\x00" == d.pack())

        d.add("sub.test_sub_container.test", DFUInt16(value=0xAABB))
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa" == d.pack())

        d.add("sub.test_sub_container.another", DFUInt16(value=0xCCDD))
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc" == d.pack())

        d.add("upper", DFUInt8(value=b"A"))
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x41" == d.pack())

        d.add("sub.inner_insert", DFUInt8(value=b"B"))
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x42\x41" == d.pack())

        d = DFContainer()
        d.test = DFUInt32(value=0x1337)
        d.test2 = DFUInt8(value=b"A")
        d.sub = DFContainer()
        d.sub.test_sub = DFContainer()
        d.sub.test_val = DFUInt16(value=0xAABB)
        d.sub.another_sub = DFContainer()
        d.sub.another_sub.sub_item = DFUInt8(value=1)
        d.sub.another_sub.sub_item2 = DFUInt8(value=2)
        d.sub.test_sub.sub_sub = DFContainer()
        d.sub.test_sub.sub_sub.deep_value = DFUInt32(value=0xEEFF)


class TestDFContainerShorthand(unittest.TestCase):
    def test(self):
        # Shorthand
        d = DFContainer()
        d.test = DFUInt32(value=0x1337)
        self.assertTrue(b"\x37\x13\x00\x00" == d.pack())

        # Add a sub caontianer
        d.sub = DFContainer()
        self.assertTrue(b"\x37\x13\x00\x00" == d.pack())

        d.sub.test_sub_container = DFContainer()
        self.assertTrue(b"\x37\x13\x00\x00" == d.pack())

        d.sub.test_sub_container.test = DFUInt16(value=0xAABB)
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa" == d.pack())

        d.sub.test_sub_container.another = DFUInt16(value=0xCCDD)
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc" == d.pack())

        d.upper = DFUInt8(value=b"A")
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x41" == d.pack())

        d.sub.inner_insert = DFUInt8(value=b"B")
        self.assertTrue(b"\x37\x13\x00\x00\xbb\xaa\xdd\xcc\x42\x41" == d.pack())

        d = DFContainer()
        d.add("test", DFUInt32(value=0x1337))
        d.add("test2", DFUInt8(value=b"A"))
        d.add("sub", DFContainer())
        d.add("sub.test_val", DFUInt16(value=0xAABB))
        d.add("sub.another_sub", DFContainer())
        d.add("sub.another_sub.sub_item", DFUInt8(value=1))
        d.add("sub.another_sub.sub_item2", DFUInt8(value=2))
        d.add("sub.test.sub_sub", DFContainer())
        d.add("sub.test.sub_sub.deep_value", DFUInt32(value=0xEEFF))
        print(d.pack())


class TestDFLength(unittest.TestCase):
    def test(self):
        d = DFContainer()
        d.len = DFLength(DFUInt16(), DFContainer())
        d.len.data = DFUInt32(value=0xAABBCCDD)
        d.len.data2 = DFUInt8(value=10)
        self.assertTrue(b"\x05\x00\xdd\xcc\xbb\xaa\x0a" == d.pack())

        d = DFContainer()
        d.len = DFLength(DFUInt16(endian=DFEndian.BIG), DFContainer())
        d.len.data = DFUInt32(value=0xAABBCCDD)
        d.len.data2 = DFUInt8(value=10)
        self.assertTrue(b"\x00\x05\xdd\xcc\xbb\xaa\x0a" == d.pack())


class TestPrint(unittest.TestCase):
    def test(self):
        logging.basicConfig(level=logging.WARN)
        d = DFUInt8(value=0x41)
        print(d)

        d = DFContainer()
        d.test = DFUInt32(value=0x1337)
        d.test2 = DFUInt8(value=b"A")
        d.sub = DFContainer()
        d.sub.test_val = DFUInt16(value=0xAABB)
        d.sub.another_sub = DFContainer()
        d.sub.another_sub.sub_item = DFUInt8(value=-1)
        d.sub.test = DFContainer()
        d.sub.another_sub.out_of_order = DFUInt16(value=0x1122)
        d.sub.test.deep_value = DFUInt32(value=1337)
        d.sub.test.sub_sub = DFContainer()
        d.sub.test.sub_sub.deep_value = DFUInt32(value=1337)
        print(d)
        print(d.pack())

        print("")
        d = DFContainer()
        d.add("test", DFUInt32(value=0x1337))
        d.add("test2", DFUInt8(value=b"A"))
        d.add("sub", DFContainer())
        d.add("sub.test_val", DFUInt16(value=0xAABB))
        d.add("sub.another_sub", DFContainer())
        d.add("sub.another_sub.sub_item", DFUInt8(value=1))
        d.add("sub.another_sub.sub_item2", DFUInt8(value=2))
        d.add("sub.test.sub_sub", DFContainer())
        d.add("sub.test.sub_sub.deep_value", DFUInt32(value=0xEEFF))
        print(d)
        print(d.pack())

        d = DFContainer()
        d.test = DFUInt32(value=0x1337)
        d.test2 = DFUInt8(value=b"A")
        d.sub = DFLength(DFUInt32(), DFContainer())
        d.sub.test_val = DFUInt16(value=0xAABB)
        d.sub.another_sub = DFContainer()
        d.sub.another_sub.sub_item = DFUInt8(value=-1)
        d.sub.test = DFContainer()
        d.sub.another_sub.out_of_order = DFUInt16(value=0x1122)
        d.sub.test.deep_value = DFUInt32(value=1337)
        d.sub.test.sub_sub = DFContainer()
        d.sub.test.sub_sub.deep_value = DFUInt32(value=1337)
        d.sub.buf = DFBuffer(value=b"A" * 100)
        print(d)
        print(d.pack())


if __name__ == "__main__":
    unittest.main()
