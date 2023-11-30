from PIL import Image
import struct
import ws2812
import sys
sys.path.insert(0, '/storage/.kodi/addons/script.module.spidev/lib')
import spidev
import time
import subprocess
import os

###Variables Definition
LEDS_SIDE = 8
LEDS_TOP = 44


def process_image_pil(image_path, target_width, target_height):
    # Open the image
    image = Image.open(image_path)

    # Get the top half of the image
    half_height = image.height // 2
    top_half = image.crop((0, 0, image.width, half_height))

    # Resize the image to the target dimensions
    resized_image = top_half.resize((target_width, target_height))

    # Convert the image to a flat list of RGB values
    flat_list = [resized_image.getpixel((j, i)) for i in range(target_height) for j in range(target_width)]

    # Reshape the list into a 3D array
    image_array = [flat_list[i * target_width:(i + 1) * target_width] for i in range(target_height)]

    return image_array

def main():
    screenshot_path = "/storage/python_ambilights/screenshot.png"
    target_width = LEDS_TOP
    target_height = LEDS_SIDE

    processed_image = process_image_pil(screenshot_path, target_width, target_height)
    #print(processed_image)
    return compute_led_values(processed_image)

def compute_led_values(image):
    led_data = []
    for i in range(8):
        led_data.append((image[-i][0][1],image[-i][0][0],image[-i][0][2]))
    for i in range(44):
        led_data.append((image[0][i][1],image[0][i][0],image[0][i][2]))
    for i in range(8):
        led_data.append((image[-i][-1][1],image[-i][-1][0],image[-i][-1][2]))
    return(led_data)

def take_screenshot():
    command = "/storage/drm-vc4-grabber-v0.1.1-aarch64-linux/drm-vc4-grabber --screenshot"
    os.system(command)

def delete_screenshot():
    file_path = 'screenshot.png'

    try:
        os.remove(file_path)
        #print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {e}")



if __name__ == "__main__":
    spi = spidev.SpiDev()
    spi.open(0,0)
    while True:
        take_screenshot()
        time.sleep(0.01)
        led_data = main()
        ws2812.write2812(spi, led_data)
        #delete_screenshot()
        time.sleep(0.1)
        #break
