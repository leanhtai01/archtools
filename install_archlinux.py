import time

from lib.archinstall import ArchInstall

arch_install = ArchInstall('settings.json')

arch_install.execute_method(arch_install.connect_to_wifi)
time.sleep(60)
arch_install.execute_method(arch_install.install_base_system)
arch_install.execute_method(arch_install.install_intel_drivers)
arch_install.execute_method(arch_install.install_other_packages)
arch_install.execute_method(arch_install.configure_thermald)
arch_install.execute_method(arch_install.install_pipewire)
arch_install.execute_method(arch_install.install_desktop_environment)
arch_install.execute_method(arch_install.enable_bluetooth_service)
arch_install.execute_method(arch_install.configure_display_manager)
arch_install.execute_method(arch_install.install_fonts)
arch_install.execute_method(arch_install.install_browsers)
arch_install.execute_method(arch_install.install_editors)
arch_install.execute_method(arch_install.install_core_programming)
arch_install.execute_method(arch_install.install_core_tools)
arch_install.execute_method(arch_install.configure_git)
arch_install.execute_method(arch_install.install_kvm)
arch_install.execute_method(arch_install.install_docker)
arch_install.execute_method(arch_install.install_c_cpp_programming)
arch_install.execute_method(arch_install.install_go_programming)
arch_install.execute_method(arch_install.install_java_programming)
arch_install.execute_method(arch_install.install_dotnet_programming)
arch_install.execute_method(arch_install.install_python_programming)
arch_install.execute_method(arch_install.install_javascript_programming)
arch_install.execute_method(arch_install.install_gnome_programming)
arch_install.execute_method(arch_install.install_multimedia)
arch_install.execute_method(arch_install.install_office)
arch_install.execute_method(arch_install.install_games)
arch_install.execute_method(
    arch_install.install_aur_packages_from_file,
    'packages_info/arch_linux/aur.txt'
)
arch_install.execute_method(arch_install.install_snapd)
arch_install.execute_method(arch_install.install_input_method)
arch_install.execute_method(arch_install.install_disc_image_tools)
arch_install.execute_method(arch_install.configure_ufw)
arch_install.execute_method(arch_install.configure_emacs)
