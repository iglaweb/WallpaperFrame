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

**OR**

1. Create a .plist file according to the instructions in the [Apple Dev docs](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html#//apple_ref/doc/uid/10000172i-SW7-BCIEDDBJ).
2. Place in ~/Library/LaunchAgents or ~/Library/LaunchDaemons.
3. Log in (or run manually via launchctl load [filename.plist]). Look at `com.user.loginscript_run_once.plist` to run job once or `com.user.loginscript_every_day.plist` to run it on a daily base.
4. To load script manually, open Up Terminal and type following command:
```
launchctl load ~/Library/LaunchAgents/com.user.loginscript_run_once.plist
```
5. Check that you job put in the launched queue:
```
launchctl list | grep com.user.loginscript
```


Issues
------

If you find any problems or would like to suggest a feature, please
feel free to file an [issue](https://github.com/iglaweb/WallpaperFrame/issues)
