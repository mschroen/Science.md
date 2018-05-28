# science.md 
# 1. Make sure you have the following commands available on your system:
#       pandoc ( http://pandoc.org/installing.html )
#       pdflatex (e.g., https://www.tug.org/texlive/acquire-netinstall.html )
#       cat, sed, du, wc, rm (e.g., https://cygwin.com/install.html )
# 2. Use the -s flag to reduce verbose output, e.g., `make -s pdf`
# 3. You can compile the following documents:
#       - Markdown: make -s
#       - LaTeX:    make -s tex
#       - PDF:      make -s pdf
#       - Word:     make -s docx
#       - all:      make -s all
#       - clean:    make clean
# 4. Specify the filename to be used for releases.
#    Default is the parent folder name
NAME = $(shell basename $(CURDIR))

# Merge files from `content/*.md` to a single file `release/NAME.md`
# Outputs also the resulting file size (`du -bh`) and word count (`wc -w`)
merge:
	@echo -e "\e[1;35m| cat content/*.md > release/$(NAME).md\e[0m"
	cd content && cat \
	title.md  \
	abstract.md  \
	introduction.md  \
	methods.md  \
	results.md  \
	conclusion.md  \
	appendix.md  \
	acknowledgements.md  \
	bib.md  \
	> ../release/$(NAME).md
	@echo -e "\e[40;1;32m> " $$(du -bh release/$(NAME).md) "\e[0m" 
	@echo -e "i Less than" $$(wc -w < release/$(NAME).md) "words"

# From Markdown to LaTeX using pandoc
tex: merge
	cp release/$(NAME).md release/$(NAME).md.temp
    
	@echo -e "\e[1;35m| sed s/==XX comment==/*\\XX comment*/ release/$(NAME).md\e[0m"
	sed -i -- 's/==TODO==/\\TODO/g' release/$(NAME).md.temp
	sed -i -- 's/==\([a-zA-Z]\+\) \([^=]\+\)==/*\\\1 \2*/g' release/$(NAME).md.temp
	@echo -e "\e[1;35m| sed s/.png/.pdf/ release/$(NAME).md\e[0m"
	sed -i -- 's/\.png/\.pdf/g' release/$(NAME).md.temp
	
	@echo -e "\e[1;35m| pandoc release/$(NAME).md -o release/$(NAME).tex\e[0m"
	cd release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter=pandoc-citeproc \
	-V colorlinks -V papersize=a4 -V geometry=margin=1in --number-sections -M secPrefix=section -M tblPrefix=Table \
    --template templates/pandoc.tex \
    $(NAME).md.temp -o $(NAME).tex
	
	@echo -e "\e[40;1;32m> " $$(du -bh release/$(NAME).tex) "\e[0m"
	rm release/$(NAME).md.temp

# From Markdown to PDF using pandoc
pdf: merge
	cp release/$(NAME).md release/$(NAME).md.temp
    
	@echo -e "\e[1;35m| sed s/==XX comment==/*\\XX comment*/ release/$(NAME).md\e[0m"
	sed -i -- 's/==TODO==/\\TODO/g' release/$(NAME).md.temp
	sed -i -- 's/==\([a-zA-Z]\+\) \([^=]\+\)==/*\\\1 \2*/g' release/$(NAME).md.temp
	@echo -e "\e[1;35m| sed s/.png/.pdf/ release/$(NAME).md\e[0m"
	sed -i -- 's/\.png/\.pdf/g' release/$(NAME).md.temp
	
	@echo -e "\e[1;35m| pandoc release/$(NAME).md -o release/$(NAME).pdf\e[0m"
	cd release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter=pandoc-citeproc -f markdown \
	-V colorlinks -V papersize=a4 -V geometry=margin=1in --number-sections -M secPrefix=section -M tblPrefix=Table \
    --template templates/pandoc.tex --csl templates/copernicus.csl \
    $(NAME).md.temp -o $(NAME).pdf
	
	@echo -e "\e[40;1;32m> " $$(du -bh release/$(NAME).pdf) "\e[0m"
	rm release/$(NAME).md.temp

# From Markdown to Word using pandoc
docx: merge
	cp release/$(NAME).md release/$(NAME).md.temp
    
	@echo -e "\e[1;35m| sed s/==XX comment==/[XX] comment/ release/$(NAME).md\e[0m"
	sed -i -- 's/==TODO==/<span custom-style="TODO"> TODO <\/span>/g' release/$(NAME).md.temp
	sed -i -- 's/==\([a-zA-Z]\+\) \([^=]\+\)==/<span custom-style="comment-name"> \1 <\/span><span custom-style="comment"> \2<\/span>/g' release/$(NAME).md.temp
	
	@echo -e "\e[1;35m| pandoc release/$(NAME).md -o release/$(NAME).docx\e[0m"
	cd release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter=pandoc-citeproc -f markdown \
	--number-sections -M secPrefix=section -M numberSections=true -M tblPrefix=Table \
	--reference-doc=templates/reference.docx \
	$(NAME).md.temp -o $(NAME).docx
	
	@echo -e "\e[40;1;32m> " $$(du -bh release/$(NAME).docx) "\e[0m"
	rm release/$(NAME).md.temp

# From Markdown to HTML using pandoc
html: merge
	cp release/$(NAME).md release/$(NAME).md.temp
    
	@echo -e "\e[1;35m| sed s/==XX comment==/[XX] comment/ release/$(NAME).md\e[0m"
	sed -i -- 's/==TODO==/<span class="todo">TODO<\/span>/g' release/$(NAME).md.temp
	sed -i -- 's/==\([a-zA-Z]\+\) \([^=]\+\)==/<span class="comment \1"><b>\1<\/b> \2<\/span>/g' release/$(NAME).md.temp
	
	@echo -e "\e[1;35m| pandoc release/$(NAME).md -o release/$(NAME).html\e[0m"
	cd release && pandoc --wrap=preserve -s --filter pandoc-crossref --filter pandoc-citeproc -f markdown \
	--template templates/pandoc.html -t html5 --mathjax --number-sections -M secPrefix=section -M tblPrefix=Table \
	$(NAME).md.temp -o $(NAME).html
	
	@echo -e "\e[40;1;32m> " $$(du -bh release/$(NAME).html) "\e[0m"
	rm release/$(NAME).md.temp

# From Markdown to Everything
all: merge html docx tex pdf

# Clean `release/` folder from garbage. Remove `-i` flag if you know what you do.
clean:
	rm -i release/$(NAME).*
