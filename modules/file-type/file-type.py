import os
import hashlib
from optparse import OptionParser


__description__ = 'File Type'
__author__ = 'Andrew Mitchell'
__version__ = '1.0'
__date__ = '2018/03'


file_types_dic = {
'000001': 'MPA',
'000002': 'TAG/TGA',
'000007': 'PJT',
'00000F': 'MOV',
'000077': 'MOV',
'000100': 'DDB/TST/TTF',
'005001': 'XMV',
'00FFFF': 'IMG/MDF/SMD',
'060500': 'RAW',
'0A0501': 'PCS',
'17A150': 'PCB',
'1F9D8C': 'Z',
'202020': 'BAS',
'234445': 'PRG',
'234558': 'm3u',
'24536F': 'PLL',
'255044': 'PDF',
'2A2420': 'LIB',
'2A5052': 'ECO',
'2A7665': 'SCH',
'2E524D': 'RM',
'3026B2': 'WMA/WMV',
'31BE00': 'WRI',
'384250': 'PSD',
'3C2144': 'HTM',
'3C3F78': 'MSC/XML',
'3F5F03': 'HLP',
'3F5F03': 'LHP',
'414331': 'dwg',
'42494C': 'LDB',
'424D3E': 'BMP',
'434841': 'FNT',
'435753': 'SWF',
'484802': 'PDG',
'49492A': 'TIF',
'495363': 'CAB',
'495453': 'CHM',
'4C0000': 'LNK',
'4D4544': 'MDS',
'4D5A16': 'DRV',
'4D5A50': 'DPL',
'4D5A90': 'EXE/IME/IMM/OCX/OLB/dll',
'4D5AEE': 'COM',
'4E4553': 'NES',
'504B03': 'ZIP',
'524946': 'WAV',
'526172': 'RAR',
'526563': 'EML/PPC',
'584245': 'XBE',
'5B4144': 'PBK',
'5B436C': 'CCD',
'5B5769': 'CPX',
'60EA27': 'ARJ',
'7B5072': 'GTD',
'7B5C72': 'RTF',
'805343': 'scm',
'87F53E': 'GBC',
'89504E': 'PNG',
'C22020': 'NLS',
'C5D0D3': 'EPS',
'D0CF11': 'PPT/XLS/max',
'E93B03': 'COM',
'FFFB50': 'MP3',
'FFFE3C': 'XSL',
'FFFFFF': 'SUB'
}


def filetype_module(filename):

    with open(filename, 'r') as file:
        # not ideal, really dumb converting string PDF to hex then check the hex in the dict then convert to string.
        first_line = file.readline()
        hex_first_line = ''.join(x.encode('hex') for x in first_line)
        if hex_first_line[:6].upper() in file_types_dic.keys():
            file_type_lookup = file_types_dic[hex_first_line[:6].upper()]
            print file_type_lookup
        else:
            print "NA"


if __name__ == "__main__":
        parser = OptionParser(usage='usage: %prog file / dir\n' + __description__, version='%prog ' + __version__)
        (options, args) = parser.parse_args()
        is_file = os.path.isfile(args[0])
        if is_file:
            filetype_module(args[0])
