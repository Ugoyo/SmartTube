#!/bin/bash
set -x
OUT=.github/screenshot/out
mkdir -p $OUT
PKG=org.smarttube.beta
APK=$(ls smarttubetv/build/outputs/apk/stbeta/debug/*universal*.apk 2>/dev/null | head -1)
[ -z "$APK" ] && APK=$(ls smarttubetv/build/outputs/apk/stbeta/debug/*x86*.apk | grep -v x86_64 | head -1)
echo "APK: $APK"
adb install -r -g "$APK"
shot() { adb exec-out screencap -p > "$OUT/$1.png"; }

# Start the app normally first (app init), then open the picker
adb shell monkey -p $PKG -c android.intent.category.LEANBACK_LAUNCHER 1
sleep 25
shot 0_after_launch
adb shell am start -n $PKG/com.liskovsoft.smartyoutubetv2.tv.ui.accountselection.AccountSelectionActivity
sleep 12
shot 1_account_focused
adb shell input keyevent KEYCODE_DPAD_RIGHT
adb shell input keyevent KEYCODE_DPAD_RIGHT
sleep 2
shot 2_add_account_focused
adb shell input keyevent KEYCODE_DPAD_DOWN
sleep 2
shot 3_signed_out_focused
adb logcat -d -t 400 > $OUT/logcat.txt || true
ls -la $OUT
