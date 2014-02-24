import os, glob

import setup

def extract(dir, nth=0):
    file = setup.ARCHIVES[dir]
    if os.path.isdir(dir):
        print('directory: {0} already exists'.format(dir))
    else:
        if file.endswith('.tar.gz'):
            os.system('7z x archives\\{0} -y >nul'.format(file))
            file = file[:-3]
            print('extracting {0} to {1}...'.format(file, dir))
            os.system('7z x {0} -o{1} -y >nul'.format(file, dir))
            kill(file)
        else:
            print('extracting {0} to {1}...'.format(file, dir))
            os.system('7z x archives\\{0} -otmp -y >nul'.format(file, dir))
            tmp = glob.glob('tmp\\*')[nth]
            rename(tmp, dir)
            kill('tmp')

def kill(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.system('del /q {0}'.format(path))
        elif os.path.isdir(path):
            os.system('rd /s /q {0}'.format(path))

def rename(old, new):
    tries = 0
    while tries < 10:
        try:
            kill(new)
            os.rename(old, new)
            tries = 10
        except OSError as e:
            print('warning: failed to rename {0} to {1} ({2})'.format(old, new, e.strerror))
            tries += 1
