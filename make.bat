REM science.md
REM A windows batch file which does exactly the same thing as `make all`.
@echo off
REM Set NAME of the project, defaults to the parent folder name.
for %%a in (.) do set NAME=%%~nxa
@echo %NAME%

REM Merge Markdown
@echo "| cat content/*.md > release/%NAME%.md"
cd content && cat ^
  title.md ^
  abstract.md ^
  introduction.md ^
  methods.md ^
  results.md ^
  conclusion.md ^
  acknowledgements.md ^
  bib.md ^
  > ../release/%NAME%.md
for %%I in (%NAME%.md) do @echo "> Bytes: %%~znI.md"
@echo.

REM make HTML
@echo "| pandoc release/%NAME%.md -o release/%NAME%.html"
cd ../release && pandoc --wrap=preserve -s -S --filter pandoc-crossref --filter pandoc-citeproc -f markdown ^
--template templates/pandoc.html -t html5 --mathjax --number-sections -M secPrefix=section -M tblPrefix=Table ^
%NAME%.md -o %NAME%.html
for %%I in (%NAME%.html) do @echo "> Bytes: %%~znI.html"
@echo.

REM make Word
@echo "| pandoc release/%NAME%.md -o release/%NAME%.docx"
cd ../release && pandoc --wrap=preserve -s -S --filter pandoc-crossref --filter=pandoc-citeproc -f markdown ^
--number-sections -M numberSections=true -M secPrefix=section -M tblPrefix=Table ^
%NAME%.md -o %NAME%.docx
for %%I in (%NAME%.docx) do @echo "> Bytes: %%~znI.docx"
@echo.

REM make LaTeX
@echo "| pandoc release/%NAME%.md -o release/%NAME%.tex"
cd ../release && pandoc --wrap=preserve -s -S --filter pandoc-crossref --filter=pandoc-citeproc -f markdown ^
-V colorlinks -V papersize=A4 -V geometry=margin=1in --number-sections -M secPrefix=section -M tblPrefix=Table ^
--template templates/pandoc.tex %NAME%.md -o %NAME%.tex
for %%I in (%NAME%.tex) do @echo "> Bytes: %%~znI.tex"
@echo.

REM make PDF
@echo "| pandoc release/%NAME%.md -o release/%NAME%.pdf"
sed -i -- 's/\.png/\.pdf/g' ../release/%NAME%.md
cd ../release && pandoc --wrap=preserve -s -S --filter pandoc-crossref --filter=pandoc-citeproc -f markdown ^
-V colorlinks -V papersize=A4 -V geometry=margin=1in --number-sections -M secPrefix=section -M tblPrefix=Table ^
--template templates/pandoc.tex %NAME%.md -o %NAME%.pdf
for %%I in (%NAME%.pdf) do @echo "> Bytes: %%~znI.pdf"
@echo.

REM require any key before close.
pause