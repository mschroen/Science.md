#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Generates a diff

from batch script:
@echo off
REM set folder names of released versions (. means the current (i.e. release) folder)
set OLD=version20161209-145947
set NEW=.

REM use command line arguments, eg. diff.bat file1.tex file2.tex
REM latexdiff %~1 %~2 > diff.tex

REM or use filenames like the current .tex file in release/
for %%i in (*.*) do if "%%~xi"==".tex" ( set NAME=%%~nxi )
latexdiff %OLD%/%NAME% %NEW%/%NAME% > diff.tex

REM compile diff.tex
pdflatex diff.tex
bibtex diff 
pdflatex diff.tex
pdflatex diff.tex

REM remove auxillary files
rm diff.out
rm diff.aux
rm diff.bbl
rm diff.blg
rm diff.log
rm diff.tex

echo Woohoo! I have successfully generated the file diff.pdf 
pause
'''
import os
import glob
import shlex
import subprocess
from datetime import datetime


if __name__ == '__main__':
    # JF TODO: improve this later, take from command line argument
    old_folder = 'version20161209-145947'
    new_folder = '.'
    diff_name = 'diff'

    diff = diff_name + '.tex'

    # get filename from extension
    for f in glob.iglob('*.*'):
        name, ext = os.path.splitext(f)
        if ext == '.tex':
            filename = f
  
    # run latexdiff on tex file
    new = os.path.join(new_folder, filename)
    old = os.path.join(old_folder, filename)
    cmd = f'latexdiff {old} {new}'
    with open(diff, "w") as f:
        subprocess.run(shlex.split(cmd), stdout=f)

    # compile to generate pdf showing diff
    cmds = ['pdflatex', 'bibtex', 'pdflatex', 'pdflatex']
    for cmd in cmds:
        _cmd = f'{cmd} {diff}'
        subprocess.run(shlex.split(_cmd))

    # delete auxiliary files
    auxs = ['.out', '.aux', '.bbl', '.blg', '.log', '.tex']
    aux_files = ' '.join([f'{diff_name}{ext}' for ext in auxs])
    cmd = f'rm {aux_files}'
    subprocess.run(shlex.split(cmd))

    print(f'Woohoo! I have successfully generated the file {diff_name}.pdf')
    print("done!")
