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
    pulseaudio-utils \
    rofi \
    stow \
    xclip \
    xdotool

# Disable blueman-applet from starting automatically in GNOME
cp /etc/xdg/autostart/blueman.desktop ${HOME}/.config/autostart/
echo "NotShowIn=GNOME;" >> ${HOME}/.config/autostart/blueman.desktop

# Add the current user to the video group to adjust the brightness
sudo usermod -aG video ${USER}

# Fix permissions
find -type d -exec chmod 700 {} \;
find -type f -not -name "install.sh" -exec chmod 600 {} \;
find -type f -path "./.local/bin/*" -exec chmod 700 {} \;

# Deploy files
stow -d .. -t ${HOME} i3wm
