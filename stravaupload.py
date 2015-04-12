#!/usr/bin/env python
""" Upload tcx files to Strava
"""

import sys
import os
import webbrowser
from requests.exceptions import ConnectionError, HTTPError
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

from stravalib import Client, exc, model


def main():
    """Main function
    """

    # Parse the input arguments
    parser = ArgumentParser(description='Upload tcx file to Strava')
    parser.add_argument('input', help='Input tcx file')
    parser.add_argument('-t', '--title', help='Title of activity')
    parser.add_argument('-p', '--private', action='store_true',
                        help='Make the activity private')
    parser.add_argument('-a', '--activity', choices=model.Activity.TYPES,
                        metavar='',
                        help='Possible values: {%(choices)s}')
    parser.add_argument('-v', '--view', action='store_true',
                        help='Open the activity in a web browser.')
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

    # Try to upload
    print 'Uploading...'
    try:
        upload = strava.upload_activity(
            activity_file=open(args.input, 'r'),
            data_type='tcx',
            name=args.title,
            private=True if args.private else False,
            activity_type=activity_type
        )
    except exc.ActivityUploadFailed as error:
        print 'An exception occured: ',
        print error
        exit(1)
    except ConnectionError as error:
        print 'No internet connection'
        exit(1)

    print 'Upload succeeded.'
    print 'Waiting for activity...'

    try:
        activity = upload.wait()
    except HTTPError as error:
        print 'HTTPError:' + error
        exit(0)

    print 'Activity id: ' + str(activity.id)

    if args.view:
        url = 'https://www.strava.com/activities/' + str(activity.id)
        webbrowser.open_new_tab(url)


if __name__ == '__main__':
    main()
