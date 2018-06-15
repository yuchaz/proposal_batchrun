import configparser
import os

config = configparser.SafeConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir,'path.cfg')

def path_config_writer(run_dir):
    config.add_section("path")
    config.set("path", "run_dir", run_dir)
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def get_path():
    config.read(config_file)
    return config.get('path', 'run_dir')
