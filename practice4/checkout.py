import subprocess
from ssh_checkout import ssh_checkout, upload_files
import yaml

with open('config.yml', 'r', encoding='utf8') as f:
    data = yaml.safe_load(f)
HOST = data['host']
USER = data['user']
PASSWD = data['passwd']


def checkout(cmd, text=""):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in res.stdout and res.returncode == 0) or text in res.stderr:
        return True
    else:
        return False


def get_out(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    return res.stdout.strip().split("\n"), res.stderr


def deploy():
    res = []
    upload_files(HOST, USER, PASSWD, "/home/taya/p7zip-full.deb", "/home/testuser/p7zip-full.deb")
    res.append(ssh_checkout(HOST, USER, PASSWD, "echo '123' | sudo -S dpkg -i /home/testuser/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout(HOST, USER, PASSWD, "echo '123' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return res


def save_log(start_time, name):
    print(start_time)
    with open(f'./logs/{name}', 'w', encoding='utf8') as f:
        f.write(''.join(get_out(f"journalctl -p 6 --since '{start_time}'")[0]))
