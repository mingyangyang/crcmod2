#-----------------------------------------------------------------------------
# Copyright (c) 2010 Craig McQueen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-----------------------------------------------------------------------------
'''
crcmod.predefined defines some well-known CRC algorithms.

To use it, e.g.:
    import crcmod.predefined
    
    crc32func = crcmod.predefined.mkPredefinedCrcFun("crc-32")
    crc32class = crcmod.predefined.PredefinedCrc("crc-32")

crcmod.predefined.Crc is an alias for crcmod.predefined.PredefinedCrc
But if doing 'from crc.predefined import *', only PredefinedCrc is imported.
'''

# local imports
import crcmod

__all__ = [
    'PredefinedCrc',
    'mkPredefinedCrcFun',
]

REVERSE = True
NON_REVERSE = False

# The following table defines the parameters of well-known CRC algorithms.
# The "Check" value is the CRC for the ASCII byte sequence "123456789". It
# can be used for unit tests.
_crc_definitions_table = [
#       Name                Identifier-name,    Poly            Reverse         Init-value      XOR-out     Check
    [   'crc-8',            'Crc8',             0x107,          NON_REVERSE,    0x00,           0x00,       0xF4,       ],
    [   'crc-8-darc',       'Crc8Darc',         0x139,          REVERSE,        0x00,           0x00,       0x15,       ],
    [   'crc-8-i-code',     'Crc8ICode',        0x11D,          NON_REVERSE,    0xFD,           0x00,       0x7E,       ],
    [   'crc-8-itu',        'Crc8Itu',          0x107,          NON_REVERSE,    0x55,           0x55,       0xA1,       ],

    [   'crc-16',           'Crc16',            0x18005,        REVERSE,        0x0000,         0x0000,     0xBB3D,     ],
    [   'crc-16-usb',       'Crc16Usb',         0x18005,        REVERSE,        0x0000,         0xFFFF,     0xB4C8,     ],
    [   'x-25',             'CrcX25',           0x11021,        REVERSE,        0x0000,         0xFFFF,     0x906E,     ],
    [   'xmodem',           'CrcXmodem',        0x11021,        NON_REVERSE,    0x0000,         0x0000,     0x31C3,     ],
    [   'modbus',           'CrcModbus',        0x18005,        REVERSE,        0xFFFF,         0x0000,     0x4B37,     ],

    # Note definitions of CCITT are disputable. See:
    #    http://homepages.tesco.net/~rainstorm/crc-catalogue.htm
    #    http://web.archive.org/web/20071229021252/http://www.joegeluso.com/software/articles/ccitt.htm
    [   'kermit',           'CrcKermit',        0x11021,        REVERSE,        0x0000,         0x0000,     0x2189,     ],
    [   'crc-ccitt-false',  'CrcCcittFalse',    0x11021,        NON_REVERSE,    0xFFFF,         0x0000,     0x29B1,     ],
    [   'crc-aug-ccitt',    'CrcAugCcitt',      0x11021,        NON_REVERSE,    0x1D0F,         0x0000,     0xE5CC,     ],

    [   'crc-24',           'Crc24',            0x1864CFB,      NON_REVERSE,    0xB704CE,       0x000000,   0x21CF02,   ],

    [   'crc-32',           'Crc32',            0x104C11DB7,    REVERSE,        0x00000000,     0xFFFFFFFF, 0xCBF43926, ],
    [   'crc-32c',          'Crc32C',           0x11EDC6F41,    REVERSE,        0x00000000,     0xFFFFFFFF, 0xE3069283, ],
    [   'crc-32-mpeg',      'Crc32Mpeg',        0x104C11DB7,    NON_REVERSE,    0xFFFFFFFF,     0x00000000, 0x0376E6E7, ],
    [   'posix',            'CrcPosix',         0x104C11DB7,    NON_REVERSE,    0xFFFFFFFF,     0xFFFFFFFF, 0x765E7680, ],

# 64-bit
#       Name                Identifier-name,    Poly                    Reverse         Init-value          XOR-out             Check
    [   'crc-64',           'Crc64',            0x1000000000000001B,    REVERSE,        0x0000000000000000, 0x0000000000000000, 0x46A5A9388A5BEFFE, ],
    [   'crc-64-jones',     'Crc64Jones',       0x1AD93D23594C935A9,    REVERSE,        0xFFFFFFFFFFFFFFFF, 0x0000000000000000, 0xCAA717168609F281, ],

# Other unusual widths
#       Name                Identifier-name,    Poly            Reverse         Init-value      XOR-out     Check
    [   'crc-3-rohc',       'Crc3Rohc',         0xB,            REVERSE,        0x7,            0x0,        0x6,        ],
    [   'crc-4-itu',        'Crc3Itu',          0x13,           REVERSE,        0x00,           0x00,       0x07,       ],
    [   'crc-5-epc',        'Crc5Epc',          0x29,           NON_REVERSE,    0x09,           0x00,       0x00,       ],
    [   'crc-5-itu',        'Crc5Itu',          0x35,           REVERSE,        0x00,           0x00,       0x07,       ],
    [   'crc-5-usb',        'Crc5Usb',          0x25,           REVERSE,        0x00,           0x1F,       0x19,       ],
    [   'crc-6-itu',        'Crc5Itu',          0x43,           REVERSE,        0x00,           0x00,       0x06,       ],
    [   'crc-7',            'Crc7',             0x89,           NON_REVERSE,    0x00,           0x00,       0x75,       ],
    [   'crc-7-rohc',       'Crc7Rohc',         0xCF,           REVERSE,        0x7F,           0x00,       0x53,       ],
    [   'crc-10',           'Crc10',            0x633,          NON_REVERSE,    0x000,          0x000,      0x199,      ],
    [   'crc-11',           'Crc11',            0xB85,          NON_REVERSE,    0x01A,          0x000,      0x5A3,      ],
    [   'crc-14-darc',      'Crc14Darc',        0x4805,         REVERSE,        0x0000,         0x0000,     0x082D,     ],
    [   'crc-15',           'Crc15',            0xC599,         NON_REVERSE,    0x0000,         0x0000,     0x059E,     ],

#       Name                Identifier-name,    Poly                    Reverse         Init-value          XOR-out             Check
    [   'crc-40-gsm',       'Crc40Gsm',         0x10004820009,          NON_REVERSE,    0x0000000000,       0x0000000000,       0x2BE9B039B9,   ],
]


def _simplify_name(name):
    """
    Reduce CRC definition name to a simplified form:
        * lowercase
        * dashes removed
        * spaces removed
        * any initial "CRC" string removed
    """
    name = name.lower()
    name = name.replace('-', '')
    name = name.replace(' ', '')
    if name.startswith('crc'):
        name = name[len('crc'):]
    return name


_crc_definitions_by_name = {}
_crc_definitions_by_identifier = {}
_crc_definitions = []

_crc_table_headings = [ 'name', 'identifier', 'poly', 'reverse', 'init', 'xor_out', 'check' ]

for table_entry in _crc_definitions_table:
    crc_definition = dict(zip(_crc_table_headings, table_entry))
    _crc_definitions.append(crc_definition)
    name = _simplify_name(table_entry[0])
    if name in _crc_definitions_by_name:
        raise Exception("Duplicate entry for '%s' in CRC table" % name)
    _crc_definitions_by_name[name] = crc_definition
    _crc_definitions_by_identifier[table_entry[1]] = crc_definition


def _get_definition_by_name(crc_name):
    definition = _crc_definitions_by_name.get(_simplify_name(crc_name), None)
    if not definition:
        definition = _crc_definitions_by_identifier.get(crc_name, None)
    if not definition:
        raise KeyError("Unkown CRC name '%s'" % crc_name)
    return definition


class PredefinedCrc(crcmod.Crc):
    def __init__(self, crc_name):
        definition = _get_definition_by_name(crc_name)
        crcmod.Crc.__init__(self, poly=definition['poly'], initCrc=definition['init'], rev=definition['reverse'], xorOut=definition['xor_out'])


# crcmod.predefined.Crc is an alias for crcmod.predefined.PredefinedCrc
Crc = PredefinedCrc


def mkPredefinedCrcFun(crc_name):
    definition = _get_definition_by_name(crc_name)
    return crcmod.mkCrcFun(poly=definition['poly'], initCrc=definition['init'], rev=definition['reverse'], xorOut=definition['xor_out'])


# crcmod.predefined.mkCrcFun is an alias for crcmod.predefined.mkPredefinedCrcFun
mkCrcFun = mkPredefinedCrcFun
