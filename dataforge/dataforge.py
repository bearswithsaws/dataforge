#!/usr/bin/env python3

# DataForge package

import abc
import binascii
import logging
import struct
from collections import OrderedDict
from enum import Enum


class DFEndian(Enum):
    LITTLE = 1
    BIG = 2


class DFRangeException(Exception):
    """DFRangeException"""

    pass


class DFEndianException(Exception):
    """DFEndianException"""

    pass


class DFTypeException(object):
    """docstring for DFTypeException"""

    pass


class DFBasicDataType(abc.ABC):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def value(self):
        pass

    @value.setter
    @abc.abstractmethod
    def value(self, value):
        pass

    @abc.abstractmethod
    def pack(self):
        pass

    @abc.abstractmethod
    def length(self):
        pass


class DFUInt8(DFBasicDataType):
    def __init__(self, value=0):
        self._fmt = "B"
        self._width = 1
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, int):
            self._value = val & 0xFF
        elif isinstance(val, bytes):
            if len(val) > 1:
                raise DFRangeException
            self._value = ord(val)
        else:
            raise DFTypeException

    def pack(self):
        return struct.pack(self._fmt, self._value)

    @property
    def length(self):
        return self._width

    def __str__(self):
        return self.pretty_print()

    def pretty_print(self, indent=0):
        return " " * indent + "|- " + "Unsigned Byte 0x{0:02X}".format(self.value)


class DFSInt8(DFUInt8):
    """docstring for DFSInt8"""

    def __init__(self, **kwargs):
        super(DFSInt8, self).__init__(**kwargs)
        self._fmt = "b"

    def pretty_print(self, indent=0):
        return " " * indent + "|- " + "Signed Byte 0x{0:02X}".format(self.value)


class DFUInt16(DFBasicDataType):
    def __init__(self, value=0, endian=DFEndian.LITTLE):
        if endian == DFEndian.LITTLE:
            self._endian = "<"
        elif endian == DFEndian.BIG:
            self._endian = ">"
        else:
            raise DFEndianException
        self._fmt = "H"
        self._width = 2
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, int):
            self._value = val & 0xFFFF
        else:
            if len(val) > 2:
                raise DFRangeException
            self._value = struct.unpack("@" + self._fmt, val)[0]

    def pack(self):
        return struct.pack(self._endian + self._fmt, self.value)

    @property
    def length(self):
        return self._width

    def __str__(self):
        return self.pretty_print()

    def pretty_print(self, indent=0):
        return " " * indent + "|- " + "Unsigned Short 0x{0:04X}".format(self.value)


class DFSInt16(DFUInt16):
    """docstring for DFSInt16"""

    def __init__(self, **kwargs):
        super(DFSInt16, self).__init__(**kwargs)
        self._fmt = "h"

    def pretty_print(self, indent=0):
        return " " * indent + "|- " + "Signed Short 0x{0:04X}".format(self.value)


class DFUInt32(DFBasicDataType):
    def __init__(self, value=0, endian=DFEndian.LITTLE):
        if endian == DFEndian.LITTLE:
            self._endian = "<"
        elif endian == DFEndian.BIG:
            self._endian = ">"
        else:
            raise DFEndianException
        self._fmt = "I"
        self._width = 4
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if type(val) == int:
            self._value = val & 0xFFFFFFFF
        else:
            if len(val) > 4:
                raise DFRangeException
            self._value = struct.unpack("@" + self._fmt, val)[0]

    def pack(self):
        return struct.pack(self._endian + self._fmt, self.value)

    @property
    def length(self):
        return self._width

    def __str__(self):
        return self.pretty_print()

    def pretty_print(self, indent=0):
        return " " * indent + "|- " + "Unsigned Long 0x{0:08X}".format(self.value)


class DFSInt32(DFUInt32):
    """docstring for DFSInt32"""

    def __init__(self, **kwargs):
        super(DFSInt32, self).__init__(**kwargs)
        self._fmt = "i"

    def pretty_print(self, indent=0):
        return " " * indent + "|- " + "Signed Long 0x{0:08X}".format(self.value)


class DFBuffer(DFBasicDataType):
    def __init__(self, value=b""):
        self._value = value
        self._width = len(self._value)

    @property
    def length(self):
        return self._width

    def pack(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, bytes):
            self._value = val
        else:
            raise DFTypeException("DFBuffer must be type: bytes")

    def pretty_print(self, indent=0):
        shortVal = str(binascii.hexlify(self.pack()))
        if self.length > 10:
            shortVal = str(binascii.hexlify(self.pack()[:10])) + "..."
        return " " * indent + "|- " + "Buffer {0}".format(shortVal)


# is a container a basic data type or its own thing?
class DFContainer(DFBasicDataType):
    """docstring for DFContainer"""

    def __init__(self):
        self._children = OrderedDict()
        self._name = None

    def add(self, name, obj):
        root = name
        subContainer = None
        logging.debug(name)
        if "." in root:
            root, subContainer = root.split(".", 1)
        logging.debug("{0} : {1}".format(root, subContainer))
        logging.debug(
            "Adding {0} to {1} (sub: {2})".format(type(obj), root, subContainer)
        )
        if root is not None and subContainer is None and isinstance(obj, DFContainer):
            logging.debug("SETTING NAME!!! {0}".format(subContainer))
            obj._name = root
        if root in iter(self._children) and subContainer is not None:
            # Recurse
            logging.debug("{0} in children for this container".format(root))
            self._children[root].add(subContainer, obj)
        else:
            logging.debug("New child, Setting {0} to {1}".format(root, obj))
            self._children[root] = obj

        return self

    def __getattribute__(self, name):
        if name != "_children" and name in self._children.keys():
            return self._children[name]
        else:
            return super(DFContainer, self).__getattribute__(name)

    def __setattr__(self, name, obj):
        if isinstance(obj, DFBasicDataType) and not name.startswith(
            "_"
        ):  # Or whatever a container is?
            logging.debug("SETTER: {0}".format(name))
            self.add(name, obj)
        else:
            super(DFBasicDataType, self).__setattr__(name, obj)

    @property
    def length(self):
        return len(repr(self))

    # Does value make sense? Does this show we need another basic class type?
    @property
    def value(self, value):
        pass

    def _get_children(self):
        """Returns a copy of its children"""
        return list(iter(self._children.values()))[:]

    def pack(self):
        data = b""
        children = self._get_children()
        while len(children):
            child = children.pop()
            if isinstance(child, DFBasicDataType):
                data = child.pack() + data
            else:
                data = repr(child) + data
        return data

    # def __str__( self ):
    #    return binascii.hexlify( repr( self ) )

    def __str__(self):
        return self.pretty_print()

    def pretty_print(self, indent=0):
        ret = " " * indent + "+{0}\n".format(self._name)
        for child in self._children:
            logging.debug("current child: {0} ({1})".format(child, indent))
            if isinstance(self._children[child], DFContainer):
                ret += "|" + self._children[child].pretty_print(indent + 1)
            else:
                ret += (
                    "|"
                    + self._children[child].pretty_print(indent + 1)
                    + " : {0} ".format(child)
                    + "\n"
                )
        return ret


class DFLength(DFContainer):
    def __init__(self, field, container):
        super(DFLength, self).__init__()
        self._field = field
        self._children["_data"] = container

    def __getattribute__(self, name):
        if name != "_children" and name in self._children["_data"]._children.keys():
            return self._children["_data"]._children[name]
        else:
            return super(DFContainer, self).__getattribute__(name)

    def __setattr__(self, name, obj):
        if isinstance(obj, DFBasicDataType) and not name.startswith("_"):
            self.add("_data." + name, obj)
        else:
            super(DFContainer, self).__setattr__(name, obj)

    def pack(self):
        data = b""
        children = self._get_children()
        while len(children):
            child = children.pop()
            if isinstance(child, DFBasicDataType):
                data = child.pack() + data
            else:
                data = repr(child) + data

        self._field.value = len(data)
        return self._field.pack() + data

    @property
    def value(self):
        data = b""
        children = self._get_children()
        while len(children):
            child = children.pop()
            if isinstance(child, DFBasicDataType):
                data = child.pack() + data
            else:
                data = repr(child) + data
        self._field.value = len(data)
        return self._field.value

    def __str__(self):
        return self.pretty_print()

    def pretty_print(self, indent=0):
        ret = " " * indent + "+{0} length: 0x{1:0x}\n".format(self._name, self.value)
        for child in self._children["_data"]._children:
            logging.debug("current child: {0} ({1})".format(child, indent))
            if isinstance(self._children["_data"]._children[child], DFContainer):
                ret += "|" + self._children["_data"]._children[child].pretty_print(
                    indent + 1
                )
            else:
                ret += (
                    "|"
                    + self._children["_data"]._children[child].pretty_print(indent + 1)
                    + " : {0} ".format(child)
                    + "\n"
                )
        return ret


def main():
    pass


if __name__ == "__main__":
    main()
