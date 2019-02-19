import sys
import os
from shutil import copyfile
from git import Repo
from tag_rund.tag_helper import *
from tag_rund.tex_helper import *

repoPath = sys.argv[1]
ext = 'tex'

os.chdir(repoPath)

# Fix for bitbuckit pipeline -> is necessary for tag trigger
os.system('git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"')
os.system('git fetch')

os.system('git checkout master')
os.system('git pull')

repo = Repo('./')

if 'publish' not in repo.branches:
    os.system('git branch publish')

os.system('git checkout publish')
os.system('git pull')
os.system('git merge --strategy-option=theirs master')

doneList = []

for tag in repo.tags:
    tag = str(tag)

    if validateTag(tag):
        tagl = parseTag(tag)

        version = tagl[0]
        filenames = tagl[1:]
        filename = checkIfSourceFileExists(filenames, ext)

        if filename != False and checkIfVersionExists(filenames, version, 'pdf'):
            print(version)
            print(filename)
            print(tag)

            tagFile = tag + '.' + ext

            os.system('git checkout tags/'+tag)

            cwd = os.getcwd()

            if filename[2] is not '':
                os.chdir(filename[2])

            copyfile(filename[1], tagFile)
            addVersion(tagFile, version)
            generateLatexFile(tagFile)
            os.remove(tagFile)

            doneList.append("%s -> %s" % (tag, tagFile))

            os.chdir(cwd)

            os.system('git checkout publish')
            os.system('git add -f *.pdf')
            os.system('git commit -m "Robot build for tag: %s"' % tag)
            os.system('git clean -f')
            os.system('git push origin publish')

print("Generated %s versions" % len(doneList))
print("")
for done in doneList:
    print(done)

