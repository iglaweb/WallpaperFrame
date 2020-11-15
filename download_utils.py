import os
from os import makedirs
from os.path import isfile
from os.path import join, exists, expanduser

import yadisk
from requests import get

import io_prefs
import utils
import wallpaper_utils

# https://yandex.ru/dev/direct/doc/dg-v4/examples/auth-token-sample.html/
YADISK_APP_USER_TOKEN = io_prefs.read_system_credentials()

YADISK_ENABLE = False  # True if Yandex Disk folder or local
YADISK_IMAGE_FOLDER = '/Pictures/Events/201910_USA'  # remote on yandex disk or local
YADISK_IMAGES_COUNT_DOWNLOAD = 50

APP_USE_ONLY_LANDSCAPE = True
APP_CLEAR_CACHE_CYCLE = True

# Configurations
# Location to save downloaded wallpapers
# Leave the IMAGE_LOCAL_DIR empty to use default directory /Users/USERNAME/Pictures/PhotoFramer
# Or you can set your own custom directory
IMAGE_LOCAL_DIR = '/Users/igla/Downloads/Point Lobos'
IMAGE_DIR_REMOTE_PC = 'Pictures/PhotoFramer'

PERIOD_WALLPAPER_SECONDS = 0
PERIOD_WALLPAPER_MINUTES = 0
PERIOD_WALLPAPER_HOURS = 0
PERIOD_WALLPAPER_DAYS = 1

PERIOD_UPDATE_TOTAL_SEC = PERIOD_WALLPAPER_SECONDS + \
                          PERIOD_WALLPAPER_MINUTES * 60 + \
                          PERIOD_WALLPAPER_HOURS * 3600 + \
                          PERIOD_WALLPAPER_DAYS * 3600 * 24


def get_wallpaper_dir():
    if '' != IMAGE_LOCAL_DIR.strip():
        image_dir = IMAGE_LOCAL_DIR
    else:
        image_dir = join(expanduser("~"), IMAGE_DIR_REMOTE_PC)

    if not exists(image_dir):
        makedirs(image_dir)
    return image_dir


def download_save_img(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)


# Download a image with given URL
def download_image(url, download_only=False):
    file_name = url.split('/')[-1]
    file_path = utils.get_wallpaper_path(file_name)
    if isfile(file_path):
        print('Skipped - ' + file_name + ' exists already.')
    else:
        download_save_img(url, file_path)
        print('Image downloaded --> ' + file_path)
    if not download_only:
        wallpaper_utils.set_wallpaper(file_path)


def fetch_photos() -> list:
    if YADISK_ENABLE:
        return fetch_yadisk_photos()
    else:
        return get_local_photos()


def can_use_photo(image_width: int, image_height: int):
    return True if APP_USE_ONLY_LANDSCAPE is False or \
                   (APP_USE_ONLY_LANDSCAPE is True and int(image_width) > int(image_height)) else False


def get_local_photos() -> list:
    photo_list = []

    for image_name in os.listdir(IMAGE_LOCAL_DIR):
        fullname_src = os.path.join(IMAGE_LOCAL_DIR, image_name)

        if utils.is_image(fullname_src):
            im_width, im_height = utils.find_image_size(fullname_src)

            if can_use_photo(im_width, im_height):
                fullname_dst = os.path.join(IMAGE_LOCAL_DIR, image_name)
                # shutil.copy2(fullname_src, fullname_dst)  # copy image to new dst
                photo_list.append(fullname_dst)
    print('Resolved photos: ' + str(len(photo_list)))
    return photo_list


def fetch_yadisk_photos(images_count=YADISK_IMAGES_COUNT_DOWNLOAD, photo_folder: str = YADISK_IMAGE_FOLDER) -> list:
    y = yadisk.YaDisk(token=YADISK_APP_USER_TOKEN)
    # Проверяет, валиден ли токен
    print(y.check_token())

    # Получает общую информацию о диске
    print(y.get_disk_info())

    # Print files and directories at "/some/path"
    remote_dir = y.listdir(photo_folder)
    photo_list = []

    for file in remote_dir:
        image_url = file['file']
        if image_url is not None:
            print(file)
            # print(image_url)

            size, image_size = utils.get_image_sizes(image_url)
            if image_size is None:
                print('Invalid image. Skip')
                continue
            image_width, image_height = image_size

            if can_use_photo(image_width, image_height):
                image_dir = get_wallpaper_dir()
                file_path = join(image_dir, f'photo_{images_count}.jpg')

                download_save_img(image_url, file_path)

                photo_list.append(file_path)
                images_count = images_count - 1
                if images_count == 0:
                    break
    print('Fetched photos: ' + str(len(photo_list)))
    return photo_list
