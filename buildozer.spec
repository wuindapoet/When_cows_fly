# This .spec config file tells Buildozer an app's requirements for being built.
#
# It largely follows the syntax of an .ini file.
# See the end of the file for more details and warnings about common mistakes.

[app]

# (str) Title of your application
title = When Cows Fly

# (str) Package name
package.name = whencowsfly

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,json,mp3,wav,pyc,json,ttf,gif

# (list) List of inclusions using pattern matching
source.include_patterns = assets/fonts/HeehawRegular.ttf

# (list) Source files to exclude (leave empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (leave empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
# Do not prefix with './'
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow==9.5.0

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/images/characters/logo.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/images/characters/logo.png

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse, landscape-reverse, or all
orientation = landscape

# (list) List of services to declare
# This is currently only relevant to Android services.
# Each service consists of a name (a valid Java class name, with the first letter capitalized)
# followed by a colon, followed by the name of the Python script (.py file) that should be
# launched. This is optionally followed by ":foreground" for foreground services or
# ":foreground:sticky" for sticky foreground services. The default is a background service.
# Bound services are not supported.
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# Kivy version to use
osx.kivy_version = 2.3.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/
# for general documentation.
# Lottie files can be created using various tools, like Adobe After Effect or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
# (See https://python-for-android.readthedocs.io/en/latest/buildoptions.html for all the supported syntaxes and properties)
#android.permissions = android.permission.INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18)

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 36

# (str) Android NDK version to use
#android.ndk = 23b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = /home/user/.buildozer/android/platform/android-sdk

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android SDK
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint =
