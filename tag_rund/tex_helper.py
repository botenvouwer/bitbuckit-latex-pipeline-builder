import os

def addVersion(texFile, version='latest'):

    line = "\\newcommand{\PipelineBuildVersion}{%s}" % version

    with open(texFile, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def generateLatexFile(texFile):
    os.system('latexmk -cd -e \'$$pdflatex="pdflatex -interaction=nonstopmode %%S %%0"\' -f -pdf "%s"' % texFile)