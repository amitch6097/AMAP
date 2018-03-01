from struct import unpack
import pefile


def get_unicode_string(buf,pos):
    out = ''
    for i in range(len(buf[pos:])):
        if not (ord(buf[pos+i]) >= 32 and ord(buf[pos+i]) <= 126) and not (ord(buf[pos+i+1]) >= 32 and ord(buf[pos+i+1]) <= 126):
            out += '\x00'
            break
        out += buf[pos+i]
    if out == '':
        return None
    else:
        return out.replace('\x00','')


def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % 6])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    
    return ''.join(out)


def extract_config(rawData):
    try:
        pe = pefile.PE(data=rawData)
        try:
          rt_string_idx = [
          entry.id for entry in 
          pe.DIRECTORY_ENTRY_RESOURCE.entries].index(pefile.RESOURCE_TYPE['RT_RCDATA'])
        except ValueError, e:
            return None
        except AttributeError, e:
            return None
        rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]
        for entry in rt_string_directory.directory.entries:
            if str(entry.name) == 'XTREME':
                data_rva = entry.directory.entries[0].data.struct.OffsetToData
                size = entry.directory.entries[0].data.struct.Size
                data = pe.get_memory_mapped_image()[data_rva:data_rva+size]
                return data
    except:
        return None 


def v29(rawConfig):
    config_data = {}
    config_data["ID"] = get_unicode_string(rawConfig, 0x9e0)
    config_data["Group"] = get_unicode_string(rawConfig, 0xa5a)
    config_data["Version"] = get_unicode_string(rawConfig, 0xf2e)
    config_data["Mutex"] = get_unicode_string(rawConfig, 0xfaa)
    config_data["Install Dir"] = get_unicode_string(rawConfig, 0xb50)
    config_data["Install Name"] = get_unicode_string(rawConfig, 0xad6)
    config_data["HKLM"] = get_unicode_string(rawConfig, 0xc4f)
    config_data["HKCU"] = get_unicode_string(rawConfig, 0xcc8)
    config_data["Custom Reg Key"] = get_unicode_string(rawConfig, 0xdc0)
    config_data["Custom Reg Name"] = get_unicode_string(rawConfig, 0xe3a)
    config_data["Custom Reg Value"] = get_unicode_string(rawConfig, 0xa82)
    config_data["ActiveX Key"] = get_unicode_string(rawConfig, 0xd42)
    config_data["Injection"] = get_unicode_string(rawConfig, 0xbd2)
    config_data["FTP Server"] = get_unicode_string(rawConfig, 0x111c)
    config_data["FTP UserName"] = get_unicode_string(rawConfig, 0x1210)
    config_data["FTP Password"] = get_unicode_string(rawConfig, 0x128a)
    config_data["FTP Folder"] = get_unicode_string(rawConfig, 0x1196)
    config_data["Domain1"] = str(get_unicode_string(rawConfig, 0x50)+":"+str(unpack("<I", rawConfig[0:4])[0]))
    config_data["Domain2"] = str(get_unicode_string(rawConfig, 0xca)+":"+str(unpack("<I", rawConfig[4:8])[0]))
    config_data["Domain3"] = str(get_unicode_string(rawConfig, 0x144)+":"+str(unpack("<I", rawConfig[8:12])[0]))
    config_data["Domain4"] = str(get_unicode_string(rawConfig, 0x1be)+":"+str(unpack("<I", rawConfig[12:16])[0]))
    config_data["Domain5"] = str(get_unicode_string(rawConfig, 0x238)+":"+str(unpack("<I", rawConfig[16:20])[0]))
    config_data["Domain6"] = str(get_unicode_string(rawConfig, 0x2b2)+":"+str(unpack("<I", rawConfig[20:24])[0]))
    config_data["Domain7"] = str(get_unicode_string(rawConfig, 0x32c)+":"+str(unpack("<I", rawConfig[24:28])[0]))
    config_data["Domain8"] = str(get_unicode_string(rawConfig, 0x3a6)+":"+str(unpack("<I", rawConfig[28:32])[0]))
    config_data["Domain9"] = str(get_unicode_string(rawConfig, 0x420)+":"+str(unpack("<I", rawConfig[32:36])[0]))
    config_data["Domain10"] = str(get_unicode_string(rawConfig, 0x49a)+":"+str(unpack("<I", rawConfig[36:40])[0]))
    config_data["Domain11"] = str(get_unicode_string(rawConfig, 0x514)+":"+str(unpack("<I", rawConfig[40:44])[0]))
    config_data["Domain12"] = str(get_unicode_string(rawConfig, 0x58e)+":"+str(unpack("<I", rawConfig[44:48])[0]))
    config_data["Domain13"] = str(get_unicode_string(rawConfig, 0x608)+":"+str(unpack("<I", rawConfig[48:52])[0]))
    config_data["Domain14"] = str(get_unicode_string(rawConfig, 0x682)+":"+str(unpack("<I", rawConfig[52:56])[0]))
    config_data["Domain15"] = str(get_unicode_string(rawConfig, 0x6fc)+":"+str(unpack("<I", rawConfig[56:60])[0]))
    config_data["Domain16"] = str(get_unicode_string(rawConfig, 0x776)+":"+str(unpack("<I", rawConfig[60:64])[0]))
    config_data["Domain17"] = str(get_unicode_string(rawConfig, 0x7f0)+":"+str(unpack("<I", rawConfig[64:68])[0]))
    config_data["Domain18"] = str(get_unicode_string(rawConfig, 0x86a)+":"+str(unpack("<I", rawConfig[68:72])[0]))
    config_data["Domain19"] = str(get_unicode_string(rawConfig, 0x8e4)+":"+str(unpack("<I", rawConfig[72:76])[0]))
    config_data["Domain20"] = str(get_unicode_string(rawConfig, 0x95e)+":"+str(unpack("<I", rawConfig[76:80])[0]))
    return config_data


def v32(rawConfig):
    config_data = {}
    config_data["ID"] = get_unicode_string(rawConfig, 0x1b4)
    config_data["Group"] = get_unicode_string(rawConfig, 0x1ca)
    config_data["Version"] = get_unicode_string(rawConfig, 0x2bc)
    config_data["Mutex"] = get_unicode_string(rawConfig, 0x2d4)
    config_data["Install Dir"] = get_unicode_string(rawConfig, 0x1f8)
    config_data["Install Name"] = get_unicode_string(rawConfig, 0x1e2)
    config_data["HKLM"] = get_unicode_string(rawConfig, 0x23a)
    config_data["HKCU"] = get_unicode_string(rawConfig, 0x250)
    config_data["ActiveX Key"] = get_unicode_string(rawConfig, 0x266)
    config_data["Injection"] = get_unicode_string(rawConfig, 0x216)
    config_data["FTP Server"] = get_unicode_string(rawConfig, 0x35e)
    config_data["FTP UserName"] = get_unicode_string(rawConfig, 0x402)
    config_data["FTP Password"] = get_unicode_string(rawConfig, 0x454)
    config_data["FTP Folder"] = get_unicode_string(rawConfig, 0x3b0)
    config_data["Domain1"] = str(get_unicode_string(rawConfig, 0x14)+":"+str(unpack("<I", rawConfig[0:4])[0]))
    config_data["Domain2"] = str(get_unicode_string(rawConfig, 0x66)+":"+str(unpack("<I", rawConfig[4:8])[0]))
    config_data["Domain3"] = str(get_unicode_string(rawConfig, 0xb8)+":"+str(unpack("<I", rawConfig[8:12])[0]))
    config_data["Domain4"] = str(get_unicode_string(rawConfig, 0x10a)+":"+str(unpack("<I", rawConfig[12:16])[0]))
    config_data["Domain5"] = str(get_unicode_string(rawConfig, 0x15c)+":"+str(unpack("<I", rawConfig[16:20])[0]))
    config_data["Msg Box Title"] = get_unicode_string(rawConfig, 0x50c)
    config_data["Msg Box Text"] = get_unicode_string(rawConfig, 0x522)
    return config_data


def v35(config_raw):
    config_data = {}
    config_data['ID'] = get_unicode_string(config_raw, 0x1b4)
    config_data['Group'] = get_unicode_string(config_raw, 0x1ca)
    config_data['Version'] = get_unicode_string(config_raw, 0x2d8)
    config_data['Mutex'] = get_unicode_string(config_raw, 0x2f0)
    config_data['Install Dir'] = get_unicode_string(config_raw, 0x1f8)
    config_data['Install Name'] = get_unicode_string(config_raw, 0x1e2)
    config_data['HKLM'] = get_unicode_string(config_raw, 0x23a)
    config_data['HKCU'] = get_unicode_string(config_raw, 0x250)
    config_data['ActiveX Key'] = get_unicode_string(config_raw, 0x266)
    config_data['Injection'] = get_unicode_string(config_raw, 0x216)
    config_data['FTP Server'] = get_unicode_string(config_raw, 0x380)
    config_data['FTP UserName'] = get_unicode_string(config_raw, 0x422)
    config_data['FTP Password'] = get_unicode_string(config_raw, 0x476)
    config_data['FTP Folder'] = get_unicode_string(config_raw, 0x3d2)
    config_data['Domain1'] = str(get_unicode_string(config_raw, 0x14)+':'+str(unpack('<I', config_raw[0:4])[0]))
    config_data['Domain2'] = str(get_unicode_string(config_raw, 0x66)+':'+str(unpack('<I', config_raw[4:8])[0]))
    config_data['Domain3'] = str(get_unicode_string(config_raw, 0xb8)+':'+str(unpack('<I', config_raw[8:12])[0]))
    config_data['Domain4'] = str(get_unicode_string(config_raw, 0x10a)+':'+str(unpack('<I', config_raw[12:16])[0]))
    config_data['Domain5'] = str(get_unicode_string(config_raw, 0x15c)+':'+str(unpack('<I', config_raw[16:20])[0]))
    config_data['Msg Box Title'] = get_unicode_string(config_raw, 0x52c)
    config_data['Msg Box Text'] = get_unicode_string(config_raw, 0x542)
    return config_data


def config(data):
    key = 'C\x00O\x00N\x00F\x00I\x00G'

    config_coded = extract_config(data)
    config_raw = rc4crypt(config_coded, key)

    # 1.3.x - Not implemented yet.
    if len(config_raw) == 0xe10:
        config_data = None
    # 2.9.x - Not a stable extract.
    elif len(config_raw) == 0x1390 or len(config_raw) == 0x1392:
        config_data = v29(config_raw)
    # 3.1 & 3.2
    elif len(config_raw) == 0x5Cc:
        config_data = v32(config_raw)
    # 3.5
    elif len(config_raw) == 0x7f0:
        config_data = v35(config_raw)
    else:
        config_data = None

    return config_data
