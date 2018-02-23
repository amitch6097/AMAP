import string
import pefile

def string_print(line):
    return filter(lambda x: x in string.printable, line)

def xor(data):
    key = 0xBC
    encoded = bytearray(data)
    for i in range(len(encoded)):
        encoded[i] ^= key
    return str(encoded).decode('ascii', 'replace')

def extract_config(raw_data):
    try:
        pe = pefile.PE(data=raw_data)

        try:
            rt_string_idx = [
                entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries
            ].index(pefile.RESOURCE_TYPE['RT_RCDATA'])
        except ValueError, e:
            return None
        except AttributeError, e:
            return None

        rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]

        for entry in rt_string_directory.directory.entries:
            if str(entry.name) == 'XX-XX-XX-XX' or str(entry.name) == 'CG-CG-CG-CG':
                data_rva = entry.directory.entries[0].data.struct.OffsetToData
                size = entry.directory.entries[0].data.struct.Size
                data = pe.get_memory_mapped_image()[data_rva:data_rva+size]
                config = data.split('####@####')
                return config
    except:
        return None
    
def config(data):
    conf = {}
    raw_conf = extract_config(data)
    if raw_conf:
        if len(raw_conf) > 20:
            domains = ''
            ports = ''
            #Config sections 0 - 19 contain a list of Domains and Ports
            for i in range(0,19):
                if len(raw_conf[i]) > 1:
                    domains += xor(raw_conf[i]).split(':')[0]
                    domains += ','
                    ports += xor(raw_conf[i]).split(':')[1]
                    ports += ','
                
            conf['Domain'] = domains
            conf['Port'] = ports
            conf['CampaignID'] = string_print(xor(raw_conf[20]))
            conf['Password'] = string_print(xor(raw_conf[21]))
            conf['InstallFlag'] = string_print(xor(raw_conf[22]))
            conf['InstallDir'] = string_print(xor(raw_conf[25]))
            conf['InstallFileName'] = string_print(xor(raw_conf[26]))
            conf['ActiveXStartup'] = string_print(xor(raw_conf[27]))
            conf['REGKeyHKLM'] = string_print(xor(raw_conf[28]))
            conf['REGKeyHKCU'] = string_print(xor(raw_conf[29]))
            conf['EnableMessageBox'] = string_print(xor(raw_conf[30]))
            conf['MessageBoxIcon'] = string_print(xor(raw_conf[31]))
            conf['MessageBoxButton'] = string_print(xor(raw_conf[32]))
            conf['InstallMessageTitle'] = string_print(xor(raw_conf[33]))
            conf['InstallMessageBox'] = string_print(xor(raw_conf[34]))
            conf['ActivateKeylogger'] = string_print(xor(raw_conf[35]))
            conf['KeyloggerBackspace'] = string_print(xor(raw_conf[36]))
            conf['KeyloggerEnableFTP'] = string_print(xor(raw_conf[37]))
            conf['FTPAddress'] = string_print(xor(raw_conf[38]))
            conf['FTPDirectory'] = string_print(xor(raw_conf[39]))
            conf['FTPUserName'] = string_print(xor(raw_conf[41]))
            conf['FTPPassword'] = string_print(xor(raw_conf[42]))
            conf['FTPPort'] = string_print(xor(raw_conf[43]))
            conf['FTPInterval'] = string_print(xor(raw_conf[44]))
            conf['Persistance'] = string_print(xor(raw_conf[59]))
            conf['HideFile'] = string_print(xor(raw_conf[60]))
            conf['ChangeCreationDate'] = string_print(xor(raw_conf[61]))
            conf['Mutex'] = string_print(xor(raw_conf[62]))        
            conf['MeltFile'] = string_print(xor(raw_conf[63]))
            conf['CyberGateVersion'] = string_print(xor(raw_conf[67]))      
            conf['StartupPolicies'] = string_print(xor(raw_conf[69]))
            conf['USBSpread'] = string_print(xor(raw_conf[70]))
            #conf['P2PSpread'] = string_print(xor(raw_conf[71])
            #conf['GoogleChromePasswords'] = string_print(xor(raw_conf[73]))

        if xor(raw_conf[57]) == 0 or xor(raw_conf[57]) == None:
            conf['ProcessInjection'] = 'Disabled'
        elif xor(raw_conf[57]) == 1:
            conf['ProcessInjection'] = 'Default Browser'
        elif xor(raw_conf[57]) == 2:
            conf['ProcessInjection'] = xor(raw_conf[58])

        return conf