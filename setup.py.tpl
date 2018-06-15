from path_handler import path_config_writer
import os

run_dir = '_PLEASE_CHANGE_PATH_OF_RUN_DIR'


###############################################################################
####################### START WRITING PATH CONFIGS ############################
###############################################################################

def write_config():
    if '_PLEASE_CHANGE' in run_dir:
        raise ValueError('Please change pathes in setup.py')
    elif not os.path.exists(run_dir):
        raise FileNotFoundError('Please enter the correct path')

    path_config_writer(run_dir)

if __name__ == '__main__':
    write_config()
