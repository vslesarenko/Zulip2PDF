from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import hashlib
import os
import shutil
import re
from PIL import Image


def hash_file(filepath):
    '''Just create hash for comparison'''
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_files(file1, file2):
    """Compare two files by their hash values."""
    return hash_file(file1) == hash_file(file2)

def create_or_clean_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


def merge_pngs_to_pdf(png_files, output_pdf):
    # Open the first image and convert it to RGB (as PDF does not support RGBA)
    images = [Image.open(file).convert('RGB') for file in png_files]
    # Save all images into one PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])


scroll_pause_time = 3 #Time (sec) to wait after scrolling before screenshot
request_pause_time = 2 #Time (sec) to wait after request of new channel

max_scroll_clicks=100 #Just a failsafe in case if autodetection for the file
channel_list=["dm/187-Angelika-Gedsun", "stream/101-MetaLab.3AAuto3DPrinter"]

# Set up Firefox WebDriver
driver = webdriver.Firefox()

for key, channel in enumerate(channel_list):
    screen_count = 0
    driver.get(f"https://zulip.vm.uni-freiburg.de/#narrow/{channel}")
    channel_short_name, channel_alternative_name=channel.split("-",1)
    channel_short_name=channel_short_name.replace("/", "-")
    channel_alternative_name=re.sub(r'["\/:*?"<>|]', '_', channel_alternative_name)
    if key==0:
        print ("Waiting 15 seconds for log in! Don't forget to close all pop-ups (green) after log in! Also the first  should be scrolled all the way down")
        time.sleep(15)
        print ("We are starting")
    print (f"Working with the channel {channel}")
    try:
        create_or_clean_folder(f"RAW/{channel_alternative_name}")
    except:
        print ("Warning! Perhaps you need to close all image files and folders in explorer before running again. But we still try to run")

    time.sleep(request_pause_time)

    fname_list = []
    while (screen_count<=max_scroll_clicks):
        fname=f"RAW/{channel_alternative_name}/zulip_screen_100{screen_count}.png"
        driver.save_screenshot(fname)
        print ("Saved "+str(screen_count)+"   "+str(fname))

        # Scroll down
        if screen_count==0:
            main_div=driver.find_element("tag name", "body")
        main_div.send_keys(Keys.PAGE_UP)
        time.sleep(scroll_pause_time)

        # Check if reach the top
        if screen_count>0:
            fname_prev=f"RAW/{channel_alternative_name}/zulip_screen_100{screen_count-1}.png"
            if compare_files(fname, fname_prev):
                os.remove(fname)
                break
        fname_list.append(fname)
        screen_count += 1

    #Now saving to pdf
    fname_list=sorted(fname_list, reverse=True)
    output_pdf = f"RAW/{channel_alternative_name}.pdf"
    merge_pngs_to_pdf(fname_list, output_pdf)
    print(f"PDF saved as RAW/{output_pdf}")


print ("DONE!")
driver.quit()