# Задание 1.
#
# Условие:
# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess


def find_text(command: str, text: str) -> bool:
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if res.returncode == 0:
        my_list = res.stdout.split("\n")
        if text in my_list:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    print(find_text("cat /etc/os-release", "VERSION_CODENAME=jammy"))
