# Docker setup
Be sure to run the following commands when starting the docker image each time so that the script can be run without being stopped.
```
git config --global user.email "EMAIL"
git config --global user.name "USER"
```

Install GitPython for stable git version control in python script
```
pip install gitpython
```


# Path setup
1. run `cp setup.py.tpl setup.py`
1. Edit the `run_dir` in `setup.py`
1. run `python setup.py` for setting up `path.cfg`


# CLI
1. Use `python run_batch.py --help` for seeing instructions.
1. `--run-branches`: branches to run. Will skip the non-exists branches

## Example commands
`python run_batch.py --run-branches batchrun1 batchrun2`
Where `batchrun1` and `batchrun2` is the branches that contains the edited config files.
