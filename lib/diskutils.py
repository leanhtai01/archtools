# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
import pathlib
import subprocess
import time


def wipe_device(device):
    """wipe everything from (signature, partition, ...)"""
    subprocess.run(['wipefs', '-a', f'/dev/{device}'])
    subprocess.run(['sgdisk', '-Z', f'/dev/{device}'])
    time.sleep(2)


def wipe_partition(partition):
    """wipe everything from partition"""
    subprocess.run(['wipefs', '-a', f'/dev/{partition}'])


def create_partition(device, part_type, gpt_name, part_size):
    """create a partition"""
    subprocess.run([
        'sgdisk',
        '-n', f'0:0:{part_size}',
        '-t', f'0:{part_type}',
        '-c', f'0:{gpt_name}',
        f'/dev/{device}'
    ])


def format_fat32(partition):
    """format a partition to FAT32"""
    subprocess.run(['mkfs.vfat', '-F32', f'/dev/{partition}'])


def format_ntfs(partition):
    """format a partition to NTFS"""
    subprocess.run(['mkfs.ntfs', '-f', f'/dev/{partition}'])


def format_ext4(partition):
    """format a partition to ext4"""
    subprocess.run(['mkfs.ext4', f'/dev/{partition}'])


def set_partition_flag_state(device, partnum, flag, state):
    """change the state of the flag on partition using parted"""
    subprocess.run([
        'parted', f'/dev/{device}', 'set', f'{partnum}', f'{flag}', f'{state}'
    ])


def make_swap(partition):
    """make swap partition"""
    subprocess.run(['mkswap', f'/dev/{partition}'])
    subprocess.run(['swapon', f'/dev/{partition}'])


def mount_partition(partition, mount_point):
    """mount a partition to specific mount point"""
    subprocess.run(['mount', f'/dev/{partition}', mount_point])


def shrink_partition(device, partnum, space_to_shrink, unit='GiB'):
    """shrink partition using parted"""
    info = f'{partnum}\n-{space_to_shrink}{unit}\nYes\n'
    subprocess.run([
        'parted', f'/dev/{device}', 'resizepart', '---pretend-input-tty'
    ], input=info.encode())


def make_partitions_for_windows(device):
    """make partition for Windows"""
    esp_partnum = '1'
    msftres_partnum = '2'
    msftdata_partnum = '3'
    winre_partnum = '4'

    wipe_device(device)

    create_partition(device, 'ef00', 'EFI system partition', '+100M')
    create_partition(device, '0c01', 'Microsoft reserved partition', '+16M')
    create_partition(device, '0700', 'Basic data partition', '0')
    shrink_partition(device, msftdata_partnum, '509', 'MiB')
    create_partition(device, '2700', '', '0')

    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + esp_partnum
    msftres_part_name = partition_prefix + msftres_partnum
    msftdata_part_name = partition_prefix + msftdata_partnum
    winre_part_name = partition_prefix + winre_partnum

    wipe_partition(esp_part_name)
    wipe_partition(msftres_part_name)
    wipe_partition(msftdata_part_name)
    wipe_partition(winre_part_name)

    format_fat32(esp_part_name)
    format_ntfs(msftdata_part_name)
    format_ntfs(winre_part_name)
    set_partition_flag_state(device, winre_partnum, 'hidden', 'on')


def prepare_unencrypted_layout(
    device, esp_size='+550M', boot_size='+550M', swap_size='+20G'
):
    """prepare layout for unencrypted system"""
    esp_partnum = '1'
    xbootldr_partnum = '2'
    swap_partnum = '3'
    root_partnum = '4'

    wipe_device(device)

    create_partition(device, 'ef00', 'esp', esp_size)
    create_partition(device, 'ea00', 'XBOOTLDR', boot_size)
    create_partition(device, '8200', 'swap', swap_size)
    create_partition(device, '8304', 'root', '0')

    # set partition name based on device's name
    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + esp_partnum
    xbootldr_part_name = partition_prefix + xbootldr_partnum
    swap_part_name = partition_prefix + swap_partnum
    root_part_name = partition_prefix + root_partnum

    wipe_partition(esp_part_name)
    wipe_partition(xbootldr_part_name)
    wipe_partition(swap_part_name)
    wipe_partition(root_part_name)

    format_fat32(esp_part_name)
    format_fat32(xbootldr_part_name)
    make_swap(swap_part_name)
    format_ext4(root_part_name)

    # mount the filesystem
    mount_partition(root_part_name, '/mnt')  # must be mount first
    pathlib.Path('/mnt/efi').mkdir(exist_ok=True)
    pathlib.Path('/mnt/boot').mkdir(exist_ok=True)
    mount_partition(esp_part_name, '/mnt/efi')
    mount_partition(xbootldr_part_name, '/mnt/boot')

    return {
        'esp_part_name': esp_part_name,
        'xbootldr_part_name': xbootldr_part_name,
        'swap_part_name': swap_part_name,
        'root_part_name': root_part_name
    }


def prepare_unencrypted_dual_boot_layout(
    device, boot_size='+550M', swap_size='+20G', root_size='+200G'
):
    """prepare layout for unencrypted dual boot with Windows system"""
    esp_partnum = '1'
    msftdata_partnum = '3'
    xbootldr_partnum = '5'
    swap_partnum = '6'
    root_partnum = '7'

    # calculate and make space for required partitions
    space_to_shrink = str(
        int(boot_size[1:-1]) +
        int(swap_size[1:-1]) * 1024 +
        int(root_size[1:-1]) * 1024
    )
    shrink_partition(device, msftdata_partnum, space_to_shrink, 'MiB')

    create_partition(device, 'ea00', 'XBOOTLDR', boot_size)
    create_partition(device, '8200', 'swap', swap_size)
    create_partition(device, '8304', 'root', '0')

    # set partition name based on device's name
    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + esp_partnum
    xbootldr_part_name = partition_prefix + xbootldr_partnum
    swap_part_name = partition_prefix + swap_partnum
    root_part_name = partition_prefix + root_partnum

    wipe_partition(xbootldr_part_name)
    wipe_partition(swap_part_name)
    wipe_partition(root_part_name)

    format_fat32(xbootldr_part_name)
    make_swap(swap_part_name)
    format_ext4(root_part_name)

    mount_partition(root_part_name, '/mnt')  # must be mount first
    pathlib.Path('/mnt/efi').mkdir(exist_ok=True)
    pathlib.Path('/mnt/boot').mkdir(exist_ok=True)
    mount_partition(esp_part_name, '/mnt/efi')
    mount_partition(xbootldr_part_name, '/mnt/boot')

    return {
        'esp_part_name': esp_part_name,
        'xbootldr_part_name': xbootldr_part_name,
        'swap_part_name': swap_part_name,
        'root_part_name': root_part_name
    }
