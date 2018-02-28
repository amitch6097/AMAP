import string
import pefile
from binascii import *

BASE_CONFIG = {
    'FWB': '',
    'GENCODE': '',
    'MUTEX': '',
    'NETDATA': '',
    'OFFLINEK': '',
    'SID': '',
    'FTPUPLOADK': '',
    'FTPHOST': '',
    'FTPUSER': '',
    'FTPPASS': '',
    'FTPPORT': '',
    'FTPSIZE': '',
    'FTPROOT': '',
    'PWD': ''
}

def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
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

def v3_data(data, key):
    config = BASE_CONFIG
    dec = rc4crypt(unhexlify(data), key)
    config[str(entry.name)] = dec

    return config

def v51_data(data, key):
    config = BASE_CONFIG
    dec = rc4crypt(unhexlify(data), key)
    dec_list = dec.split('\n')
    for entries in dec_list[1:-1]:
        key, value = entries.split('=')
        key = key.strip()
        value = value.rstrip()[1:-1]
        clean_value = filter(lambda x: x in string.printable, value)
        config[key] = clean_value

    return config

def version_check(raw_data):
    if '#KCMDDC2#' in raw_data:
        return '#KCMDDC2#-890' 
    elif '#KCMDDC4#' in raw_data:
        return '#KCMDDC4#-890'
    elif '#KCMDDC42#' in raw_data:
        return '#KCMDDC42#-890'
    elif '#KCMDDC42F#' in raw_data:
        return '#KCMDDC42F#-890'
    elif '#KCMDDC5#' in raw_data:
        return '#KCMDDC5#-890'
    elif '#KCMDDC51#' in raw_data:
        return '#KCMDDC51#-890'
    else:
        return None

def offset_check(raw_data):
    j = raw_data.find("#KCMDDC")
    thisprog = raw_data[:j][::-1].find('This program'[::-1])
    mz = raw_data[:j-thisprog][::-1].find('ZM')
    start = j - thisprog - mz - 2
    return start

def extract_config(raw_data, key):
    raw_config = BASE_CONFIG

    pe = pefile.PE(data=raw_data)
    
    rt_string_idx = [
        entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries
    ].index(pefile.RESOURCE_TYPE['RT_RCDATA'])
    rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]
    
    entry_names = [str(x.name) for x in rt_string_directory.directory.entries]
    print('\n'.join(entry_names))
    print(str(sum([1 for x in raw_config.keys() if x in entry_names])))
    if 'DCDATA' not in entry_names and (sum([1 for x in raw_config.keys() if x in entry_names]) == 0):
        off = offset_check(raw_data)
        pe = pefile.PE(data=raw_data[off:])
        rt_string_idx = [
            entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries
        ].index(pefile.RESOURCE_TYPE['RT_RCDATA'])
        rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]

    for entry in rt_string_directory.directory.entries:
        if str(entry.name) == 'DCDATA':
            data_rva = entry.directory.entries[0].data.struct.OffsetToData
            size = entry.directory.entries[0].data.struct.Size
            data = pe.get_memory_mapped_image()[data_rva:data_rva+size]
            raw_config = v51_data(data, key)
        elif str(entry.name) in raw_config.keys():
            data_rva = entry.directory.entries[0].data.struct.OffsetToData
            size = entry.directory.entries[0].data.struct.Size
            data = pe.get_memory_mapped_image()[data_rva:data_rva+size]
            dec = rc4crypt(unhexlify(data), key)
            raw_config[str(entry.name)] = filter(lambda x: x in string.printable, dec)

    return config_clean(raw_config)

def config_clean(raw_config):
    try:
        newConf = {}
        newConf["FireWallBypass"] = raw_config["FWB"]
        newConf["FTPHost"] = raw_config["FTPHOST"]
        newConf["FTPPassword"] = raw_config["FTPPASS"]
        newConf["FTPPort"] = raw_config["FTPPORT"]
        newConf["FTPRoot"] = raw_config["FTPROOT"]
        newConf["FTPSize"] = raw_config["FTPSIZE"]
        newConf["FTPKeyLogs"] = raw_config["FTPUPLOADK"]
        newConf["FTPUserName"] = raw_config["FTPUSER"]
        newConf["Gencode"] = raw_config["GENCODE"]
        newConf["Mutex"] = raw_config["MUTEX"]
        newConf["Domains"] = raw_config["NETDATA"]
        newConf["OfflineKeylogger"] = raw_config["OFFLINEK"]
        newConf["Password"] = raw_config["PWD"]
        newConf["CampaignID"] = raw_config["SID"]
        newConf["Version"] = raw_config["Version"]
        return newConf
    except:
        return raw_config

        
def config(data):
    versionKey = version_check(data)
    if versionKey:
        conf_data =  extract_config(data, versionKey)
        return conf_data
    else:
        return None

