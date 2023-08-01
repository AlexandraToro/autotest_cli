import subprocess


def checkout(cmd, text=""):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in res.stdout and res.returncode == 0) or text in res.stderr:
        return True
    else:
        return False


def get_out(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    return res.stdout.strip().split("\n"), res.stderr

