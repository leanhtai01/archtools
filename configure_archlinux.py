from lib.archinstall import ArchInstall

arch_install = ArchInstall('settings.json', live_system=False)

arch_install.execute_method(arch_install.configure_gnome)
arch_install.execute_method(arch_install.make_gnome_shortcuts)
arch_install.execute_method(arch_install.configure_input_method)
arch_install.execute_method(arch_install.configure_gedit)
