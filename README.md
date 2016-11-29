# science.md
Framework for drafting scientific documents: Write (Markdown), Compile (PDF, Word, HTML), Share (Git)

## Concept

This framework is designed to make writing easier. It provides lots of helper scripts to do the work for you, like building the manuscript PDF, creating folders for milestones, generating diffs, and more. You can focus on writing, while formatting, compiling, and collaborating just works for everyone like a charm.

## Requirements 

### Editing

You do not need anything to write your draft, but a simple text editor to edit the files `content/*.md`. Some text editor suggestions:

- Simple, fast, syntax-highlighting: [Notepad2](https://xhmikosr.github.io/notepad2-mod/)
- Advanced, powerful, incl. Markdown preview: [Atom Editor](https://atom.io/)
- *(most intuitive)* What you see is what you get: [Typora](https://www.typora.io/#download)

### Compiling

If you want to compile your text to LaTeX, PDF, Word, or HTML, you need:

- [pandoc](http://pandoc.org/installing.html), and the additional [cross-ref filter](https://github.com/lierdakil/pandoc-crossref/releases/). The latter is to be extracted into the same folder as pandoc was installed.
- `pdflatex`, e.g., from the [TeXlive distribution](https://www.tug.org/texlive/acquire-netinstall.html),

Then some very basic `bash` commands are needed. Most of them are actually standard on Linux or Mac, but Windows sometimes needs a slight additional kick.

- `make`, `cat`, `sed`, `du`, `rm`, `wc`, e.g. from the [cygwin distribution](https://cygwin.com/install.html).
- *(Optional):* A useful terminal, e.g., `mintty`, also from cygwin.

I recommend creating `.png` equivalents from every `.pdf` figure, such that HTML and Word output can actually display the (originally) `.pdf` figures. There is a handy script for that in `fig/pdf2png.bat`, which requires *mutools*:

- [mutools software](http://mupdf.com/).

**General Note:** Please make sure that all the binaries files of your installed tools are accessible from command line, i.e., registered in the system paths. On Windows, add all folders containing `pandoc`, `pdflatex`, `mutools`, `cygwin/bin`, etc, to the system path via `Control Panel > System > Advanced > Environmental Variables`.


## Workflow

I recommend to use the `git` version control to commit stages or publish your version to your self-hosted repository. Ofcourse, also `SVN` would do. There are many GUI tools that can make life easier, too. 

1. **Get up to date with remote changes:** `git pull`, or with *GitHub Desktop* press `Sync`.
2. **Examine what your colleagues did:** `git diff` or `git log`, or with *GitHub Desktop*'s `History` tab. Or use run the script `release/diff.bat` to create a *latexdiff* between the current and the latest released version.
3. **Contribute:** change text in `content/*.md`, add figures to `fig/*`, etc.
4. *(Optional):* compile to HTML, Word, PDF using `make -s all` or `make.bat`.
5. *(Optional):* store a milestone version by using `release/release.bat`.
6. **Commit your work:** `git add . && git commit -am "Message"`, or with *GitHub Desktop* press `Commit`.
7. **Upload your contribution:** `git push`, or with *GitHub Desktop* press `Sync`.

## Comments

- *Visible* comments can be started within the text by typing a *backslash* followed by your initials, e.g. `\MS I better like invisble comments.` Use the YAML settings in `content/title.md` to add more initials and corresponding colors.
- *Invisible* comments will not appear in the compiled output and can be of any length. Those comments follow the HTML style guide and look like this: `<!--- this is a comment --->`

## Figures

- Figure files are located in the folder `fig/`
- Always try to create `.pdf` files to assure high-quality figures. Only for pure photographs `.jpg` is acceptable.
- After adding or changing `.pdf` figures, go to `fig/` and run `pdf2png.bat`. This will convert all `.pdf` figures to `.png` equivalents, which are easier to visualize in text editors, Word, and web browsers.
- Add figures to the Markdown text using `![caption](../fig/name.png)`. Use `.png` extension even for `.pdf` figures, to make them visible for Typora, Word, HTML. The PDF compiled output will always use the corresponding `.pdf` file.

## Literature

Add a citation using `@Eistein1905` or `[see also @Eistein1905]`. The corresponding name must be appended to `lit/references.bib`. Those BibTeX entries can be found everywhere in the internet, e.g. using the *google scholar*  search engine or export from any reference manager.

## Compile

The test from `content/*.md` can be compiled to Markdown, LaTeX, PDF, or Word. 

1. *(once)* open the file `Makefile` or `make.bat` and make sure that the `.md` files are arranged in the corrected order. If you added new files to `content/`, also add them to the given list.
2. Compile:
        a. If you have a capable terminal, run `make -s all` to compile to all available output formats. Use the flag `-s` to reduce verbose output. The following commands are available: 
            - Markdown: make -s
            - LaTeX:    make -s tex
            - PDF:      make -s pdf
            - Word:     make -s docx
            - all:      make -s all
            - clean:    make clean
        b. On Windows, you can simply double-click the file `make.bat` to compile to all output formats.

## Release

The currently compiled files are stored in `release/` and can be copied to an extra folder, `release/version[Date]-[Time]`, to permanently save one version, which can be used later to perform diffs, for instance. This process has been automated, simply go to `release/` and run `release.bat`.

## Difference between two versions

- The difference between two commits can be visualised with `git diff`, or using the *GitHub Desktop* GUI.
- The difference between two released versions can be visualised using the `latexdiff` script that usually comes with the `texlive` distribution. Edit the file `diff.bat` by specifiying the two folders which you want to compare (the *new* version defaults to the current files in the `release/`folder). Then run `diff.bat`. It creates diffs from the two `.tex` files in the given folders and compiles a new `diff.pdf` where differences are nicely highlighted.

# Markdown Syntax

- citation: `@Einstein2015`, or `[see @Einstein2015; @Newton1730, and references therein]`
- section: `# Section`, `## Subsection`, `### Subsubsection {#sec:label}`, ...
- figure: `![caption](../fig/file.png){#fig:label}`
- math: `$x=1$`, `$$ A=B $$ {#eq:label}`
- reference: `@Fig:label`, `@sec:label`, `@eq:label`, `@tbl:label`
- comments: `\XX text until two newlines`, `\MS personalized comment`, `<!--- invisble comment --->`
- code: ``code``
- table:

    |  A  |               B | C     |
    | --: | --------------: | :---: |
    |  42 |         $y=x+1$ | True  |
    |  23 |            None | False |

    Table: Caption. {#tbl:label}
