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
from lib.archinstall import ArchInstall

arch_install = ArchInstall('settings.json')

arch_install.execute_method(arch_install.install_base_system)
arch_install.execute_method(arch_install.configure_as_virtualbox_guest)
arch_install.execute_method(arch_install.install_pipewire)
arch_install.execute_method(arch_install.install_gnome_de)
arch_install.execute_method(arch_install.configure_display_manager, 'gdm')
arch_install.execute_method(arch_install.install_fonts)
arch_install.execute_method(arch_install.install_browsers)
arch_install.execute_method(arch_install.install_editors)
