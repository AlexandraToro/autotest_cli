from checkout import checkout
import yaml

with open('config.yml', 'r', encoding='utf8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_folder1 = data['FOLDER_folder1']


def test_step1(clear_dir, get_dir, make_file):
    res1 = checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2", "Everything is Ok")
    res2 = checkout(f"ls {FOLDER_OUT}", "arx2.7z")
    assert res1 and res2, "test1 FAIL"


def test_step2(clear_dir, get_dir, make_file):
    res = []
    res.append(checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2", "Everything is Ok"))
    res.append(checkout(f"cd {FOLDER_OUT}; 7z e arx2.7z -o{FOLDER_folder1} -y", "Everything is Ok"))
    for i in make_file:
        res.append(checkout(f"ls {FOLDER_folder1}", i))
    assert all(res), "test2 FAIL"


def test_step3():
    assert checkout(f"cd {FOLDER_OUT}; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"


def test_step4(get_list):
    assert checkout(f"cd {FOLDER_OUT}; 7z d arx2.7z {get_list[0]} ", "Everything is Ok"), "test4 FAIL"


def test_step5(get_list):
    assert checkout(
        f"cd {FOLDER_TST}; echo 'hello' >> {get_list[1]}; cd {FOLDER_OUT}; 7z u arx2.7z {FOLDER_TST}/{get_list[1]}",
        "Everything is Ok"), "test5 FAIL"


# Дополнить проект тестами, проверяющими команду вывода списка файлов (l)
def test_step6(get_list):
    res = []
    for i in get_list:
        res.append(checkout('7z l arx2.7z', i))
    assert res, "test6 FAIL"


# Дополнить проект тестами, проверяющими команду разархивирования с путями (x)
def test_step7(clear_dir, get_dir, make_file, get_subfolder_and_file):
    res = []
    res.append(checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2", "Everything is Ok"))
    res.append(checkout(f"cd {FOLDER_OUT}; 7z x arx2.7z -o{FOLDER_folder1} -y", "Everything is Ok"))
    for i in make_file:
        res.append(checkout(f"ls {FOLDER_folder1}", i))
    if checkout(f'cd {FOLDER_folder1}/{get_subfolder_and_file[0]}'):
        for i in get_subfolder_and_file[1]:
            res.append(checkout(f'ls', i))
    assert res, "test7 FAIL"


# Доработать проект, добавив тест команды расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.
def test_step8(clear_dir, get_dir, make_file):
    res = []
    res.append(checkout(f"cd {FOLDER_TST}; 7z a {FOLDER_OUT}/arx2", "Everything is Ok"))
    test_hash = checkout(f"cd {FOLDER_OUT}; crc32 arx2.7z")
    res.append(checkout(f"cd {FOLDER_OUT}; 7z h arx2.7z", f"{test_hash}"))
    assert res, "test8 FAIL"
