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