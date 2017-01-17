@echo off

@echo "cat *protocol.md > summary.md"
cat *protocol.md > summary.md

@echo "pandoc summary.md -t beamer -o summary.pdf"
pandoc summary.md  -t beamer --slide-level=2 -V theme:Singapore -o summary.pdf

@echo "rm summary.md"
rm summary.md
pause