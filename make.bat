@echo off
REM science.md
REM A windows batch file which does exactly the same thing as `make all`.
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
  appendix.md ^
  acknowledgements.md ^
  bib.md ^
  > ../release/%NAME%.md
for %%I in (%NAME%.md) do @echo "> Bytes: %%~znI.md"
@echo.

REM make HTML
@echo "| pandoc release/%NAME%.md -o release/%NAME%.html"

cp ../release/%NAME%.md ../release/%NAME%.md.temp
sed -i -- 's/==TODO==/^<span class="todo"^>TODO^<\/span^>/g' ../release/%NAME%.md.temp
sed -i -- 's/==\([a-zA-Z]\+\) \([^^=]\+\)==/^<span class="comment \1"^>^<b^>\1^<\/b^> \2^<\/span^>/g' ../release/%NAME%.md.temp

cd ../release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter pandoc-citeproc -f markdown ^
--template templates/pandoc.html -t html5 --mathjax --number-sections -M secPrefix=section -M tblPrefix=Table ^
%NAME%.md.temp -o %NAME%.html
for %%I in (%NAME%.html) do @echo "> Bytes: %%~znI.html"
@echo.


REM make Word
@echo "| pandoc release/%NAME%.md -o release/%NAME%.docx"

cp ../release/%NAME%.md ../release/%NAME%.md.temp
sed -i -- 's/==TODO==/^<span custom-style="TODO"^> TODO ^<\/span^>/g' ../release/%NAME%.md.temp
sed -i -- 's/==\([a-zA-Z]\+\) \([^^=]\+\)==/^<span custom-style="comment-name"^> \1 ^<\/span^>^<span custom-style="comment"^> \2^<\/span^>/g' ../release/%NAME%.md.temp

cd ../release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter=pandoc-citeproc -f markdown ^
--number-sections -M numberSections=true -M secPrefix=section -M tblPrefix=Table ^
--reference-doc=templates/reference.docx ^
%NAME%.md.temp -o %NAME%.docx
for %%I in (%NAME%.docx) do @echo "> Bytes: %%~znI.docx"
@echo.

REM make LaTeX
@echo "| pandoc release/%NAME%.md -o release/%NAME%.tex"

cp ../release/%NAME%.md ../release/%NAME%.md.temp
sed -i -- 's/==TODO==/\\\\TODO/g' ../release/%NAME%.md.temp
sed -i -- 's/==\([a-zA-Z][^^=]\+\)==/\*\\\\\1\*/g' ../release/%NAME%.md.temp
sed -i -- 's/\.png/\.pdf/g' ../release/%NAME%.md.temp

cd ../release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter=pandoc-citeproc -f markdown ^
-V colorlinks -V papersize=a4 -V geometry=margin=1in --number-sections -M secPrefix=section -M tblPrefix=Table ^
--template templates/pandoc.tex %NAME%.md.temp -o %NAME%.tex
for %%I in (%NAME%.tex) do @echo "> Bytes: %%~znI.tex"
@echo.

REM make PDF
@echo "| pandoc release/%NAME%.md -o release/%NAME%.pdf"

cd ../release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter=pandoc-citeproc -f markdown ^
-V colorlinks -V papersize=a4 -V geometry=margin=1in --number-sections -M secPrefix=section -M tblPrefix=Table ^
--template templates/pandoc.tex --csl templates/copernicus.csl %NAME%.md.temp -o %NAME%.pdf
for %%I in (%NAME%.pdf) do @echo "> Bytes: %%~znI.pdf"
@echo.

rm ../release/%NAME%.md.temp

REM require any key before close.
pause