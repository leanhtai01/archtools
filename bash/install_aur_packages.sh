#!/usr/bin/env bash

set -e

username=$1
cmd_prefix=$2
password=$3
packages=$4

${cmd_prefix}bash -c "printf \"$password\" | sudo -S -i;
    export HOME=\"/home/$username\";
    yay -Syu --needed --noconfirm $packages"
