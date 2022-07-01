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


def main():
    path_to_iso = subprocess.check_output(
        'read -e -p "Enter path to the iso: " path; echo $path',
        shell=True
    ).decode().strip()

    # get the iso information
    file_name = os.path.splitext(path_to_iso)[0] + '_modified.iso'
    volume_name = subprocess.check_output(
        f'iso-info {path_to_iso} | ' +
        "grep -i '^Volume[ ]*:' | " +
        "cut -d':' -f2 | " +
        "sed 's/^ //g'",
        shell=True
    ).decode().strip()

    # mount the iso
    subprocess.run([
        'sudo', 'mount', f'{path_to_iso}', '/mnt', '-o', 'loop'
    ])

    # create dir for modifications
    subprocess.run([
        'mkdir', '-p', '/tmp/modified/sources'
    ])

    # let user choose version of Windows on install
    with open('/tmp/modified/sources/ei.cfg', 'w') as writer:
        writer.write('[Channel]\r\nRetail\r\n')

    # create custom iso (need cdrtools)
    subprocess.run(
        'mkisofs ' +
        '-iso-level 4 ' +
        '-l ' +
        '-R ' +
        '-UDF ' +
        '-D ' +
        '-b boot/etfsboot.com ' +
        '-no-emul-boot ' +
        '-boot-load-size 8 ' +
        '-hide boot.catalog ' +
        '-eltorito-alt-boot ' +
        '-eltorito-platform efi ' +
        '-no-emul-boot ' +
        '-b efi/microsoft/boot/efisys.bin ' +
        f'-V {volume_name} ' +
        f'-o {file_name} ' +
        '/mnt ' +
        '/tmp/modified',
        shell=True
    )

    subprocess.run([
        'sudo', 'umount', '/mnt'
    ])

    print('Successfully making custom Windows iso!\n')


if __name__ == '__main__':
    main()
