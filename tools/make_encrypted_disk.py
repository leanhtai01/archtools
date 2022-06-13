# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
if __package__ is None:
    import os
    import sys

    sys.path.append(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
import subprocess
from getpass import getpass

from lib import diskutils


def main():
    subprocess.run(['lsblk'])
    device = input('Enter device to encrypt (e.g. sda, sdb,...): ')
    encrypt_name = input('Enter name for encrypted device: ')

    password = getpass('Enter password: ')
    re_enter_password = getpass('Enter password again: ')
    while password != re_enter_password:
        print('Two password is not the same!')
        password = getpass('Enter password: ')
        re_enter_password = getpass('Enter password again: ')

    username = input('Enter username: ')

    diskutils.encrypt_device(device, encrypt_name, username, password)


if __name__ == '__main__':
    main()
