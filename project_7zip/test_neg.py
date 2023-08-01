import yaml

from checkout import checkout

with open('config.yml', 'r', encoding='utf8') as f:
    data = yaml.safe_load(f)
FOLDER_TST = data["FOLDER_TST"]
FOLDER_OUT = data['FOLDER_OUT']
FOLDER_folder1 = data['FOLDER_folder1']


def test_step1(get_bad_file):
    assert checkout(f"cd {FOLDER_OUT}; 7z e arx_bad.7z -o{FOLDER_folder1} -y",
                    "Can not open the file as [7z] archive"), "test1 FAIL"


def test_step2(get_bad_file):
    assert checkout(f"cd {FOLDER_OUT}; 7z t arx_bad.7z", "Can not open the file as [7z] archive"), "test2 FAIL"
