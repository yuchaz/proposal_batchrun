import os
import sqlite3
import pandas as pd
from path_handler import get_path
from utils import execute
import logging
from glob import glob
from shutil import copy2, move
import time

opsim_hostname = os.environ['OPSIM_HOSTNAME']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('batchrun.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Start batch run on proposal scheduler')

run_dir = get_path()
unfinished_dir = os.path.abspath('unfinished_config')
finished_dir = os.path.abspath('finished_config')
config_dir = os.path.abspath('config_dir')

if not os.path.exists(config_dir):
    os.makedirs(config_dir)
if not os.path.exists(finished_dir):
    os.makedirs(finished_dir)
if not os.path.exists(run_dir):
    error_str = 'Path {} not found, please check your setup.py'.format(run_dir)
    logger.error(error_str)
    raise FileNotFoundError(error_str)
if not os.path.exists(unfinished_dir):
    error_str = 'Path {} not found, unfinished_dir should be given'
    logger.error(error_str)
    raise FileNotFoundError(error_str)


session_db = os.path.join(run_dir, 'output',
                          '{}_sessions.db'.format(opsim_hostname))


def get_latest_sessionid(plus_one=True):
    if not os.path.exists(session_db):
        default_run_name = '{}_2000'.format(opsim_hostname)
        logger.warning('Session DB not found, will use '
                       'the default run_name {}'.format(default_run_name))
        return default_run_name
    con = sqlite3.connect(session_db)
    out = pd.read_sql('SELECT sessionHost, sessionId as s from Session '
                      'order by s desc limit 1', con)
    session_id = out['s'][0]
    if plus_one:
        session_id += 1
    return '{}_{}'.format(out['sessionHost'][0], session_id)


for config_directory in glob(os.path.join(unfinished_dir, '*')):
    logger.info('Running with config: {}'.format(config_directory))
    config_dir_name = config_directory.split('/')[-1]
    next_session_id = get_latest_sessionid()
    logger.info('Running opsim with session ID: {}'.format(next_session_id))
    for pyconfigs in glob(os.path.join(config_directory, '*.py')):
        copy2(pyconfigs, config_dir)
    execute(['./run_opsim.sh {} {}'.format(run_dir, config_dir)])
    logger.info('Finish running {}'.format(next_session_id))
    new_path_in_finished_config = os.path.join(finished_dir, '{}_{}'.format(
        next_session_id, config_dir_name))
    os.makedirs(new_path_in_finished_config)
    for pyconfigs in glob(os.path.join(config_dir, '*.py')):
        config_file_name = pyconfigs.split('/')[-1]
        move(pyconfigs, os.path.join(
            new_path_in_finished_config, config_file_name))
    logger.info('Finish moving configs to new path in {}'.format(
        new_path_in_finished_config))

    time.sleep(1)
