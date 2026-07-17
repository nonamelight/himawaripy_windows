import os
import sys
import time
import json
import urllib.request
import ssl
import multiprocessing as mp
import multiprocessing.dummy as mp_dummy
import itertools as it
from glob import iglob
from datetime import timedelta, datetime
from time import strptime, strftime, mktime
import io

from PIL import Image
from dateutil.tz import tzlocal

from himawaripy.utils import set_background, get_desktop_environment
from himawaripy.config import load_config

# Semantic Versioning: Major, Minor, Patch
HIMAWARIPY_VERSION = (2, 2, 0)
counter = None
HEIGHT = 550
WIDTH = 550

def is_discharging():
    if sys.platform.startswith("linux"):
        from glob import glob
        if len(glob("/sys/class/power_supply/BAT*")) > 1:
            print("Multiple batteries detected, using BAT0.")
        with open("/sys/class/power_supply/BAT0/status") as f:
            status = f.readline().strip()
            return status == "Discharging"
    elif sys.platform == "darwin":
        import subprocess
        return b"discharging" in subprocess.check_output(["pmset", "-g", "batt"])
    else:
        sys.exit("Battery saving feature works only on linux or mac!\n")

def calculate_time_offset(latest_date, auto, preferred_offset):
    if auto:
        preferred_offset = int(datetime.now(tzlocal()).strftime("%z")[0:3])
        print("Detected offset: UTC{:+03d}:00".format(preferred_offset))
        if 11 >= preferred_offset > 10:
            preferred_offset = 10
            print("Offset is greater than +10, +10 will be used...")
        elif 12 >= preferred_offset > 11:
            preferred_offset = -12
            print("Offset is greater than +10, -12 will be used...")

    himawari_offset = 10  # UTC+10:00 is the time zone that himawari is over
    offset = int(preferred_offset - himawari_offset)
    offset_tmp = datetime.fromtimestamp(mktime(latest_date)) + timedelta(hours=offset)
    return offset_tmp.timetuple()

def download(url):
    exception = None
    for i in range(1, 4):  # retry max 3 times
        try:
            with urllib.request.urlopen(url, context=ssl.SSLContext(ssl.PROTOCOL_TLS)) as response:
                return response.read()
        except Exception as e:
            exception = e
            print("[{}/3] Retrying to download '{}'...".format(i, url))
            time.sleep(1)
            pass
    if exception:
        raise exception
    else:
        sys.exit("Could not download '{}'!\n".format(url))

def download_chunk(args):
    global counter
    x, y, latest, level = args
    url_format = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/{}d/{}/{}_{}_{}.png"
    url = url_format.format(level, WIDTH, strftime("%Y/%m/%d/%H%M%S", latest), x, y)

    tiledata = download(url)

    # If the tile data is 2867 bytes, it is a blank "No Image" tile.
    if tiledata.__sizeof__() == 2867:
        sys.exit("No image available for {}.".format(strftime("%Y/%m/%d %H:%M:%S", latest)))

    with counter.get_lock():
        counter.value += 1
        if counter.value == level * level:
            print("Downloading tiles: completed.")
        else:
            print("Downloading tiles: {}/{} completed...".format(counter.value, level * level))
    return x, y, tiledata

def thread_main(args, custom_config=None):
    global counter
    counter = mp.Value("i", 0)

    level = args.level
    
    if custom_config is None:
        config = load_config()
    else:
        config = custom_config
        
    history_offset_minutes = config.get("history_offset", 0)

    print("Updating...")
    latest_json = download("https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json")
    latest = strptime(json.loads(latest_json.decode("utf-8"))["date"], "%Y-%m-%d %H:%M:%S")

    print("Latest version: {} GMT.".format(strftime("%Y/%m/%d %H:%M:%S", latest)))
    requested_time = calculate_time_offset(latest, args.auto_offset, args.offset)
    
    if history_offset_minutes > 0:
        requested_time_dt = datetime.fromtimestamp(mktime(requested_time))
        requested_time_dt -= timedelta(minutes=history_offset_minutes)
        rounded_minute = (requested_time_dt.minute // 10) * 10
        requested_time_dt = requested_time_dt.replace(minute=rounded_minute, second=0, microsecond=0)
        requested_time = requested_time_dt.timetuple()
        
    if args.auto_offset or args.offset != 10 or history_offset_minutes > 0:
        print("Target version: {} GMT.".format(strftime("%Y/%m/%d %H:%M:%S", requested_time)))

    png = Image.new("RGB", (WIDTH * level, HEIGHT * level))

    p = mp_dummy.Pool(level * level)
    print("Downloading tiles...")
    res = p.map(download_chunk, it.product(range(level), range(level), (requested_time,), (args.level,)))

    for (x, y, tiledata) in res:
        tile = Image.open(io.BytesIO(tiledata))
        png.paste(tile, (WIDTH * x, HEIGHT * y, WIDTH * (x + 1), HEIGHT * (y + 1)))

    if sys.platform == "win32":
        try:
            import ctypes
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            
            scale_pct = config.get("scale", 100)
            earth_size = int(screen_height * (scale_pct / 100.0))
            
            if hasattr(Image, "Resampling"):
                resample_filter = Image.Resampling.LANCZOS
            else:
                resample_filter = Image.ANTIALIAS
                
            png = png.resize((earth_size, earth_size), resample_filter)
            
            bg = Image.new("RGB", (screen_width, screen_height), color=(0, 0, 0))
            x_offset = (screen_width - earth_size) // 2
            y_offset = (screen_height - earth_size) // 2
            bg.paste(png, (x_offset, y_offset))
            png = bg
        except Exception as e:
            print("Error resizing image for Windows:", e)

    for file in iglob(os.path.join(args.output_dir, "himawari-*.png")):
        os.remove(file)

    output_file = os.path.join(args.output_dir, strftime("himawari-%Y%m%dT%H%M%S.png", requested_time))
    print("Saving to '%s'..." % (output_file,))
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    png.save(output_file, "PNG")

    if not args.dont_change:
        r = set_background(output_file)
        if not r:
            sys.exit("Your desktop environment '{}' is not supported!\n".format(get_desktop_environment()))
    else:
        print("Not changing your wallpaper as requested.")
