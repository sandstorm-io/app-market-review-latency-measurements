import json
import urllib2
import os
import sys
import glob

SAMPLE_DATA = {
    u'apps': [{u'appId': u'vfnwptfn02ty21w715snyyczw0nqxkv3jvawcah10c6z7hj1hnu0',
               u'author': {u'githubUsername': u'engelgabriel',
                           u'hackernewsUsername': u'engelgabriel',
                           u'keybaseUsername': u'gabrielengel',
                           u'name': u'Gabriel Engel',
                           u'picture': u'https://s3.amazonaws.com/keybase_processed_uploads/2c7b65ea5fdf38a96e7eb58cf0b9e305_360_360_square_360.jpeg',
                           u'redditUsername': u'gabriel_engel',
                           u'twitterUsername': u'gabriel_engel'},
               u'categories': [u'Communications',
                               u'Productivity',
                               u'Office',
                               u'Social',
                               u'DevTools'],
               u'codeLink': u'https://github.com/RocketChat/Rocket.Chat',
               u'createdAt': u'1970-01-01T00:00:00Z',
               u'imageId': u'1a2cca1a21b5000e717807090c9b1177.svg',
               u'isOpenSource': True,
               u'name': u'Rocket.Chat',
               u'packageId': u'2d7833a1f56776958cf967123f11d0f6',
               u'shortDescription': u'Chat app',
               u'upstreamAuthor': u'Rocket.Chat',
               u'version': u'0.45.0',
               u'versionNumber': 45,
               u'webLink': u'https://rocket.chat'}]}

def get_app_data():
    as_bytes = urllib2.urlopen("https://app-index.sandstorm.io/experimental/index.json").read()
    app_data = json.loads(as_bytes)
    return app_data

def alert_or_not(app_data):
    error_output = ''
    if not os.path.exists('state'):
        os.mkdir('state')
    apps = app_data.get('apps', [])
    filenames_to_keep = []
    for package in apps:
        packageId = package['packageId']
        name = package['name']
        packageIdAsFilename = 'state/' + packageId
        filenames_to_keep.append(packageIdAsFilename)
        if os.path.exists(packageIdAsFilename):
            error_output += 'Found old package: %s - %s\n\n' % (
                name, packageId)
        else:
            with open(packageIdAsFilename, 'w') as just_touching_the_file:
                pass

    for filename in glob.glob('state/*'):
        if filename not in filenames_to_keep:
            os.unlink(filename)

    return error_output

def main(app_data=None):
    if app_data is None:
        app_data = get_app_data()
    errors = alert_or_not(app_data)
    if errors:
        print errors
        sys.exit(1)

if __name__ == '__main__':
    main()
