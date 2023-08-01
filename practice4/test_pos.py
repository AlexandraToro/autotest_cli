from checkout import deploy, save_log
from ssh_checkout import ssh_checkout, ssh_getout, upload_files
import yaml

with open('config.yml', 'r', encoding='utf8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_folder1 = data['FOLDER_folder1']
TYPE = data['type']
HOST = data['host']
USER = data['user']
PASSWD = data['passwd']



def test_step1(start_time):
    save_log(start_time, 'log1')
    assert all(deploy()), "test1 FAIL"


def test_step2(clear_dir, get_dir, make_file, start_time):
    res1 = ssh_checkout(HOST, USER, PASSWD, f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2",
                        "Everything is Ok")
    res2 = ssh_checkout(HOST, USER, PASSWD,  f"ls {FOLDER_OUT}", f"arx2.{TYPE}")
    save_log(start_time, 'log2')
    assert res1 and res2, "test2 FAIL"


def test_step3(clear_dir, get_dir, make_file, start_time):
    res = []
    res.append(ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2 -t{TYPE}",
                            "Everything is Ok"))
    res.append(ssh_checkout(HOST, USER, PASSWD, f"cd {FOLDER_OUT}; 7z e arx2.{TYPE} -o{FOLDER_folder1} -y",
                            "Everything is Ok"))
    for i in make_file:
        res.append(ssh_checkout(HOST, USER, PASSWD, f"ls {FOLDER_folder1}", i))
    save_log(start_time, 'log3')
    assert all(res), "test3 FAIL"


def test_step4(start_time):
    save_log(start_time, 'log4')
    assert ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_OUT}; 7z t arx2.{TYPE}",
                        "Everything is Ok"), "test4 FAIL"


def test_step5(get_list, start_time):
    save_log(start_time, 'log5')
    assert ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_OUT}; 7z d arx2.{TYPE} {get_list[0]} ",
                        "Everything is Ok"), "test5 FAIL"


def test_step6(get_list, start_time):
    save_log(start_time, 'log6')
    assert ssh_checkout(
        HOST, USER, PASSWD,
        f"cd {FOLDER_TST}; echo 'hello' >> {get_list[1]}; cd {FOLDER_OUT}; 7z u arx2.{TYPE} {FOLDER_TST}/{get_list[1]}",
        "Everything is Ok"), "test6 FAIL"


# Дополнить проект тестами, проверяющими команду вывода списка файлов (l)
def test_step7(get_list, start_time):
    save_log(start_time, 'log7')
    res = []
    for i in get_list:
        res.append(ssh_checkout(HOST, USER, PASSWD,  f'7z l arx2.{TYPE}', i))
    assert res, "test7 FAIL"


# Дополнить проект тестами, проверяющими команду разархивирования с путями (x)
def test_step8(clear_dir, get_dir, make_file, get_subfolder_and_file, start_time):
    res = []
    res.append(ssh_checkout(HOST, USER, PASSWD, f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2 -t{TYPE}",
                            "Everything is Ok"))
    res.append(ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_OUT}; 7z x arx2.{TYPE} -o{FOLDER_folder1} -y",
                            "Everything is Ok"))
    for i in make_file:
        res.append(ssh_checkout(HOST, USER, PASSWD,  f"ls {FOLDER_folder1}", i))
    if ssh_checkout(HOST, USER, PASSWD, f'cd {FOLDER_folder1}/{get_subfolder_and_file[0]}'):
        for i in get_subfolder_and_file[1]:
            res.append(ssh_checkout(HOST, USER, PASSWD,  f'ls', i))
    save_log(start_time, 'log8')
    assert res, "test8 FAIL"


# Доработать проект, добавив тест команды расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.
def test_step9(clear_dir, get_dir, make_file, start_time):
    res = []
    res.append(ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2 -t{TYPE}",
                            "Everything is Ok"))
    test_hash = ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_OUT}; crc32 arx2.{TYPE}")
    res.append(ssh_checkout(HOST, USER, PASSWD,  f"cd {FOLDER_OUT}; 7z h arx2.7{TYPE}", f"{test_hash}"))
    save_log(start_time, 'log9')
    assert res, "test9 FAIL"
