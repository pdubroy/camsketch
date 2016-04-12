#!/bin/bash

set -e

echo; cd $(dirname "${BASH_SOURCE[0]}")

echo -n "camsketch: installing our plugin into CamTwist's Effects directory..."
mkdir ~/Library/Application\ Support/CamTwist 2> /dev/null || true
mkdir ~/Library/Application\ Support/CamTwist/Effects 2> /dev/null || true
cp ../src/camsketch-overlay.qtz ~/Library/Application\ Support/CamTwist/Effects && echo "done."

echo -n "camsketch: installing a CamTwist saved setup..."
mkdir ~/Library/Application\ Support/CamTwist/Saved\ Setups/ 2> /dev/null || true
cp ../CamTwist-config.xml ~/Library/Application\ Support/CamTwist/Saved\ Setups/camsketch && echo "done."

echo -n "camsketch: modifying CamTwist settings to autoload camsketch setup..."
defaults write com.allocinit.CamTwist autoload camsketch && echo "done."

echo -n "camsketch: setting CamTwist video size..."
defaults write com.allocinit.CamTwist usingCustomVideoSize 1
if system_profiler SPCameraDataType 2> /dev/null | grep "FaceTime HD" > /dev/null; then
  defaults write com.allocinit.CamTwist videoSize "\"{1280, 720}\"" && echo "using 1280x720."
else
  defaults write com.allocinit.CamTwist videoSize "\"{640, 480}\"" && echo "No HD camera found! Using 640x480."
fi

echo "camsketch: installation complete! You may now close the terminal window."; echo
