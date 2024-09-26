#!/bin/bash

# Install packages
sudo apt update && sudo apt install -y \
    arandr \
    blueman \
    brightnessctl \
    feh \
    i3 \
    maim \
    playerctl \
    rofi \
    stow \
    xclip \
    xdotool

# Add the current user to the video group to adjust the brightness
sudo usermod -aG video ${USER}

# Fix permissions
find -type d -exec chmod 700 {} \;
find -type f -not -name "install.sh" -exec chmod 600 {} \;
find -type f -path "./.local/bin/*" -exec chmod 700 {} \;

# Deploy files
stow -d .. -t ${HOME} i3wm
