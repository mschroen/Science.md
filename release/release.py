#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Creates a new release

from batch script:
@echo off
set hour=%time:~0,2%
if "%hour:~0,1%" == " " set hour=0%hour:~1,1%
set min=%time:~3,2%
if "%min:~0,1%" == " " set min=0%min:~1,1%
set secs=%time:~6,2%
if "%secs:~0,1%" == " " set secs=0%secs:~1,1%

set year=%date:~-4%
set month=%date:~3,2%
if "%month:~0,1%" == " " set month=0%month:~1,1%
set day=%date:~0,2%
if "%day:~0,1%" == " " set day=0%day:~1,1%

set datetimef=%year%%month%%day%-%hour%%min%%secs%

mkdir version%datetimef%
cp *.pdf version%datetimef%/
cp *.tex version%datetimef%/
cp *.docx version%datetimef%/
cp *.html version%datetimef%/
cp *.md version%datetimef%/

echo Woohoo! I have successfully generated the folder: version%datetimef%
pause
'''
import glob
import shlex
import subprocess
from datetime import datetime


if __name__ == '__main__':
    # folder name
    folder = 'version' + datetime.today().strftime('%Y%m%d-%H%M%S')

    # add here all file types to save as release
    ftypes = [
        '*.pdf',
        '*.tex',
        '*.docx',
        '*.html',
        '*.md',
    ]

    # grab all files
    files = []
    for ftype in ftypes:
        files.extend(glob.glob(ftype))

    # create folder
    cmd = f'mkdir {folder}'
    subprocess.run(shlex.split(cmd))

    # copy all files to that folder
    cmd = f"cp {' '.join(files)} {folder}"
    subprocess.run(shlex.split(cmd))
    
    print(f'Woohoo! I have successfully generated the folder: {folder}')
    print("done!")