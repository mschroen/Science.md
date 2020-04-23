#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Create Gantt diagrams.

from batch script:
@echo off
@echo pandoc Gantt.md -o Gantt.html
pandoc -s -t html5 Gantt.md --template templates/gantt-template.html -H templates/mermaid.min.js.html -o Gantt.html
@echo sed fine-tuning...
sed -i -- 's/.code.gantt/gantt/' Gantt.html
sed -i -- 's/..code.\(..pre.\)/\1/' Gantt.html
@echo.
pause
'''
import shlex
import subprocess

if __name__ == '__main__':
    print("pandoc Gantt.md -o Gantt.html")
    cmd = (
        'pandoc -s -t html5 Gantt.md'
        ' --template templates/gantt-template.html'
        ' --metadata title="Gant"'
        ' -H templates/mermaid.min.js.html -o Gantt.html'
    )
    subprocess.run(shlex.split(cmd))

    print("sed fine-tuning...")
    cmd = 'sed -i -- \'s/.code.gantt/gantt/\' Gantt.html'
    subprocess.run(shlex.split(cmd))
    cmd = 'sed -i -- \'s/..code.\(..pre.\)/\1/\' Gantt.html'
    subprocess.run(shlex.split(cmd))

    print("done!")