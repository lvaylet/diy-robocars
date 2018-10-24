#!/usr/bin/env python3
# coding: utf-8

"""
This module is responsible for taking photos to the SD card. It also creates
symlinks to the photos to be transferred to the FTP.
"""

import logging
import os
import time
from datetime import datetime
import picamera


# region Helpers

def wait_next_period(delay):
    t = time.time()
    delta = delay - (t % delay)
    time.sleep(delta)
    return t + delta


# endregion

# Configure logging
# TODO Centralize and share logging configuration across all services. Use a config file in a git submodule?
# TODO Log INFO to console and DEBUG to local rotating file for historical debugging.
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# Pull configuration from environment variables, falling back to default values if they are not defined.
TIMELAPSE_DELAY = int(os.getenv('APP_TIMELAPSE_DELAY', '60'))
TIMELAPSE_FORWARD = int(os.getenv('APP_TIMELAPSE_FORWARD', '900'))
DATA_DIR = os.getenv('DATA_DIR', '/sd/data')
PENDING_DIR = os.path.join(DATA_DIR, 'pending')
MEDUSA_ID_FILE = os.path.join(DATA_DIR, 'medusa_id')

medusa_id = 0
while medusa_id == 0:
    try:
        with open(MEDUSA_ID_FILE, 'r') as input_file:
            medusa_id = int(input_file.read())
    except (IOError, FileNotFoundError):
        logging.error('Could not read [%s]. Unable to get medusa ID. Retrying in 60 seconds...', MEDUSA_ID_FILE)
        time.sleep(60)

preview = False
r = (1080, 972)
q = 50
c0 = picamera.PiCamera(0)
c1 = picamera.PiCamera(1)
c0.resolution = r
c1.resolution = r
c0.hflip = True
c1.hflip = True
c0.vflip = True
c1.vflip = True

if preview:
    c0.start_preview(fullscreen=False, window=(0, 0, 800, 1200))
    c1.start_preview(fullscreen=False, window=(800, 0, 800, 1200))

# TM asked CM not to add seconds, because capture continuous on the two cams can cause >1 sec delay which in turn causes
# filename inconsistency
# template = '%d-{timestamp:%%Y%%m%%d-%%H%%M%%S}-cam%d.jpg'
template = '%d-{timestamp:%%Y%%m%%d-%%H%%M00}-cam%d.jpg'
f0_template = template % (medusa_id, 0)
f1_template = template % (medusa_id, 1)

logging.info('Timelapse started')
time_is_now = wait_next_period(TIMELAPSE_DELAY)
day_dir = os.path.join(DATA_DIR, datetime.utcfromtimestamp(time_is_now).strftime('%Y%m%d'))
os.makedirs(day_dir, exist_ok=True)
os.chdir(day_dir)
for (f0, f1) in zip(c0.capture_continuous(f0_template, quality=q), c1.capture_continuous(f1_template, quality=q)):
    logging.debug('Cam snapshots')
    # Create symlinks every TIMELAPSE_FORWARD seconds (900 seconds by default, i.e. 15 mins)
    if time_is_now % TIMELAPSE_FORWARD == 0:
        os.symlink(os.path.join(day_dir, f0), os.path.join(PENDING_DIR, f0))
        os.symlink(os.path.join(day_dir, f1), os.path.join(PENDING_DIR, f1))
    time_is_now = wait_next_period(TIMELAPSE_DELAY)
    day_dir = os.path.join(DATA_DIR, datetime.utcfromtimestamp(time_is_now).strftime('%Y%m%d'))
    os.makedirs(day_dir, exist_ok=True)
    os.chdir(day_dir)

if preview:
    c0.stop_preview()
    c1.stop_preview()
