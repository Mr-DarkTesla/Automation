import os
import datetime

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def FileCreation(path):
    file_name = str(datetime.datetime.now()) + '.txt'
    with open(os.path.join(path, file_name), 'w') as fp:
        fp.write('Headder')
    return file_name


# print(FileCreation(os.getcwd() + '/../RawData/'))
