#!/usr/bin/env bash

set -e

username=$1
cmd_prefix=$2

${cmd_prefix}mkdir -p /home/$username/.config/pipewire
${cmd_prefix}cp -r /usr/share/pipewire /home/$username/.config/
${cmd_prefix}sed -i '/resample.quality/s/#//; /resample.quality/s/4/15/' \
    /home/$username/.config/pipewire/{client.conf,pipewire-pulse.conf}
