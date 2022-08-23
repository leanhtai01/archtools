#!/usr/bin/env bash

set -e

username=$1
cmd_prefix=$2

${cmd_prefix}mkdir -p /home/$username/.config/environment.d
${cmd_prefix}printf \
             "GTK_IM_MODULE=fcitx\nQT_IM_MODULE=fcitx\nXMODIFIERS=@im=fcitx\n" \
             >> /home/$username/.config/environment.d/fcitx5.conf
