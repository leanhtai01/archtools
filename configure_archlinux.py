from lib.archinstall import ArchInstall

arch_install = ArchInstall('settings.json', live_system=False)

arch_install.execute_method(arch_install.configure_gnome)
arch_install.execute_method(arch_install.make_gnome_shortcuts)
arch_install.execute_method(arch_install.configure_input_method)
arch_install.execute_method(arch_install.enable_gnome_appindicator)
arch_install.execute_method(arch_install.enable_gnome_vitals_extension)
arch_install.execute_method(arch_install.configure_gedit)
arch_install.execute_method(arch_install.install_tmcbeans_from_snap)
arch_install.execute_method(
    arch_install.install_flatpak_packages_from_file,
    'packages_info/arch_linux/flatpak.txt'
)
