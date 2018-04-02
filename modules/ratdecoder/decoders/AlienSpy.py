import re
import json
import string
import struct
from zipfile import ZipFile
from cStringIO import StringIO

#Non Standard Imports
from Crypto.Cipher import ARC4

def version_a(enckey, coded_jar):
    config_dict = {}
    for key in enckey:
        print "  [!] testing Key {0}".format(key)
        decoded_data = decrypt_RC4(key, coded_jar)
        try:
            decoded_jar = ZipFile(StringIO(decoded_data))
            raw_config = decoded_jar.read('org/jsocket/resources/config.json')
            config = json.loads(raw_config)
            for k, v in config.iteritems():
                config_dict[k] = v
            return config_dict
        except:
            pass


def version_b(enckey, coded_jar):
    config_dict = {}
    for key in enckey:
        print "  [!] testing Key {0}".format(key)
        decoded_data = decrypt_RC4(key, coded_jar)
        try:
            decoded_jar = ZipFile(StringIO(decoded_data))
            raw_config = decoded_jar.read('config.xml')

            for line in raw_config.split('\n'):
                if line.startswith('<entry key'):
                    config_dict[re.findall('key="(.*?)"', line)[0]] = re.findall('>(.*?)</entry', line)[0]
            return config_dict
        except:
            pass


def version_c(enckey, coded_jar, rounds=20, P=0xB7E15163, Q=0x9E3779B9):
    config_dict = {}
    for key in enckey:
        print "  [!] testing Key {0}".format(key)
        decoded_data = decrypt_RC6(key, coded_jar, rounds=rounds, P=P, Q=Q)
        try:
            decoded_jar = ZipFile(StringIO(decoded_data))
            raw_config = decoded_jar.read('org/jsocket/resources/config.json')
            config = json.loads(raw_config)
            for k, v in config.iteritems():
                config_dict[k] = v
            return config_dict
        except:
            pass

def version_d(enckey, coded_jar):
    return version_c(enckey, coded_jar, rounds=22, P=0xb7e15263, Q=0x9e3779c9)


def string_print(line):
    try:
        return filter(lambda x: x in string.printable, str(line))
    except:
        return line


def decrypt_RC4(enckey, data):
	cipher = ARC4.new(enckey) # set the ciper
	return cipher.decrypt(data) # decrpyt the data


def decrypt_RC6(key, encrypted, P, Q, rounds):
    def rol(a, i):
        a &= 0xFFFFFFFF
        i &= 0x1F
        x = (((a << i) & 0xFFFFFFFF) | (a >> (32 - i))) & 0xFFFFFFFF
        return x

    def ror(a, i):
        i &= 0x1F
        a &= 0xFFFFFFFF
        return ( ((a >> i) & 0xFFFFFFFF) | (a << ( (32 - i)))) & 0xFFFFFFFF


    def to_int(bytes):
        l = []
        for i in range(len(bytes)/4):
            l.append(struct.unpack("<I", bytes[i*4:(i*4)+4])[0])
        return l

    def decrypt_block(block, S):
        # Decrypt block
        ints = to_int(block)
        ints[0] = (ints[0] - S[T-2])
        ints[2] = (ints[2] - S[T-1])
        for i in reversed(range(rounds)):
            r = i+1

            # rotate ints
            ints = ints[-1:] + ints[:-1]

            tmp1 = rol(ints[3] * (2 * ints[3] + 1), 5)
            tmp2 = rol(ints[1] * (2 * ints[1] + 1), 5)
            ints[2] = ror(ints[2] - S[2 * r + 1], tmp2) ^ tmp1
            ints[0] = ror(ints[0] - S[2 * r], tmp1) ^ tmp2

        ints[3] = ints[3] - S[1]
        ints[1] = ints[1] - S[0]

        # convert to bytes
        decrypted = []
        for i in range(4):
            for j in range(4):
                decrypted.append(ints[i] >> (j * 8) & 0xFF)
        return decrypted

    T = 2 * rounds + 4

    # Expand key
    L = to_int(key)
    S = []
    S = [0 for i in range(T)]
    S[0] = P

    for x in range(T-1):
        S[x+1] = (S[x] + Q) & 0xFFFFFFFF
    i = 0
    j = 0
    A = 0
    B = 0

    for x in xrange(3*T):
        A = S[i] = rol((S[i] + A + B), 3)
        B = L[j] = rol((L[j] + A + B), (A + B))
        i = (i + 1) % T
        j = (j + 1) % 8

    # Decrypt blocks
    decrypted = []
    while True:
        decrypted += decrypt_block(encrypted[:16], S)
        encrypted = encrypted[16:]
        if not encrypted:
            break
    data = bytearray(decrypted)
    data = data.rstrip(b"\x00")
    return data


def decrypt_XOR(keys, data):
    for key in keys:
        res = ""
        for i in xrange(len(data)):
            res += chr(ord(data[i]) ^ ord(key[i%len(key)]))
        if "SERVER" in res:
            return res

def xor_config(data):
    config_dict = {}
    xor_keys = ["0x999sisosouuqjqhyysuhahyujssddqsad23rhggdsfsdfs",
                "VY999sisosouuqjqhyysuhahyujssddqsad22rhggdsfsdfs",
                "ABJSIOODKKDIOSKKJDJUIOIKASJIOOQKSJIUDIKDKIAS",
                "fkfjgioelsqisoosidiijsdndcbhchyduwiqoqpqwoieweueidjdshsjahshquuiqoaooasisjdhdfh",
                "adsdcwegtryhyurtgwefwedwscsdcwsdfcasfwqedfwefsdfasdqwdascfsdfvsdvwergvergerg",
                "adsdcwegtryhyurtgwefwedwscsdcwsdfcasfwqedfwefsdfasdqwdascfsdfvsdvwergvergerg",
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "lolskmzzzznzbxbxjxjjzkkzzkiziopoakidqoiwjdiqjhwdiqjwiodjdhjhbhbvhcebucbecercsdsd",
                "Zlolskmzzzznzbxbxjxjjzkkzzkiziopoakidqoiwjdiqjhwdiqjwiodjdhjhbhbvhcebucbecercsdsd",
                "aaaaaaaaaaaaaaaaaaaaa",
                "kevthehermitisacompletegaywhatfuckwithhismotherXDXDXD",
                "XXXXXXXkevthehermitisacompletegaywhatfuckwithhismotherXDXDXD",
                ]
    raw_config = decrypt_XOR(xor_keys, data)
    for line in raw_config.split('\n'):
        if line.startswith('<entry key'):
            config_dict[re.findall('key="(.*?)"', line)[0]] = re.findall('>(.*?)</entry', line)[0]
    return config_dict

def run(file_name):
    config_dict = False
    jar = ZipFile(file_name, 'r')
    # Version A
    if 'a.txt' and 'b.txt' in jar.namelist():
        pre_key = jar.read('a.txt')
        enckey = ['{0}{1}{0}{1}a'.format('plowkmsssssPosq34r', pre_key),
                  '{0}{1}{0}{1}a'.format('kevthehermitisaGAYXD', pre_key)
                  ]
        coded_jar = jar.read('b.txt')
        config_dict = version_a(enckey, coded_jar)

    # Version B
    if 'ID' and 'MANIFEST.MF' in jar.namelist():
        pre_key = jar.read('ID')
        enckey = ['{0}H3SUW7E82IKQK2J2J2IISIS'.format(pre_key)]
        coded_jar = jar.read('MANIFEST.MF')
        config_dict = version_b(enckey, coded_jar)

    # Version C
    if 'resource/password.txt' and 'resource/server.dll' in jar.namelist():
        pre_key = jar.read('resource/password.txt')
        enckey = ['CJDKSIWKSJDKEIUSYEIDWE{0}'.format(pre_key)]
        coded_jar = jar.read('resource/server.dll')
        config_dict = version_c(enckey, coded_jar)

    # Version D
    if 'java/stubcito.opp' and 'java/textito.isn' in jar.namelist():
        pre_key = jar.read('java/textito.isn')
        enckey = ['TVDKSIWKSJDKEIUSYEIDWE{0}'.format(pre_key)]
        coded_jar = jar.read('java/stubcito.opp')
        config_dict = version_c(enckey, coded_jar)

    # Version E
    if 'java/textito.text' and 'java/resource.xsx' in jar.namelist():
        pre_key = jar.read('java/textito.text')
        enckey = ['kevthehermitGAYGAYXDXD{0}'.format(pre_key)]
        coded_jar = jar.read('java/resource.xsx')
        config_dict = version_c(enckey, coded_jar)

    if 'amarillo/asdasd.asd' and 'amarillo/adqwdqwd.asdwf' in jar.namelist():
        pre_key = jar.read('amarillo/asdasd.asd')
        enckey = ['kevthehermitGAYGAYXDXD{0}'.format(pre_key)]
        coded_jar = jar.read('amarillo/adqwdqwd.asdwf')
        config_dict = version_c(enckey, coded_jar)

    # Version F
    if 'config/config.perl' in jar.namelist():
        temp_config = xor_config(jar.read('config/config.perl'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['kevthehermitGAYGAYXDXD{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_c(enckey, coded_jar)

    # Version G
    if 'config/config.pl' in jar.namelist():
        temp_config = xor_config(jar.read('config/config.pl'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['kevthehermitGAYGAYGAYD{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_c(enckey, coded_jar)

    # Version H
    if 'config/config.ini' in jar.namelist():
        temp_config = xor_config(jar.read('config/config.ini'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['kevthehermitGAYGAYGAYD{0}'.format(temp_config["PASSWORD"]),
                  'kevthehermitGADGAYGAYD{}'.format(temp_config["PASSWORD"])]
        config_dict = version_c(enckey, coded_jar)

    # Version I
    if 'windows/windows.ini' in jar.namelist():
        temp_config = xor_config(jar.read('windows/windows.ini'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['kevthehermitGADGAYGAYD{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_c(enckey, coded_jar)

    # Version J
    if 'components/linux.plsk' in jar.namelist():
        temp_config = xor_config(jar.read('components/linux.plsk'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['kevthehermitGADGAYGAYD{0}'.format(temp_config["PASSWORD"]),
                  'LDLDKFJVUI39OWIS9WOQ92{}'.format(temp_config["PASSWORD"])]
        config_dict = version_c(enckey, coded_jar)
        if config_dict is None:
            config_dict = version_d(enckey, coded_jar)

    # Version K
    if 'components/manifest.ini' in jar.namelist():
        temp_config = xor_config(jar.read('components/manifest.ini'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['LDLDKFJVUI39OWIS9WOQ93{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_d(enckey, coded_jar)

    # Version L
    if 'components/mac.hwid' in jar.namelist():
        temp_config = xor_config(jar.read('components/mac.hwid'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['LDLDKFJVUI39OWIS9WOQ92{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_d(enckey, coded_jar)

    # Version M
    if 'components/logo.png' in jar.namelist():
        temp_config = xor_config(jar.read('components/logo.png'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['LDLDKFJVUI39OWIS9WOQ93{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_d(enckey, coded_jar)

    # Version N
    if 'components/picture.gif' in jar.namelist():
        temp_config = xor_config(jar.read('components/picture.gif'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['TDLDKFJVUI39OWIS9WOQ93{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_d(enckey, coded_jar)

    # Version O
    if 'klip/clip.mp4' in jar.namelist():
        temp_config = xor_config(jar.read('klip/clip.mp4'))
        coded_jar = jar.read(temp_config['SERVER'][1:])
        enckey = ['TKLDKFJVUI39OWIS9WOQ93{0}'.format(temp_config["PASSWORD"])]
        config_dict = version_d(enckey, coded_jar)

    return config_dict
