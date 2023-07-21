# Задание 2. (повышенной сложности)
#
# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.


import subprocess
import re


def find_text(command: str, text: str, advance: bool = False) -> bool:
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if res.returncode == 0:
        if advance:
            new_res = res.stdout.replace('_', ' ')
            new_res = re.sub(r'\W+', ' ', new_res)
            my_list = new_res.split(" ")
            print(my_list)
            if text in new_res:
                return True
            else:
                return False
        else:
            my_list = res.stdout.split("\n")
            if text in my_list:
                return True
            else:
                return False
    else:
        return False


if __name__ == '__main__':
    print(find_text("cat /etc/os-release", "VERSION_CODENAME=jammy"))
    print(find_text("cat /etc/os-release", "jammy", advance=True))
