# WallpaperFrame

PhotoFramer can download and set image of the day as wallpaper on OS X. The image provider is a local folder on PC or folder from [Yandex Disk](https://disk.yandex.com).


Getting Started
---------
To use Yandex Disk integration, you need to set up [token](https://yandex.ru/dev/direct/doc/dg-v4/examples/auth-token-sample.html/?lang=en) in *.prefs* file and assign YADISK_ENABLE variable to True.
```
yadisk_token=TOKEN
```

or you can use local folder from your PC through modifying this var like:
```
IMAGE_LOCAL_DIR = '/Users/User/Pictures/Point Lobos'
```

When you are ready just make script `run_photoframer.sh` to run on startup. For macOS use `Automator` or `System Preferences → Users and Groups → Login items`.

Issues
------

If you find any problems or would like to suggest a feature, please
feel free to file an [issue](https://github.com/iglaweb/WallpaperFrame/issues)
