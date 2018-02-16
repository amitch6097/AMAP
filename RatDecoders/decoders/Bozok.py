import pefile

def extract_config(raw_data):
    pe = pefile.PE(data=raw_data)

    try:
        rt_string_idx = [
            entry.id for entry in 
            pe.DIRECTORY_ENTRY_RESOURCE.entries
        ].index(pefile.RESOURCE_TYPE['RT_RCDATA'])
    except:
        return None

    rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]

    for entry in rt_string_directory.directory.entries:
        if str(entry.name) == 'CFG':
            data_rva = entry.directory.entries[0].data.struct.OffsetToData
            size = entry.directory.entries[0].data.struct.Size
            data = pe.get_memory_mapped_image()[data_rva:data_rva+size]
            return data
                
def config(data):
    try:
        conf_dict = {}
        config_raw = extract_config(data).replace('\x00', '')

        if not config_raw:
            return None

        config_fields = config_raw.split('|')

        if config_fields:
            conf_dict['ServerID'] = config_fields[0]
            conf_dict['Mutex'] = config_fields[1]
            conf_dict['InstallName'] = config_fields[2]
            conf_dict['StartupName'] = config_fields[3]
            conf_dict['Extension'] = config_fields[4]
            conf_dict['Password'] = config_fields[5]
            conf_dict['Install Flag'] = config_fields[6]
            conf_dict['Startup Flag'] = config_fields[7]
            conf_dict['Visible Flag'] = config_fields[8]
            conf_dict['Unknown Flag1'] = config_fields[9]
            conf_dict['Unknown Flag2'] = config_fields[10]
            conf_dict['Port'] = config_fields[11]
            conf_dict['Domain'] = config_fields[12]
            conf_dict['Unknown Flag3'] = config_fields[13]
        return conf_dict
    except:
        return None