# i3wm

[i3wm](https://i3wm.org) installation and configuration.

## Install

Open a terminal and run the following command:

```
chmod 700 install.sh && ./install.sh
```

## Configure

## Screen

Use `arandr` to create screen layouts based on the connected screens with the following names:

- Laptop: `~/.screenlayout/laptop.sh`
- Monitor: `~/.screenlayout/monitor.sh`

## Background

During i3wm startup, the file `~/.background.image` is loaded as the background image.

To use your own background image, you can either replace `~/.background.image` with your desired image or create a symbolic link pointing to it.

For example:

```
ln -s bob-sponge.jpg ~/.background.image
```
