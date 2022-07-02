# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
import subprocess


def main():
    subprocess.run(['sudo', 'virsh', 'list', '--all'])
    vm_name = input('Enter KVM virtual machine name: ')
    backup_location = subprocess.check_output(
        'read -e -p "Enter backup location: " path; echo $path',
        shell=True
    ).decode().strip() + vm_name

    # make directory for VM
    subprocess.run(['mkdir', f'{backup_location}'])

    # copy disk file
    subprocess.run([
        'sudo', 'cp',
        f'/var/lib/libvirt/images/{vm_name}.qcow2',
        f'{backup_location}'
    ])

    # dump vm's xml
    subprocess.run(
        f'sudo virsh dumpxml {vm_name} > ' +
        f'{backup_location}/{vm_name}.xml',
        shell=True
    )

    # dump snapshots
    subprocess.run(
        f'mkdir {backup_location}/snapshots',
        shell=True
    )

    snapshots = subprocess.check_output(
        f'sudo virsh snapshot-list --name --topological {vm_name}', shell=True
    ).decode().strip().splitlines()

    for snapshot in snapshots:
        subprocess.run(
            f'echo "{snapshot}.xml" >> ' +
            f'{backup_location}/snapshots_structure',
            shell=True
        )

        subprocess.run(
            f'sudo virsh snapshot-dumpxml {vm_name} {snapshot} > ' +
            f'{backup_location}/snapshots/{snapshot}.xml',
            shell=True
        )

    # change directory permission
    username = subprocess.check_output('whoami', shell=True).decode().strip()
    subprocess.run(
        f'sudo chown -R {username}:{username} {backup_location}',
        shell=True
    )
    subprocess.run(
        f'chmod 666 {backup_location}/{vm_name}.qcow2', shell=True
    )

    print('Backup complete!')


if __name__ == '__main__':
    main()
