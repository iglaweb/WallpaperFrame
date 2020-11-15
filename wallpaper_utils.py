import os
from os.path import isfile
from subprocess import PIPE, Popen
from typing import Optional

import download_utils
import io_prefs
import utils


def find_image_not_visited(image_list=None) -> Optional[str]:
    # iterate through the names of contents of the folder
    if image_list is None:
        image_list = []
    image_folder = download_utils.get_wallpaper_dir()
    for image_name in os.listdir(image_folder):
        image_fullname = os.path.join(image_folder, image_name)
        if utils.is_image(image_fullname):

            im_width, im_height = utils.find_image_size(image_fullname)
            if download_utils.can_use_photo(im_width, im_height):  # check photo file
                photo_hash = utils.sha256sum(image_fullname)
                if photo_hash not in image_list:  # image is not yet used
                    return image_fullname
    return None


def set_wallpaper(file_path: str):
    if isfile(file_path):
        # save photo_hash to prefs
        photo_hash = utils.sha256sum(file_path)
        io_prefs.write_pref_image_visit(photo_hash)

        set_wallpaper_via_as(file_path)
        print('Wallpaper set to ' + file_path)


def set_wallpaper_via_as(path: str):
    """
    Set wallpaper with AppleScript
    """
    app = "Finder"
    set_wallpaper_cmd = '''
        tell application "%(app)s"
          set desktop picture to POSIX file "%(path)s"
        end tell
      ''' % {'app': app, 'path': path}

    proc = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output, error = proc.communicate(set_wallpaper_cmd)
    if error != "":
        print("osascript error: " + error)
