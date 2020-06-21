#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Convert .pdf to .png files automatically
from batch script:
@echo off
echo Turning .pdf to .png
echo ""
for %%f in (*.pdf) do (
    echo   %%~nf
    mutool.exe draw -o "%%~nf.png" -w 600 "%%~nf.pdf"
)
echo ""
pause
'''
import os
import glob
import shlex
import subprocess


if __name__ == '__main__':
    print("converting all *.pdf files to png")
    
    for f in glob.iglob('*.pdf'):
        name, ext = os.path.splitext(f)
        cmd = f'mutool draw -o "{name}.png" -w 600 "{name}.pdf"'
        subprocess.run(shlex.split(cmd))

    print("done!")