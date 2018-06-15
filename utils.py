from subprocess import Popen

def execute(commands):
    with Popen(commands, shell=True) as process:
        try:
            process.communicate()
        except Exception as e:
            process.kill()
            raise e
