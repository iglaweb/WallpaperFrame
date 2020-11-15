import datetime as dt
import hashlib
import imghdr
from os.path import join
from urllib import request as ulreq

from PIL import ImageFile, Image, ImageOps

import download_utils
import io_prefs
import wallpaper_utils


def should_update_wallpaper() -> bool:
    last_date_update = io_prefs.get_date_last_update_wallpaper()
    date_now = dt.datetime.now()
    if last_date_update is None:  # first update
        io_prefs.write_date_last_update_wallpaper(date_now)
        return True
    else:
        # check date
        sec_diff = (date_now - last_date_update).total_seconds()
        period_time_sec = download_utils.PERIOD_UPDATE_TOTAL_SEC
        if sec_diff >= period_time_sec:
            # update last date
            io_prefs.write_date_last_update_wallpaper(date_now)
            return True
        return False


def find_image_size(filename):
    # Read original image, show width and height
    pil = Image.open(filename).convert('RGB')
    w, h = pil.size
    print("Origin: width: {}, height: {}".format(w, h))

    # Transpose with respect to EXIF data
    pil = ImageOps.exif_transpose(pil)
    w, h = pil.size
    print("Target: width: {}, height: {}".format(w, h))

    return w, h


def get_image_sizes(uri):
    # get file size *and* image size (None if not known)
    file = ulreq.urlopen(uri)
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    try:
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
    finally:
        file.close()
    return size, None


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def is_image(next_image):
    image_type = imghdr.what(next_image)
    if not image_type:
        return False
    return True


def get_wallpaper_path(file_name):
    image_dir = download_utils.get_wallpaper_dir()
    file_path = join(image_dir, file_name)
    return file_path


def run_app_update_wallpaper():
    need_update_wallpaper = should_update_wallpaper()
    if need_update_wallpaper is False:
        print('Update wallpaper date is not expired.')
        return

    photo_files = download_utils.fetch_photos()
    print(photo_files)

    image_pref_list = io_prefs.get_pref_image_visited_list()
    if len(image_pref_list) == 0:
        print('No visited wallpapers yet. Start from scratch')

    next_image = wallpaper_utils.find_image_not_visited(image_pref_list)
    if next_image is not None:
        wallpaper_utils.set_wallpaper(next_image)
    else:
        print("All wallpapers used.")
        if download_utils.APP_CLEAR_CACHE_CYCLE is True:
            print("Clear cache")
            io_prefs.pref_clear_cache()

            next_image = wallpaper_utils.find_image_not_visited()
            if next_image is not None:
                wallpaper_utils.set_wallpaper(next_image)
            else:
                print("No suitable wallpapers found")
