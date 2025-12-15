#  Controller backlight keyboard for Axioo Pongo 725 linux
A simple and portable control application for the Axioo Pongo 725 laptop running on Linux distributions such as Arch with Wayland (Hyprland), specifically for managing the RGB backlight keyboard feature.

## Prototype Preview
<img width="597" height="476" alt="image" src="https://github.com/user-attachments/assets/2aaad82d-cb48-4e28-9532-dcfaeda583fb" />

## Demo Video
https://youtu.be/VFOXhH-WwCY
<p align="center">
  <a href="https://youtu.be/VFOXhH-WwCY">
    <img src="https://img.youtube.com/vi/VFOXhH-WwCY/maxresdefault.jpg" />
  </a>
</p>

## Installation
### 1. pacman packages :
```
sudo pacman -S --needed python-gobject gtk3
````
### 2. yay package :
```
yay -S --needed clevo-drivers-dkms-git
```
### 3. Clone :
```
git clone --depth 1 https://github.com/kkrdwn/pongo725-backlight.git
```
### 4. Give permission script
Open your clone directory use `cd` and then execute this command for give the script permission:
```
chmod +x ./main.py
```
### 5. Start app use
```
./main.py
```
