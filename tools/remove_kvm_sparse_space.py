# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
import subprocess


def main():
    subprocess.run(['sudo', 'virsh', 'list', '--all'])
    vm_name = input('Enter KVM virtual machine name: ')

    subprocess.run(
        'sudo qemu-img convert -O qcow2 ' +
        f'/var/lib/libvirt/images/{vm_name}.qcow2 ' +
        f'/var/lib/libvirt/images/{vm_name}.qcow2.new',
        shell=True
    )

    subprocess.run(
        f'sudo rm /var/lib/libvirt/images/{vm_name}.qcow2',
        shell=True
    )

    subprocess.run(
        f'sudo mv /var/lib/libvirt/images/{vm_name}.qcow2.new ' +
        f'/var/lib/libvirt/images/{vm_name}.qcow2',
        shell=True
    )

    print('Sparse space removed successfully!')


if __name__ == '__main__':
    main()
