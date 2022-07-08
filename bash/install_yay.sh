#!/usr/bin/env bash

set -e

username=$1
cmd_prefix=$2
password=$3

${cmd_prefix}mkdir /home/$username/tmp
${cmd_prefix}curl -LJo /home/$username/tmp/yay.tar.gz \
    https://aur.archlinux.org/cgit/aur.git/snapshot/yay.tar.gz
${cmd_prefix}tar -xvf /home/$username/tmp/yay.tar.gz -C /home/$username/tmp
printf "$password" | ${cmd_prefix}bash -c "sudo -S -i;
    export GOCACHE="/home/$username/.cache/go-build";
    cd /home/$username/tmp/yay;
    makepkg -sri --noconfirm"
