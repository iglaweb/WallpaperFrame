import datetime as dt
import json
import os
from typing import Optional

dir_path = 'tmp/'
PREFS_FILE = f'{dir_path}settings.cfg'
KEY_IMAGE_VISITED_LIST = 'image_visited_list'
KEY_LAST_DATE_UPDATE_WALLPAPER = 'last_date_update_wallpaper'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def create_prefs_dictionary(filename) -> dict:
    prefs_dict = {}
    with open(filename) as file:
        for line in file:
            k, v = line.rstrip().split('=')
            prefs_dict[k] = v
    return prefs_dict


def read_system_credentials():
    prefs = create_prefs_dictionary('.prefs')
    if bool(prefs) is False:
        print('Cannot continue. System credentials are not set up')
        return
    token_prod = prefs['yadisk_token']
    token = token_prod
    return token


def read_prefs() -> Optional[dict]:
    if os.path.exists(PREFS_FILE) is False:
        return {}
    with open(PREFS_FILE, 'r') as fp:
        return json.load(fp)


def write_config(data):
    filename = PREFS_FILE
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(PREFS_FILE, 'w') as fp:
        json.dump(data, fp)


def write_pref_image_visit(photo_hash: str):
    config = read_prefs()
    pref = config.get(KEY_IMAGE_VISITED_LIST)
    if pref is None:
        pref = []
    pref.append(photo_hash)
    config[KEY_IMAGE_VISITED_LIST] = pref
    write_config(config)


def pref_clear_cache():
    config = read_prefs()
    config[KEY_IMAGE_VISITED_LIST] = []
    write_config(config)


def get_date_last_update_wallpaper() -> Optional[dt.datetime]:
    if os.path.exists(PREFS_FILE) is False:
        return None
    config = read_prefs()
    datetime_str = config.get(KEY_LAST_DATE_UPDATE_WALLPAPER)  # not square
    if datetime_str is None:
        return None
    return dt.datetime.strptime(datetime_str, DATE_FORMAT)


def write_date_last_update_wallpaper(datetime_obj: dt.datetime):
    timestring = datetime_obj.strftime(DATE_FORMAT)
    config = read_prefs()
    config[KEY_LAST_DATE_UPDATE_WALLPAPER] = timestring
    write_config(config)


def has_pref_image_visited(photo_hash: str) -> bool:
    if os.path.exists(PREFS_FILE) is False:
        return False
    config = read_prefs()
    image_list = config.get(KEY_IMAGE_VISITED_LIST)  # not square
    if image_list is None:
        return False
    return photo_hash in image_list[photo_hash]


def get_pref_image_visited_list() -> list:
    if os.path.exists(PREFS_FILE) is False:
        return []
    config = read_prefs()
    pref_list = config.get(KEY_IMAGE_VISITED_LIST)  # not square
    if pref_list is None:
        pref_list = []
    return pref_list
