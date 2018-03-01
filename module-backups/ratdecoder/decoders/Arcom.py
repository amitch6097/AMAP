import base64
import string
from Crypto.Cipher import Blowfish

def decrypt_blowfish(raw_data):
    key = 'CVu3388fnek3W(3ij3fkp0930di'
    cipher = Blowfish.new(key)
    return cipher.decrypt(raw_data)

def config(data):
    conf_data = {}
    config_raw = data.split('\x18\x12\x00\x00')[1].replace('\xA3\x24\x25\x21\x64\x01\x00\x00', '')
    config_decoded = base64.b64decode(config_raw)
    config_decrypted = decrypt_blowfish(config_decoded)
    parts = config_decrypted.split('|')

    if len(parts) > 3:
        conf_data['Domain'] = parts[0]
        conf_data['Port'] = parts[1]
        conf_data['Install Path'] = parts[2]
        conf_data['Install Name'] = parts[3]
        conf_data['Startup Key'] = parts[4]
        conf_data['Campaign ID'] = parts[5]
        conf_data['Mutex Main'] = parts[6]
        conf_data['Mutex Per'] = parts[7]
        conf_data['YPER'] = parts[8]
        conf_data['YGRB'] = parts[9]
        conf_data['Mutex Grabber'] = parts[10]
        conf_data['Screen Rec Link'] = parts[11]
        conf_data['Mutex 4'] = parts[12]
        conf_data['YVID'] = parts[13]
        conf_data['YIM'] = parts[14]
        conf_data['NO'] = parts[15]
        conf_data['Smart Broadcast'] = parts[16]
        conf_data['YES'] = parts[17]
        conf_data['Plugins'] = parts[18]
        conf_data['Flag1'] = parts[19]
        conf_data['Flag2'] = parts[20]
        conf_data['Flag3'] = parts[21]
        conf_data['Flag4'] = parts[22]
        conf_data['WebPanel'] = parts[23]
        conf_data['Remote Delay'] = parts[24]
    return conf_data
