from lib.archinstall import ArchInstall

arch_install = ArchInstall('settings.json', live_system=False)

arch_install.configure_gnome()
arch_install.make_gnome_shortcuts()
arch_install.configure_ibus_bamboo()
arch_install.enable_gnome_appindicator()
arch_install.enable_gnome_vitals_extension()
arch_install.configure_gedit()
arch_install.install_flatpak_packages_from_file(
    'packages_info/arch_linux/flatpak.txt'
)
