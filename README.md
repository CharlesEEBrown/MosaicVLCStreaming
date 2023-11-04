# JSON format
The content was derived from the vlan wiki.
https://wiki.videolan.org/VLC_HowTo/Make_a_mosaic/
https://wiki.videolan.org/Documentation:Modules/mosaic/
https://docs.videolan.me/vlc-user/3.0/en/advanced/vlm/vlm_mosaic.html

Use the mosaic-vlc-settings-windows-tmp.json or mosaic-vlc-settings-linux-tmp.json file 
by renaming the file to mosaic-vlc-settings.json.

{"mosaic": {
  "pixels-horizontal": "1280",
  "pixels-vertical": "720",
  "videoCodec": "mp4v",
  "audioCodec": mp4v",
  "fps": "12/1",
  "delay": "600",
  "vlc-location": "C:\\Program Files\\VideoLAN\\VLC",
  "ipcitem": [
        {"protocol": "", "url": "", "username": "", "password" : ""},
    ]
},
"app": {
  "debug":"False"
}}

## Prerequisites
VLC needs to be installed. Tested on 3.0.x versions
Requires an operating system with a GUI. Can be executed on Linux(Tested on GNOME) or Windows OS


### FYI
1. Having the delay set to 0 seconds will causes flickering.
2. Having the fps set to anything higher than 18 will cause a delay
3. Sometime executing the app in Linux causes green screen effect. Still troubleshooting.