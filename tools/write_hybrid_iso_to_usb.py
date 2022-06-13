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
import time

from lib import diskutils


def main():
    subprocess.run(['lsblk'])
    usb = input('Enter USB (e.g. sdb, sdc,...): ')
    path_to_iso = subprocess.check_output(
        'read -e -p "Enter path to the iso: " path; echo $path',
        shell=True
    ).decode().strip()

    diskutils.write_hybrid_iso_to_usb(usb, path_to_iso)

    time.sleep(30)

    subprocess.run([
        'udisksctl', 'power-off', '-b', f'/dev/{usb}'
    ])

    print(f'Successfully write {path_to_iso} to {usb}!')


if __name__ == '__main__':
    main()
