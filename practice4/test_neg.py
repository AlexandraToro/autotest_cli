import yaml
from ssh_checkout import ssh_checkout_negative

with open('config.yml', 'r', encoding='utf8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_folder1 = data['FOLDER_folder1']
TYPE = data['type']
HOST = data['host']
USER = data['user']
PASSWD = data['passwd']


def test_step1(clear_dir, get_dir, get_bad_file):
    assert ssh_checkout_negative(HOST, USER, PASSWD, f"cd {FOLDER_OUT}; 7z e arx_bad.{TYPE} -o{FOLDER_folder1} -y",
                        f"Open ERROR: Can not open the file as [{TYPE}] archive"), "test2 FAIL"


def test_step2(get_bad_file):
    assert ssh_checkout_negative(HOST, USER, PASSWD, f"cd {FOLDER_OUT}; 7z t arx_bad.{TYPE}",
                        f"Can not open the file as [{TYPE}] archive"), "test3 FAIL"
