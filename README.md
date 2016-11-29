# Science.md
An easy framework for drafting scientific documents: *Write* (Markdown), *Compile* (PDF, Word, HTML), *Share*.

## Concept

This framework is designed to make writing easier. It provides lots of helper scripts to do the work for you, like building the manuscript PDF, creating folders for milestones, generating diffs, and more. You can focus on writing, while formating, compiling, and collaborating will just work like a charm.

### Philosophy

*Have you heared about the ever-lasting discussion between [Word and Latex](http://tex.stackexchange.com/questions/218567/latex-vs-word-improvements-of-latex-over-the-years) [users](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115069)?* Don't try to convince your coauthors, you'll fail. My philosophy is that everyone is free and can use their favorit tool. Don't standardarize things. Let your coauthors decide whether they want to annotate your PDF, to put comments in Word, or to write directly in Markdown using your repository.

Markdown actually combines advantages of both, Word and Latex, and in the far future, everyone will use it ;-) But today, noone should be forced to.

### Advantages to other collaborative writing tools:

- **Write in Markdown:** Focus on writing, not on Latex's commands or Word's formatting mess. Paper writing is now possible with simple plain text.
- **Self-hosting repositories:** use any version control software hosted by you or your institution. Many institutions do not allow research to be hosted at someone else's server. You don't even have to use a remote repository, it's all yours!
- **Work offline** from any location. That allows you to be independent from Wifi, and still be able to do fancy WYSIWYG writing in Markdown, e.g., using [Typora](http://www.typora.io/). 
- **Full control:** It's your own folder, your own desktop, your own data. Add analysis scripts, processed data, sketches, ideas, and share anything without being bothered to upload. And by the way, it's only you who decides who has access to your repository.
- **Fast compilation:** PDF and Word documents are created within seconds. By sharing both, your colleagues can choose how they want to annotate and comment your work. Want to put your paper on a website? It's just a millisecond away.
- **Fully adaptable:** all the scripts and templates are open-source. Adapt it to your needs. For example, use a specific journal template, or add more features. 


## Requirements 

### OS

*Science.md* uses no OS-specific software and thus should work on any operating system. However, so far it has been tested only on Windows, and I would be glad if someone could test it on Mac and Linux!

### Editing

You do not need anything to write your draft, but a simple text editor to edit the files `content/*.md`. Some text editor suggestions:

- Simple, fast, syntax-highlighting: [Notepad2](https://xhmikosr.github.io/notepad2-mod/)
- Advanced, powerful, incl. Markdown preview: [Atom Editor](https://atom.io/)
- *(most intuitive)* What you see is what you get: [Typora](https://www.typora.io/#download)

### Compiling

If you want to compile your text to LaTeX, PDF, Word, or HTML, you need:

- [pandoc](http://pandoc.org/installing.html), and the additional [cross-ref filter](https://github.com/lierdakil/pandoc-crossref/releases/). The latter is to be extracted into the same folder as pandoc was installed.
- `pdflatex`, e.g., from the [TeXlive distribution](https://www.tug.org/texlive/acquire-netinstall.html),

Then some very basic `bash` commands are needed. Most of them are actually standard on Linux and Mac, but Windows sometimes needs a slight additional kick.

- `make`, `cat`, `sed`, `du`, `rm`, `wc`, e.g. from the [cygwin distribution](https://cygwin.com/install.html).
- *(Optional):* A useful terminal, e.g., `mintty`, also from cygwin.

I recommend creating `.png` equivalents from every `.pdf` figure, such that HTML and Word output can actually display the (originally `.pdf`) figures. There is a handy script for this job in `fig/pdf2png.bat`, which requires *mutools*:

- [mutools software](http://mupdf.com/).

*General Note: Please make sure that all the binaries files of your installed tools are accessible from command line, i.e., registered in the system paths. On Windows, add all folders containing `pandoc.exe`, `pdflate.exe`, `mutools.exe`, `cygwin/bin/`, etc, to the system path via `Control Panel > System > Advanced > Environmental Variables`.*


## Workflow

To start writing your paper, use this *Science.md* repository as a template. Just download the whole repository and copy all its content into the folder of your project, which is probably called "my_nature_paper-no3". 

If you want to version-control or share your work, I'd recommend `git` , but also `svn` or anything else would do, it's all your choice. You can self-host the repository remotely on your own server if you want.  There are many GUI tools for version-control, from which I think [GitHub Desktop](https://desktop.github.com/) is the most easy to use for non-geeks. 

1. **Get up to date with remote changes:** `git pull`, or with *GitHub Desktop* press `Sync`.
2. **Examine what your colleagues did:** `git diff` or `git log`, or with *GitHub Desktop*'s `History` tab. Or use run the script `release/diff.bat` to create a *latexdiff* between the current and the latest released version.
3. **Contribute:** change text in `content/*.md`, add figures to `fig/*`, etc.
4. *(Optional):* compile to HTML, Word, PDF using `make -s all` or `make.bat`.
5. *(Optional):* store a milestone version by using `release/release.bat`.
6. **Commit your work:** `git add . && git commit -am "Message"`, or with *GitHub Desktop* press `Commit`.
7. **Upload your contribution:** `git push`, or with *GitHub Desktop* press `Sync`.

As soon as your paper is ready and went smoothly through the internal review, you can submit it to a journal. You can either submit the Word document, or the LateX document. Some journals require a certain LaTeX template, which should be easy to fill with the content from `release/NAME.tex` that *Science.md* generated for you.

## Comments

- **Visible** comments can be started within the text by typing a *backslash* followed by your initials, e.g. `\MS I better like invisble comments.` Use the YAML settings in `content/title.md` to add more initials and corresponding colors.
- **Invisible** comments will not appear in the compiled output and can be of any length. Those comments follow the HTML style guide and look like this: `<!--- this is a comment --->`

## Figures

- Figure files are located in the folder `fig/`
- Always try to create `.pdf` files to assure high-quality figures. Only for pure photographs `.jpg` is acceptable.
- After adding or changing `.pdf` figures, go to `fig/` and run `pdf2png.bat`. This will convert all `.pdf` figures to `.png` equivalents, which are easier to visualize in text editors, Word, and web browsers.
- Add figures to the Markdown text using `![caption](../fig/name.png){#fig:label}`. Use the  `.png` extension even for `.pdf` figures, to make them visible for Typora, Word, HTML. The PDF compiled output will always use the corresponding `.pdf` file.

## Literature

Add a citation using `@Eistein1905` or `[see also @Eistein1905]`. The corresponding name must be appended to `lit/references.bib`. Those BibTeX entries can be found everywhere in the internet, e.g. using the *google scholar*  search engine or export from any reference manager.

## Compile

The text from `content/*.md` can be compiled to Markdown, LaTeX, PDF, or Word. 

1. *(Once):* Open the file `Makefile` or `make.bat` and make sure that the `.md` files are arranged in the correct order. If you added new files to `content/`, also add them to the given list.
2. If you have a capable terminal, run `make -s all` to compile to all available output formats. Use the flag `-s` to reduce verbose output. The following commands are available:
   * Markdown: `make -s`
   * LaTeX:    `make -s tex`
   * PDF:      `make -s pdf`
   * Word:     `make -s docx`
   * all:      `make -s all`
   * clean:    `make clean`

3. *(Or):* On Windows, you can simply double-click the file `make.bat` to compile to all output formats.

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
    ```
    |  A  |               B | C     |
    | --: | --------------: | :---: |
    |  42 |         $y=x+1$ | True  |
    |  23 |            None | False |

    Table: Caption. {#tbl:label}
    ```
