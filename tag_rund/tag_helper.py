import glob, os

def parseTag(tag, seperator='-'):

    list = tag.split(seperator)
    version = list.pop()
    tag = seperator.join(list)
    tag2 = ' '.join(list)

    return (version, tag, tag2)


def validateTag(tag, seperator='-'):
    if tag.count(seperator) >= 1:
        return True
    return False

def checkIfSourceFileExists(filenames, extention):

    for f in filenames:
        for filename in glob.glob('**/'+f+'.'+extention, recursive=True):
            if os.path.isfile(filename):  # filter dirs
                return (f, os.path.basename(filename), os.path.dirname(filename))

    return False

def checkIfVersionExists(tag, version, extention='pdf'):

    for f in tag:
        for filename in glob.glob('**/'+f+'-'+version+'.'+extention, recursive=True):
            if os.path.isfile(filename):  # filter dirs
                return True

    return False

