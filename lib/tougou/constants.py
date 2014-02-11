import ConfigParser
import os

def get_config(p, section, key, env_var, default):
    if env_var is not None:
        value = os.environ.get(env_var, None)
        if value is not None:
            return value
    if p is not None:
        try:
            return p.get(section, key, raw=True)
        except:
            return default
    return default


def load_config_file():
    p = ConfigParser.ConfigParser()
    path1 = os.getcwd() + "tougou.cfg"
    path2 = os.path.expanduser(os.environ.get('TOUGOU_CONFIG', "~/tougou.cfg"))
    path3 = "/etc/tougou/tougou.cfg"

    if os.path.exists(path1):
        p.read(path1)
    elif os.path.exists(path2):
        p.read(path2)
    elif os.path.exists(path3):
        p.read(path3)
    else:
        return None
    return p

p = load_config_file()
