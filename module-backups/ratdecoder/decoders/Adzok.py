from zipfile import ZipFile
from cStringIO import StringIO
import re


def parse_config(raw_config):
    config_dict = {}
    for line in raw_config.split('\n'):
        if line.startswith('<comment'):
            config_dict['Version'] = re.findall('>(.*?)</comment>', line)[0]
        if line.startswith('<entry key'):
            try:
                config_dict[re.findall('key="(.*?)"', line)[0]] = re.findall('>(.*?)</entry', line)[0]
            except:
                config_dict[re.findall('key="(.*?)"', line)[0]] = 'Not Set'
            finally:
                pass

    # Tidy the config
    clean_config = {}
    for k, v in config_dict.iteritems():
        if k == 'dir':
            clean_config['Install Path'] = v
        if k == 'reg':
            clean_config['Registrey Key'] = v
        if k == 'pass':
            clean_config['Password'] = v
        if k == 'hidden':
            clean_config['Hidden'] = v
        if k == 'puerto':
            clean_config['Port'] = v
        if k == 'ip':
            clean_config['Domain'] = v
        if k == 'inicio':
            clean_config['Install'] = v

    return clean_config


def config(data):
    new_zip = StringIO(data)
    raw_config = {}
    with ZipFile(new_zip, 'r') as jar:
        for name in jar.namelist():
            if name == "config.xml": # contains the encryption key
                raw_config = jar.read(name)
                new_config = parse_config(raw_config)
                return new_config
