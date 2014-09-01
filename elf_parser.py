import elf_types

class ELFParts(type):
    def __init__(cls, name, bases, attrs):
        super(ELFParts, cls).__init__(name, bases, attrs)
        cls._set_fields()

    def _add_field(cls, name, *fld_data):
        cls._fields.add_field(name, *fld_data)
        setattr(cls, name, property(cls._general_getter(name),
                                    cls._general_setter(name)))

    def _general_setter(cls, attr):
        def _setter(self, value):
            index = self.get_index(attr)
            field = self._fields.get_field_by_name(attr)

            self._data = (self._data[:index] +
                    field[1].str(value) + 
                    self._data[index + field[2]:])
        return _setter

    def _general_getter(cls, attr):
        def _getter(self):
            index = self.get_index(attr)
            field = self._fields.get_field_by_name(attr)

            return field[1].convert(self._data[index:index + field[2]])
        return _getter

class ELFHeader(object):
    __metaclass__ = ELFParts
    _fields = elf_types.Fielder()

    def __init__(self, elf_data):
        self._data = elf_data

    @classmethod
    def convert(cls, value):
        return cls(value)

    @classmethod
    def str(cls, value):
        raise ValueError('You can\'t edit headers directly')

    @classmethod
    def _set_fields(cls):
        cls._add_field('ident', elf_types.ELFString, 16)
        cls._add_field('type', elf_types.ELFInt16)
        cls._add_field('machine', elf_types.ELFInt16)
        cls._add_field('version', elf_types.ELFInt32)
        cls._add_field('entry', elf_types.ELFInt32)
        cls._add_field('phoff', elf_types.ELFInt32)
        cls._add_field('shoff', elf_types.ELFInt32)
        cls._add_field('flags', elf_types.ELFInt32)
        cls._add_field('ehsize', elf_types.ELFInt16)
        cls._add_field('phentsize', elf_types.ELFInt16)
        cls._add_field('phnum', elf_types.ELFInt16)
        cls._add_field('shentsize', elf_types.ELFInt16)
        cls._add_field('shnum', elf_types.ELFInt16)
        cls._add_field('shtrndx', elf_types.ELFInt16)

        cls.SIZE = cls._fields.size

    def get_index(self, attr):
        index = 0

        for name, ftype, size in self._fields:
            if name == attr:
                return index
            index += size

class ELFSectionTable(object):
    __metaclass__ = ELFParts
    _fields = elf_types.Fielder()

    def __init__(self, elf_data):
        self._data = elf_data

    @classmethod
    def convert(cls, value):
        return cls(value)

    @classmethod
    def str(cls, value):
        raise ValueError('You can\'t edit section headers directly')

    @classmethod
    def _set_fields(cls):
        pass

class ELFSectionHeader(object):
    __metaclass__ = ELFParts
    _fields = elf_types.Fielder()

    def __init__(self, elf_data):
        self._data = elf_data

    @classmethod
    def convert(cls, value):
        return cls(value)

    @classmethod
    def str(cls, value):
        raise ValueError('You can\'t edit section headers directly')

    @classmethod
    def _set_fields(cls):
        cls._add_field('name', elf_types.ELFInt32)
        cls._add_field('value', elf_types.ELFInt32)
        cls._add_field('size', elf_types.ELFInt32)
        cls._add_field('info', elf_types.ELFInt8)
        cls._add_field('other', elf_types.ELFInt8)
        cls._add_field('shndx', elf_types.ELFInt16)

    def get_index(self, attr):
        index = 0

        for name, ftype, size in self._fields:
            if name == attr:
                return index
            index += size

class ELFFile(object):
    __metaclass__ = ELFParts
    _fields = elf_types.Fielder()

    def __init__(self, file_path):
        self._path = file_path
        self._read_file()

    @classmethod
    def _set_fields(cls):
        cls._add_field('header', ELFHeader)

    def _read_file(self):
        f = open(self._path, 'rb')
        self._data = f.read()
        f.close()
        
        self._digest()

    def _write_file(self):
        f = open(self._path, 'wb')
        f.write(self._data)
        f.close()

    def _digest(self):
        pass

    def get_index(self, attr):
        index = 0

        for name, ftype, size in self._fields:
            if name == attr:
                return index
            index += size
