# python_kodi_ambilights

This project aims to re-implement ambilights on LibreElec 11.0 (Kodi 20.2), on a RPi 4. The current version uses three external librairies : 
 - https://github.com/joosteto/ws2812-spi
 - https://github.com/rudihorn/drm-vc4-grabber
 - spidev

## Installation

- copy the folder **python_ambilight** into OS **/storage** folder
- Install drm-vc4-grabber in your **/storage** folder
- Install spidev (https://forum.libreelec.tv/thread/25877-including-spidev-in-python-library/?postID=171295#post171295)
- In **python_ambilight**, add *ws2812.py* from @joosteto's repo.

## How it works

The current and main issue regarding Ambilights and LibreElec newer versions relies on the video pipes used being uncompatible with the most used Ambilight softwares. Using the promising work of @rudihorn, it is possible to use an internal drm-vc4 grabber to compute LEDs values.
My setup is composed of 60 LEDs (WS2812), 8 on each side and 44 on the top, first LED of the strip on the low-left corner.
I did not yet manage to use the socket opened by the drm-vc4-grabber in order to get the images. So, the current (temporary) solution is using the '--screenshot' option when executing the drm grabber binary. This will create a png file of the screenshot. This file is then openend, parsed, resolution lowered to match the LED density.
Then, GRB values are sent to the strip (from ws2812_spi with spidev).
This whole process causes a slight latency and obviously used way too much CPU for what it actually does.  

## Future Improvements

I need to figure a way to connect to drm-vc4-grabber websocket to this script. In future improvement, I also consider a global rework of my code to make it easier to set up.