#!/usr/bin/env python3
# grab version / date of the latest commit


import os
import subprocess


###########################################################################

def get_release_info(version='v1.3.1', date='2021-08-02s'):
    """Grab version and date of the latest commit from a git repository"""
    # go to the repository directory
    dir_orig = os.getcwd()
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    # grab git info into string
    try:
        cmd = "git describe --tags"
        version = subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL)
        version = version.decode('utf-8').strip()

        #if there are new commits after the latest release
        if '-' in version:
            version, num_commit = version.split('-')[:2]
            version += '-{}'.format(num_commit)

        cmd = "git log -1 --date=short --format=%cd"
        date = subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL)
        date = date.decode('utf-8').strip()
    except:
        pass

    # go back to the original directory
    os.chdir(dir_orig)
    return version, date


###########################################################################

release_version, release_date = get_release_info()
release_description = """MintPy release version {v}, release date {d}""".format(
    v=release_version,
    d=release_date,
)

# generate_from: http://patorjk.com/software/taag/
logo = """
___________________________________________________________

  /##      /## /##             /##     /#######           
 | ###    /###|__/            | ##    | ##__  ##          
 | ####  /#### /## /#######  /######  | ##  \ ## /##   /##
 | ## ##/## ##| ##| ##__  ##|_  ##_/  | #######/| ##  | ##
 | ##  ###| ##| ##| ##  \ ##  | ##    | ##____/ | ##  | ##
 | ##\  # | ##| ##| ##  | ##  | ## /##| ##      | ##  | ##
 | ## \/  | ##| ##| ##  | ##  |  ####/| ##      |  #######
 |__/     |__/|__/|__/  |__/   \___/  |__/       \____  ##
                                                 /##  | ##
                                                |  ######/
   Miami InSAR Time-series software in Python    \______/ 
          MintPy {v}, {d}
___________________________________________________________
""".format(v=release_version, d=release_date)

website = 'https://github.com/insarlab/MintPy'

description = 'Miami INsar Time-series software in PYthon'

