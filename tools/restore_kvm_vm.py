# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
import subprocess


def main():
    backup_location = subprocess.check_output(
        'read -e -p "Enter backup location: " path; echo $path',
        shell=True
    ).decode().strip()
    subprocess.run(f'ls -l {backup_location}', shell=True)
    vm_name = input('Enter KVM virtual machine name: ')
    backup_location += vm_name

    # copy disk file
    subprocess.run(
        f'sudo cp {backup_location}/{vm_name}.qcow2 ' +
        '/var/lib/libvirt/images/',
        shell=True
    )

    # define VM's XML
    subprocess.run(
        f'sudo virsh define {backup_location}/{vm_name}.xml',
        shell=True
    )

    # re-define snapshots
    with open(f'{backup_location}/snapshots_structure') as reader:
        snapshot_xmls = reader.read().splitlines()

    for snapshot_xml in snapshot_xmls:
        subprocess.run(
            f'sudo virsh snapshot-create --redefine ' +
            f'{vm_name} {backup_location}/snapshots/{snapshot_xml}',
            shell=True
        )

    print('Restore complete!')


if __name__ == '__main__':
    main()
