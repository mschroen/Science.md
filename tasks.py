# -*- coding: utf-8 -*-
'''
Build script for Science.md

Install Invoke using pip or pacman package manager, then run from cli:
    jf@mymachine ~$ invoke all

author: JF
'''
# standard library modules
import os
import shutil
import tempfile

# third party modules
from invoke import task
import regex as re
from colorama import Fore, Back, init

# initialize colorama
init(autoreset=True)

# set filename
file_name = os.path.basename(os.path.abspath('.'))

# set document content, watch out: order matters
content = [
    'title.md',
    'abstract.md',
    'introduction.md',
    'methods.md',
    'results.md',
    'conclusion.md',
    'appendix.md',
    'acknowledgements.md',
    'bib.md',
]


# emulate sed inplace edit using regular expresions
def sed_i(re_a: str, re_b: str, file_name: str):
    # create a temporary file to store data, as file can be big
    with tempfile.TemporaryFile(mode='w+', encoding='utf-8') as tmp:
        with open(file_name, 'r') as fi:
            for line in fi:
                tmp.write(re.sub(re_a, re_b, line, flags=re.VERSION1))
        # rewind
        tmp.seek(0)
        # write output on the same file
        with open(file_name, 'w') as fo:
            fo.writelines(tmp.readlines())


def wc_w(file_name: str) -> int:
    ''' FROM HOWTO: \\S Matches any non-whitespace character;
        this is equivalent to the class [^ \\t\\n\\r\\f\\v].
        Not very accurate, but this gives the same result as wc -w
    '''
    # use iterator to avoid using a big list in case of large files
    n_words = sum(1 for _ in re.finditer(r'\S+', open(file_name).read(), flags=re.VERSION1))
    # n_words = len(re.findall(r'\S+', open(file_name).read()))
    return n_words


def human_readable(bsize: int) -> str:
    """This function will convert bytes to MB.... GB... etc"""
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if bsize < 1024:
            bsize_str = f"{bsize:3.1f} {unit}"
            break
        bsize >>= 10
    return bsize_str


# emulate du -bh functionality
def du_bh(file_name: str) -> str:
    size = os.stat(file_name).st_size
    return f'{human_readable(size)} {file_name}'


def confirm(prompt='Confirm', res=False):
    """Prompts confirmation from the user, returns True for yes.

    The default value assumed when user types ENTER.
    """
    prompt = f'{prompt} [Y/n] ' if res else f'{prompt} [y/N] '

    while True:
        ans = input(prompt).lower()
        if not ans:
            return res
        if ans not in ['y', 'yes', 'n', 'no']:
            print('please enter y(es) or n(o)!')
            continue
        return (ans == 'y')


def rm_i(file_name: str):
    if confirm(f'Do you really want to delete {file_name}?'):
        os.remove(file_name)


@task
def merge(c):
    '''Meges all content file into one big file for later processing.'''

    # create a text list with all content pages
    # concatenate file contents, (it can be done with python later)
    print(Fore.LIGHTMAGENTA_EX + f'cat content/*.md > release/{file_name}.md')
    
    # read content files from content folder and write it 
    # into a one big file inside release folder
    dst = os.path.join('release', f'{file_name}.md')
    with open(dst, 'w') as fo:
        for md_file in content:
            src = os.path.join('content', md_file)
            with open(src, 'r') as fi:
                fo.writelines(fi.readlines())

    # file space usage estimation
    size = du_bh(f'release/{file_name}.md')
    print(Fore.LIGHTGREEN_EX + f'> {size}')

    # word count
    n = wc_w(f'release/{file_name}.md')
    print(f'i Less than {n} words')
    # res = c.run(f'wc -w < release/{file_name}.md' , hide='both')
    # print(f'i Less than {res.stdout.rstrip()} words')


@task(merge)
def tex(c):
    '''From Markdown to LaTeX using pandoc'''

    # create a temporary file
    shutil.copyfile(f'release/{file_name}.md', f'release/{file_name}.temp.md')

    # work on comments
    print(Fore.LIGHTMAGENTA_EX + f'| sed s/==XX comment==/*\\XX comment*/ release/{file_name}.md')

    # First change TODO tags
    sed_i(r'==TODO==', r'\\TODO', f'release/{file_name}.temp.md')
    # Then change all other tags
    sed_i(r'==([a-zA-Z]+) ([^=]+)==', r'*\\\1 \2*', f'release/{file_name}.temp.md')

    # change extension to .pdf in image strings
    print(Fore.LIGHTMAGENTA_EX + f'| sed s/.png/.pdf/ release/{file_name}.md')
    sed_i(r'.png', r'.pdf', f'release/{file_name}.temp.md')

    # pandoc options, modify parameters here!
    pandoc_opts = [
        '--wrap=preserve',
        '-s',
        '--filter pandoc-crossref',
        '--filter=pandoc-citeproc',
        '-f markdown',
        '-V colorlinks',
        '-V papersize=a4',
        '-V geometry=margin=1in',
        '--number-sections',
        '-M secPrefix=section',
        '-M tblPrefix=Table',
        '--template templates/pandoc.tex',
    ]
    # run pandoc
    print(Fore.LIGHTMAGENTA_EX + f'| pandoc release/{file_name}.md -o release/{file_name}.tex')
    os.chdir('release')
    c.run(f'pandoc {" ".join(pandoc_opts)} {file_name}.temp.md -o {file_name}.tex')
    os.chdir('..')

    # file space usage estimation
    size = du_bh(f'release/{file_name}.tex')
    print(Fore.LIGHTGREEN_EX + f'> {size}')

    # delete auxiliary files
    os.remove(f'release/{file_name}.temp.md')


@task(merge)
def pdf(c):
    '''From Markdown to PDF using pandoc'''

    # create a temporary file
    shutil.copyfile(f'release/{file_name}.md', f'release/{file_name}.temp.md')

    # work on comments
    print(Fore.LIGHTMAGENTA_EX + f'| sed s/==XX comment==/*\\XX comment*/ release/{file_name}.md')

    # First change TODO tags
    sed_i(r'==TODO==', r'\\TODO', f'release/{file_name}.temp.md')
    # Then change all other tags
    sed_i(r'==([a-zA-Z]+) ([^=]+)==', r'*\\\1 \2*', f'release/{file_name}.temp.md')

    # change extension to .pdf in image strings
    print(Fore.LIGHTMAGENTA_EX + f'| sed s/.png/.pdf/ release/{file_name}.md')
    sed_i(r'.png', r'.pdf', f'release/{file_name}.temp.md')

    # pandoc options, modify parameters here!
    pandoc_opts = [
        '--wrap=preserve',
        '-s',
        '--filter pandoc-crossref',
        '--filter=pandoc-citeproc',
        '-f markdown',
        '-V colorlinks',
        '-V papersize=a4',
        '-V geometry=margin=1in',
        '--number-sections',
        '-M secPrefix=section',
        '-M tblPrefix=Table',
        '--template templates/pandoc.tex',
        '--csl templates/copernicus.csl',
    ]
    # run pandoc
    print(Fore.LIGHTMAGENTA_EX + f'| pandoc release/{file_name}.md -o release/{file_name}.pdf')
    os.chdir('release')
    c.run(f'pandoc {" ".join(pandoc_opts)} {file_name}.temp.md -o {file_name}.pdf')
    os.chdir('..')

    # file space usage estimation
    size = du_bh(f'release/{file_name}.pdf')
    print(Fore.LIGHTGREEN_EX + f'> {size}')

    # delete auxiliary files
    os.remove(f'release/{file_name}.temp.md')


@task(merge)
def docx(c):
    '''From Markdown to Word using pandoc'''

    # create a temporary file
    shutil.copyfile(f'release/{file_name}.md', f'release/{file_name}.temp.md')

    # work on comments
    print(Fore.LIGHTMAGENTA_EX + f'| sed s/==XX comment==/*\\XX comment*/ release/{file_name}.md')

    # First change TODO tags
    sed_i(r'==TODO==', r'<span custom-style="TODO"> TODO </span>', f'release/{file_name}.temp.md')

    # Then change all other tags
    sed_i(
        r'==([a-zA-Z]+) ([^=]+)==',
        r'<span custom-style="comment-name"> \1 </span><span custom-style="comment"> \2</span>',
        f'release/{file_name}.temp.md'
    )

    # pandoc options, modify parameters here!
    pandoc_opts = [
        '--wrap=preserve',
        '-s',
        '--filter pandoc-crossref',
        '--filter=pandoc-citeproc',
        '-f markdown',
        '--number-sections',
        '-M secPrefix=section',
        '-M numberSections=true',
        '-M tblPrefix=Table',
        '--reference-doc=templates/reference.docx',
    ]
    # run pandoc
    print(Fore.LIGHTMAGENTA_EX + f'| pandoc release/{file_name}.md -o release/{file_name}.docx')

    os.chdir('release')
    c.run(f'pandoc {" ".join(pandoc_opts)} {file_name}.temp.md -o {file_name}.docx')
    os.chdir('..')

    # file space usage estimation
    size = du_bh(f'release/{file_name}.docx')
    print(Fore.LIGHTGREEN_EX + f'> {size}')

    # delete auxiliary files
    os.remove(f'release/{file_name}.temp.md')


@task(merge)
def html(c):
    '''From Markdown to HTML using pandoc'''

    # create temporary file
    shutil.copyfile(f'release/{file_name}.md', f'release/{file_name}.temp.md')

    # change comment strings
    print(Fore.LIGHTMAGENTA_EX + f'| sed s/==XX comment==/[XX] comment/ release/{file_name}.md')
    # First change TODO tags
    sed_i(r'==TODO==', r'<span class="todo">TODO</span>', f'release/{file_name}.temp.md')
    # Then change all other tags
    sed_i(
        r'==([a-zA-Z]+) ([^=]+)==',
        r'<span class="comment \1"><b>\1</b> \2</span>',
        f'release/{file_name}.temp.md'
    )

    # pandoc options, modify parameters here!
    pandoc_opts = [
        '--wrap=preserve',
        '-s',
        '--filter pandoc-crossref',
        '--filter pandoc-citeproc',
        '-f markdown',
        '--template templates/pandoc.html',
        '-t html5',
        '--mathjax',
        '--number-sections',
        '-M secPrefix=section',
        '-M tblPrefix=Table',
    ]
    # run pandoc
    print(Fore.LIGHTMAGENTA_EX + f'| pandoc release/{file_name}.md -o release/{file_name}.html')
    os.chdir('release')
    c.run(f'pandoc {" ".join(pandoc_opts)} {file_name}.temp.md -o {file_name}.html')
    os.chdir('..')

    # file space usage estimation
    size = du_bh(f'release/{file_name}.html')
    print(Fore.LIGHTGREEN_EX + f'> {size}')

    # delete auxiliary files
    os.remove(f'release/{file_name}.temp.md')


@task(pre=[merge, html, docx, tex, pdf])
def all(c):
    '''From Markdown to Everything'''
    pass


@task
def clean(c):
    '''Clean `release/` folder from garbage. Remove `-i` flag if you know what you do.'''
    os.chdir('release')
    with os.scandir('.') as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                if entry.name.startswith(file_name):
                    rm_i(entry.name)
    os.chdir('..')
    # c.run(f'rm -i release/{file_name}.*')
