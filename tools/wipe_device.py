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

from lib import diskutils


def main():
    subprocess.run(['lsblk'])
    device = input('Enter device to wipe (e.g. nvme0n1, sda, sdb): ')

    diskutils.wipe_device(device)

    # display wiped device's information
    subprocess.run(['lsblk'])
    subprocess.run(['parted', f'/dev/{device}', 'print'])
    print(f'Successfully wipe {device}!')


if __name__ == '__main__':
    main()
