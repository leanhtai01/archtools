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

from lib import ioutils


def main():
    path_to_dir = ioutils.inputPath('Enter path to directory: ')
    save_location = ioutils.inputPath('Enter location to save ISO: ')
    volume_name = input('Enter volume name: ')
    file_name = input('Enter the new file name of ISO: ')

    subprocess.run([
        'mkisofs', '-JR', '-V',
        f'{volume_name}',
        '-o', f'{save_location}{file_name}',
        f'{path_to_dir}'
    ])


if __name__ == '__main__':
    main()
