import os
import sqlite3
import pandas as pd
from path_handler import get_path
from utils import execute
import logging
from glob import glob
from shutil import copy2, move
import time
from git import Repo
from git.exc import GitCommandError
import argparse

opsim_hostname = os.environ['OPSIM_HOSTNAME']
parser = argparse.ArgumentParser(
    description='Run batch proposal scheduler')
parser.add_argument('--run-branches', '-bs', type=str, nargs='+',
                    default=['master'],
                    help='The branches to run')

args = parser.parse_args()
batchrun_branches = list(set(args.run_branches))

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
config_dir = os.path.abspath('config_dir')
repo_dir = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(config_dir):
    os.makedirs(config_dir)
if not os.path.exists(run_dir):
    error_str = 'Path {} not found, please check your setup.py'.format(run_dir)
    logger.error(error_str)
    raise FileNotFoundError(error_str)

repo = Repo(repo_dir)

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


for branch in batchrun_branches:
    logger.info('Running with branch: {}'.format(branch))
    next_session_id = get_latest_sessionid()
    try:
        repo.git.checkout(branch)
    except GitCommandError:
        logger.error('git branch {} not found, skip this branch'.format(branch))
        continue
    logger.info('Running opsim with session ID: {}'.format(next_session_id))
    execute(['./run_opsim.sh {} {}'.format(run_dir, config_dir)])
    logger.info('Finish running {}'.format(next_session_id))
    new_branch_name = '{}_{}'.format(next_session_id, branch)
    logger.info('Saving configs to new branch {}'.format(new_branch_name))
    repo.git.checkout('-b', new_branch_name)
    repo.git.checkout('master')
    repo.git.checkout('--', '.')
    time.sleep(1)

logger.info('End simulation...')
