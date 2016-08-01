#!/usr/bin/env python
""" Upload files to Strava
"""

import glob
import os
import sys
import webbrowser
from argparse import ArgumentParser
from requests.exceptions import ConnectionError, HTTPError
from ConfigParser import SafeConfigParser

from stravalib import Client, exc, model


def data_type_from_filename(filename):
    """Return the data type from the filename's extension.
    Exit if not supported.
    """

    data_type = None

    for ext in ['.fit', '.fit.gz', '.tcx', '.tcx.gz', '.gpx', '.gpx.gz']:
        if filename.endswith(ext):
            data_type = ext.lstrip('.')

    if not data_type:
        exit('Extension not supported')

    return data_type


def name_and_description_from_file(filename):
    """Find the name and description from GPX files.
    Other files not yet supported.
    """

    if filename.endswith('.gpx') or filename.endswith('.gpx.gz'):
        import gpxpy

        if filename.endswith('.gpx.gz'):
            import gzip
            with gzip.open(filename) as info:
                gpx_data = info.read()
            gpx = gpxpy.parse(gpx_data)

        elif filename.endswith('.gpx'):
            with open(filename) as gpx_data:
                gpx = gpxpy.parse(gpx_data)

        return gpx.name, gpx.description

    return None, None


def upload_file(strava, filename, activity_name, activity_description,
                activity_type, private, view, test, may_exit=True):
    """Upload a single file
    """
    # Find the data type
    data_type = data_type_from_filename(filename)

    # Extract name and description from the file
    if not activity_name or not activity_description:
        new_name, new_description = name_and_description_from_file(filename)
    if not activity_name:
        activity_name = new_name
    if not activity_description:
        activity_description = new_description

    # Try to upload
    print 'Uploading...'
    try:
        if test:
            print 'Test mode: not actually uploading.'
        else:
            upload = strava.upload_activity(
                activity_file=open(filename, 'r'),
                data_type=data_type,
                name=activity_name,
                description=activity_description,
                private=True if private else False,
                activity_type=activity_type
            )
    except exc.ActivityUploadFailed as error:
        print 'An exception occurred: ',
        print error
        if may_exit:
            exit(1)
        return
    except ConnectionError as error:
        print 'No internet connection'
        if may_exit:
            exit(1)
        return

    print 'Upload succeeded.'

    if view:
        print 'Waiting for activity...'

        try:
            activity = upload.wait()
        except HTTPError as error:
            if error.args[0].startswith('401'):
                print "You don't have permission to view this activity"
            else:
                print 'HTTPError: ' + ', '.join(str(i) for i in error.args)
            return

        print 'Activity id: ' + str(activity.id)

        url = 'https://www.strava.com/activities/' + str(activity.id)
        webbrowser.open_new_tab(url)


def main():
    """Main function
    """

    # Parse the input arguments
    parser = ArgumentParser(description='Upload files to Strava')
    parser.add_argument('input', help='Input filename')
    parser.add_argument('-t', '--title', help='Title of activity')
    parser.add_argument('-d', '--description', help='Description of activity')
    parser.add_argument('-p', '--private', action='store_true',
                        help='Make the activity private')
    parser.add_argument('-a', '--activity', choices=model.Activity.TYPES,
                        metavar='',
                        help='Possible values: {%(choices)s}')
    parser.add_argument('-v', '--view', action='store_true',
                        help='Open the activity in a web browser.')
    parser.add_argument('-x', '--test', action='store_true',
                        help="Don't actually upload anything.")
    args = parser.parse_args()

    # Check if an access token is provided
    configfile = [os.path.expanduser('~/.stravaupload.cfg'),
                  '.stravaupload.cfg']
    config = SafeConfigParser()
    config.read(configfile)

    if config.has_option('access', 'token'):
        access_token = config.get('access', 'token')
    else:
        print 'No access_token found in %s' % configfile
        sys.exit(0)

    # Get activity type
    activity_type = None
    if args.activity:
        activity_type = args.activity
    elif config.has_option('default', 'activity'):
        activity_type = config.get('default', 'activity')

    strava = Client()
    strava.access_token = access_token

    # Is the input a single file or wildcard?
    if os.path.isfile(args.input):
        upload_file(strava, args.input, args.title, args.description,
                    activity_type, args.private, args.view, args.test)
    else:
        filenames = glob.glob(args.input)
        if len(filenames) == 0:
            sys.exit('No input files found')
        else:
            for i, filename in enumerate(filenames):
                print i+1, "/", len(filenames)
                upload_file(strava, filename, args.title, args.description,
                            activity_type, args.private, args.view, args.test,
                            may_exit=False)


if __name__ == '__main__':
    main()
