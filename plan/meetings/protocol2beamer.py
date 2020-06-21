#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Create presentation

from batch script:
@echo off

@echo "cat *protocol.md > summary.md"
cat *protocol.md > summary.md

@echo "pandoc summary.md -t beamer -o summary.pdf"
pandoc summary.md  -t beamer --slide-level=2 -V theme:Singapore -o summary.pdf

@echo "rm summary.md"
rm summary.md
pause
'''
import glob
import shlex
import subprocess

if __name__ == '__main__':

    print("cat *protocol.md > summary.md")
    files = ' '.join(glob.glob('*protocol.md')
    cmd = f'cat {files}'
    with open('summary.md', "w") as f:
        subprocess.run(shlex.split(cmd), stdout=f)
    
    print("pandoc summary.md -t beamer -o summary.pdf")
    cmd = 'pandoc summary.md -t beamer --slide-level=2 -V theme:Singapore -o summary.pdf'
    subprocess.run(shlex.split(cmd))

    print("rm summary.md")
    cmd = 'rm summary.md'
    subprocess.run(shlex.split(cmd))
