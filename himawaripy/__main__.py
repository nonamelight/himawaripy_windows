#!/usr/bin/env python3

import argparse
import sys
import threading
import appdirs

from himawaripy.core import thread_main, HIMAWARIPY_VERSION, is_discharging
from himawaripy.controller import run_tray_mode

def parse_args():
    parser = argparse.ArgumentParser(
        description="set (near-realtime) picture of Earth as your desktop background",
        epilog="https://github.com/nonamelight/himawaripy_windows#",
    )

    parser.add_argument("--version", action="version", version="%(prog)s {}.{}.{}".format(*HIMAWARIPY_VERSION))

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--auto-offset", action="store_true", dest="auto_offset", default=False, help="determine offset automatically"
    )
    group.add_argument(
        "-o",
        "--offset",
        type=int,
        dest="offset",
        default=10,
        help="UTC time offset in hours, must be less than or equal to +10",
    )

    parser.add_argument(
        "-l",
        "--level",
        type=int,
        choices=[4, 8, 16, 20],
        dest="level",
        default=4,
        help="increases the quality (and the size) of each tile. possible values are 4, 8, 16, 20",
    )
    parser.add_argument(
        "-d",
        "--deadline",
        type=int,
        dest="deadline",
        default=6,
        help="deadline in minutes to download all the tiles, set 0 to cancel",
    )
    parser.add_argument(
        "--save-battery", action="store_true", dest="save_battery", default=False, help="stop refreshing on battery"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        dest="output_dir",
        help="directory to save the temporary background image",
        default=appdirs.user_cache_dir(appname="himawaripy", appauthor=False),
    )
    parser.add_argument(
        "--dont-change",
        action="store_true",
        dest="dont_change",
        default=False,
        help="don't change the wallpaper (just download it)",
    )

    args = parser.parse_args()

    if not -12 <= args.offset <= 10:
        sys.exit("OFFSET has to be between -12 and +10!\n")

    if not args.deadline >= 0:
        sys.exit("DEADLINE has to be greater than (or equal to if you want to disable) zero!\n")

    return args

def main():
    if len(sys.argv) == 1 and sys.platform == "win32":
        sys.argv = [sys.argv[0], "--auto-offset"]
        args = parse_args()
        run_tray_mode(args)
        return

    args = parse_args()

    print("himawaripy {}.{}.{}".format(*HIMAWARIPY_VERSION))

    if args.save_battery and is_discharging():
        sys.exit("Discharging!\n")

    main_thread = threading.Thread(target=thread_main, args=(args,), name="himawaripy-main-thread", daemon=True)
    main_thread.start()
    main_thread.join(args.deadline * 60 if args.deadline else None)

    if args.deadline and main_thread.is_alive():
        sys.exit("Timeout!\n")

    print()
    sys.exit(0)

if __name__ == "__main__":
    main()
