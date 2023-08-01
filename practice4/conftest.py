import random
import string
from datetime import datetime

import pytest
import yaml
from ssh_checkout import ssh_getout, ssh_checkout, upload_files

with open('config.yml', 'r') as f:
    data = yaml.safe_load(f)

FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_folder1 = data['FOLDER_folder1']
TYPE = data['type']
HOST = data['host']
USER = data['user']
PASSWD = data['passwd']


@pytest.fixture()
def get_dir():
    return ssh_checkout(HOST, USER, PASSWD,f"mkdir {FOLDER_OUT} {FOLDER_TST} {FOLDER_folder1}", "")


@pytest.fixture()
def make_file():
    list_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        if ssh_checkout(HOST, USER, PASSWD,
                f'cd {FOLDER_TST}; dd if=/dev/urandom of={filename} bs={data["size"]} count={data["count"]} iflag=fullblock',
                ""):
            list_files.append(filename)
    return list_files


@pytest.fixture()
def clear_dir():
    return ssh_checkout(HOST, USER, PASSWD,f"rm -rf {FOLDER_OUT} {FOLDER_TST} {FOLDER_folder1}", "")


@pytest.fixture()
def get_list():
    return ssh_getout(HOST, USER, PASSWD,f'ls {FOLDER_TST}')


@pytest.fixture()
def get_bad_file():
    ssh_checkout(HOST, USER, PASSWD,f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx_bad", "Everything is Ok")
    ssh_checkout(HOST, USER, PASSWD,f"truncate -s 1 {FOLDER_OUT}/arx_bad.7z")
    yield "arx_bad"
    ssh_checkout(HOST, USER, PASSWD, f"rm -rf {FOLDER_OUT}/arx_bad")


@pytest.fixture()
def get_subfolder_and_file():
    list_files = []
    folder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    if ssh_checkout("0.0.0.0", "testuser", "123",f"cd {FOLDER_TST}; mkdir {folder_name}", ""):
        for i in range(data['count']):
            filename = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            if ssh_checkout("0.0.0.0", "testuser", "123",
                    f'cd {FOLDER_TST}/{folder_name}; dd if=/dev/urandom of={filename} bs={data["size"]} '
                    f'count={data["count"]} iflag=fullblock',
                    ""):
                list_files.append(filename)
    return folder_name, list_files


@pytest.fixture(autouse=True)
def get_stat():
    yield
    stat = ssh_getout("0.0.0.0", "testuser", "123","cat /proc/loadavg")
    ssh_checkout("0.0.0.0", "testuser", "123",f"echo 'time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data['count']} size: {data['size']} "
             f"load: {stat}'>> stat.txt", "")


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
