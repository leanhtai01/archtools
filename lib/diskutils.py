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


def get_size_in_byte(partition):
    """get partition's size in byte"""
    output = subprocess.run(
        ['blockdev', '--getsize64', f'/dev/{partition}'],
        capture_output=True
    )

    return int(output.stdout.decode())


def byte_to_mebibyte(byte):
    """convert byte to mebibyte"""
    return byte // (1024 ** 2)


def byte_to_gibibyte(byte):
    """convert byte to gibibyte"""
    return byte // (1024 ** 3)


def resize_ntfs_filesystem(partition, new_size, unit='M'):
    """resize NTFS filesystem"""
    subprocess.run([
        'ntfsresize', '-f', '--size', f'{new_size}{unit}', f'/dev/{partition}'
    ])

    # remove dirty flag, so the filesystem will not be checked on next
    # Windows boot
    subprocess.run(['ntfsfix', '-d', f'/dev/{partition}'])


def prepare_unencrypted_dual_boot_layout(
    device, boot_size='+550M', swap_size='+20G', root_size='+200G'
):
    """prepare layout for unencrypted dual boot with Windows system"""
    esp_partnum = '1'
    msftdata_partnum = '3'
    xbootldr_partnum = '5'
    swap_partnum = '6'
    root_partnum = '7'

    # set partition name based on device's name
    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + esp_partnum
    xbootldr_part_name = partition_prefix + xbootldr_partnum
    msftdata_part_name = partition_prefix + msftdata_partnum
    swap_part_name = partition_prefix + swap_partnum
    root_part_name = partition_prefix + root_partnum

    # calculate and make space for required partitions (the unit is MiB)
    # -1024 here to make sure filesystem not damaged after shrunk
    space_to_shrink = str(
        int(boot_size[1:-1]) +
        int(swap_size[1:-1]) * 1024 +
        int(root_size[1:-1]) * 1024
    )
    msftdata_size = byte_to_mebibyte(get_size_in_byte(msftdata_part_name))
    msftdata_new_fs_size = msftdata_size - int(space_to_shrink) - 1024
    resize_ntfs_filesystem(msftdata_part_name, str(msftdata_new_fs_size))
    shrink_partition(device, msftdata_partnum, space_to_shrink, 'MiB')

    create_partition(device, 'ea00', 'XBOOTLDR', boot_size)
    create_partition(device, '8200', 'swap', swap_size)
    create_partition(device, '8304', 'root', '0')

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


def create_luks_container(partition, password: str):
    """create luks container"""
    subprocess.run([
        'cryptsetup', 'luksFormat', '--type', 'luks2', f'/dev/{partition}', '-'
    ], input=password.encode())


def open_luks_container(partition, luks_mapper_name, password: str):
    """open luks container"""
    subprocess.run([
        'cryptsetup', 'open', f'/dev/{partition}', luks_mapper_name, '-'
    ], input=password.encode())


def prepare_logical_volumes_on_luks(
    luks_mapper_name, vg_name, lv_swap_name, swap_size, lv_root_name
):
    """prepare logical volumes (root, swap)"""
    subprocess.run(['pvcreate', f'/dev/mapper/{luks_mapper_name}'])
    subprocess.run(['vgcreate', vg_name, f'/dev/mapper/{luks_mapper_name}'])
    subprocess.run([
        'lvcreate', '-L', f'{swap_size}G', vg_name, '-n', lv_swap_name
    ])
    subprocess.run([
        'lvcreate', '-l', '+100%FREE', vg_name, '-n', lv_root_name
    ])


def prepare_encrypted_layout(
    device, password, esp_size='+550M', boot_size='+550M', swap_size='+20G'
):
    """prepare layout for encrypted system"""
    esp_partnum = '1'
    xbootldr_partnum = '2'
    luks_encrypted_partnum = '3'

    luks_mapper_name = 'cryptlvm'
    vg_name = 'vg_system'
    lv_swap_name = 'lv_swap'
    lv_root_name = 'lv_root'

    wipe_device(device)

    create_partition(device, 'ef00', 'esp', esp_size)
    create_partition(device, 'ea00', 'XBOOTLDR', boot_size)
    create_partition(device, '8309', 'luks_encrypted', '0')

    # set partition name based on device's name
    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + esp_partnum
    xbootldr_part_name = partition_prefix + xbootldr_partnum
    luks_encrypted_part_name = partition_prefix + luks_encrypted_partnum

    wipe_partition(esp_part_name)
    wipe_partition(xbootldr_part_name)
    wipe_partition(luks_encrypted_part_name)

    # make LUKS container and logical volumes
    create_luks_container(luks_encrypted_part_name, password)
    open_luks_container(luks_encrypted_part_name, luks_mapper_name, password)
    wipe_partition(f'mapper/{luks_mapper_name}')
    prepare_logical_volumes_on_luks(
        luks_mapper_name, vg_name, lv_swap_name, swap_size, lv_root_name
    )

    # format_partitions
    format_fat32(esp_part_name)
    format_fat32(xbootldr_part_name)
    make_swap(f'{vg_name}/{lv_swap_name}')
    format_ext4(f'{vg_name}/{lv_root_name}')

    # mount the filesystems
    mount_partition(f'{vg_name}/{lv_root_name}', '/mnt')  # must be mount first
    pathlib.Path('/mnt/efi').mkdir(exist_ok=True)
    pathlib.Path('/mnt/boot').mkdir(exist_ok=True)
    mount_partition(esp_part_name, '/mnt/efi')
    mount_partition(xbootldr_part_name, '/mnt/boot')

    return {
        'esp_part_name': esp_part_name,
        'xbootldr_part_name': xbootldr_part_name,
        'luks_encrypted_part_name': luks_encrypted_part_name,
        'luks_mapper_name': luks_mapper_name,
        'vg_name': vg_name,
        'lv_swap_name': lv_swap_name,
        'lv_root_name': lv_root_name
    }


def prepare_encrypted_dual_boot_layout(
    device, password, boot_size='+550M', swap_size='+20G', root_size='+200G'
):
    """prepare layout for encrypted dual boot with Windows system"""
    esp_partnum = '1'
    msftdata_partnum = '3'
    xbootldr_partnum = '5'
    luks_encrypted_partnum = '6'

    luks_mapper_name = 'cryptlvm'
    vg_name = 'vg_system'
    lv_swap_name = 'lv_swap'
    lv_root_name = 'lv_root'

    # set partition name based on device's name
    partition_prefix = device + 'p' if device.startswith('nvme') else device
    esp_part_name = partition_prefix + esp_partnum
    xbootldr_part_name = partition_prefix + xbootldr_partnum
    msftdata_part_name = partition_prefix + msftdata_partnum
    luks_encrypted_part_name = partition_prefix + luks_encrypted_partnum

    # calculate and make space for required partitions (the unit is MiB)
    # -1024 here to make sure filesystem not damaged after shrunk
    space_to_shrink = str(
        int(boot_size[1:-1]) +
        int(swap_size[1:-1]) * 1024 +
        int(root_size[1:-1]) * 1024
    )
    msftdata_size = byte_to_mebibyte(get_size_in_byte(msftdata_part_name))
    msftdata_new_fs_size = msftdata_size - int(space_to_shrink) - 1024
    resize_ntfs_filesystem(msftdata_part_name, str(msftdata_new_fs_size))
    shrink_partition(device, msftdata_partnum, space_to_shrink, 'MiB')

    create_partition(device, 'ea00', 'XBOOTLDR', boot_size)
    create_partition(device, '8309', 'luks_encrypted', '0')

    wipe_partition(xbootldr_part_name)
    wipe_partition(luks_encrypted_part_name)

    # make LUKS container and logical volumes
    create_luks_container(luks_encrypted_part_name, password)
    open_luks_container(luks_encrypted_part_name, luks_mapper_name, password)
    wipe_partition(f'mapper/{luks_mapper_name}')
    prepare_logical_volumes_on_luks(
        luks_mapper_name, vg_name, lv_swap_name, swap_size, lv_root_name
    )

    # format_partitions
    format_fat32(xbootldr_part_name)
    make_swap(f'{vg_name}/{lv_swap_name}')
    format_ext4(f'{vg_name}/{lv_root_name}')

    # mount the filesystems
    mount_partition(f'{vg_name}/{lv_root_name}', '/mnt')  # must be mount first
    pathlib.Path('/mnt/efi').mkdir(exist_ok=True)
    pathlib.Path('/mnt/boot').mkdir(exist_ok=True)
    mount_partition(esp_part_name, '/mnt/efi')
    mount_partition(xbootldr_part_name, '/mnt/boot')

    return {
        'esp_part_name': esp_part_name,
        'xbootldr_part_name': xbootldr_part_name,
        'luks_encrypted_part_name': luks_encrypted_part_name,
        'luks_mapper_name': luks_mapper_name,
        'vg_name': vg_name,
        'lv_swap_name': lv_swap_name,
        'lv_root_name': lv_root_name
    }
