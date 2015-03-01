# stravaupload
Small python script to upload tcs files to strava. It is intended for personal use and has a lot of limitations. Feel free to use it however you like. If you have any comments, questions or want to help, dont hasitate to contact me.

Tips: You can use the script https://github.com/marthinsen/polar2tcx to create tcx files from Polar devices.

## Requirements
You need python with stravalib (https://github.com/hozn/stravalib) installed (pip install stravalib)

## Instructions
1. Create an Strava Application and follow the instructions here: http://strava.github.io/api/v3/oauth/ to get an access token.
2. Rename the file .stravalib.cfg.sample to .stravalib.cfg and enter the access token there.
3. Run the script by ./stravaupload.py

