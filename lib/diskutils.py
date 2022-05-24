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


def prepare_unencrypted_layout(
    device, esp_size='+550M', boot_size='+550M', swap_size='+20G'
):
    """prepare layout for unencrypted system"""
    wipe_device(device)

    create_partition(device, 'ef00', 'esp', esp_size)
    create_partition(device, 'ea00', 'XBOOTLDR', boot_size)
    create_partition(device, '8200', 'swap', swap_size)
    create_partition(device, '8304', 'root', '0')

    # set partition name based on device's name
    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + '1'
    xbootldr_part_name = partition_prefix + '2'
    swap_part_name = partition_prefix + '3'
    root_part_name = partition_prefix + '4'

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


def prepare_unencrypted_dual_boot_windows_layout():
    """prepare layout for unencrypted dual boot with Windows system"""
    pass
