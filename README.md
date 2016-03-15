# stravaupload
Small Python script to upload FIT, TCX and GPX (and .fit.gz, .tcx.gz, .gpx.gz) files to Strava. It is intended for personal use and has a lot of limitations. Feel free to use it however you like. If you have any comments, questions or want to help, dont hesitate to contact me.

Tips: You can use the [polar2tcx script](https://github.com/marthinsen/polar2tcx) to create TCX files from Polar devices.

## Requirements
You need Python with [stravalib](https://github.com/hozn/stravalib) installed: `pip install stravalib`

## Instructions
1. Create a Strava application and follow the instructions here: http://strava.github.io/api/v3/oauth/ to get an access token.
2. Rename the file .stravalib.cfg.sample to .stravalib.cfg (or ~/.stravaupload.cfg') and enter the access token there.
3. Run the script by `./stravaupload.py`
