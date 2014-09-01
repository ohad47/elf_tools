class ELFInteger(object):
    @classmethod
    def convert(cls, value):
        if isinstance(value, int):
            return value

        if not isinstance(value, str) and not len(value) > cls.SIZE:
            raise ValueError('Incompatible value')

        return int(cls.flip_endian(value).encode('hex'), 16)
    
    @classmethod
    def flip_endian(cls, decoded_str):
        decoded_bytes = list(decoded_str)
        decoded_bytes.reverse()
        return ''.join(decoded_bytes)

    @classmethod
    def str(cls, value):
        format_str = '%%0%dx' % (cls.SIZE * 2,)
        return cls.flip_endian((format_str % value).decode('hex'))

class ELFInt8(ELFInteger):
    SIZE = 1

class ELFInt16(ELFInteger):
    SIZE = 2

class ELFInt32(ELFInteger):
    SIZE = 4

class ELFString(object):
    @classmethod
    def convert(cls, value):
        return value
    
    @classmethod
    def str(cls, value):
        return value

class Field(object):
    def __init__(self, name, ftype, size):
        self.name = name
        self.ftype = ftype
        self.size = size

class Fielder(object):
    def __init__(self):
        self._fields = []
        
    def __iter__(self):
        for field in self._fields:
            yield field.name, field.ftype, field.size

    @property
    def size(self):
        size = 0
        for field in self._fields:
            size += field.size

        return size

    def add_field(self, name, field_type, size = None):
        if not size:
            size = field_type.SIZE

        self._fields.append(Field(name, field_type, size))

    def get_field_by_name(self, name):
        for field in self._fields:
            if field.name == name:
                return field.name, field.ftype, field.size

class ELFPart(object):
    pass
