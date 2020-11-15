import sys

import utils


# Display help message
def print_help_message():
    msg = '''
PhotoFramer for Mac version 1.0
By Igor Lashkov  https://igla.su

PhotoFramer can batch download and set image of the day as wallpaper on OS X.

Usage: 
python main.py [option]

no argument         download today's picture of the day and set it as wallpaper
-h or --help        display this help message
    '''
    print(msg)
    sys.exit()


def execute():
    if len(sys.argv) < 2:
        utils.run_app_update_wallpaper()
    elif len(sys.argv) == 2:
        if '-h' == sys.argv[1] or '--help' == sys.argv[1]:
            print_help_message()
        else:
            print('Invalid argument!')
            print_help_message()


if __name__ == '__main__':
    execute()
