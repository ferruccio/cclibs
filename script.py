from subprocess import Popen, PIPE, STDOUT
import os

import setup

class Script:

    def __init__(self, build, name, config, platform):
        self.build = build
        self.name = name
        self.config = config
        self.platform = platform
        self.script = ''
        self.command('@echo off')
        if build:
            self.command('set CMAKE_PREFIX_PATH={0}\\{1}'.format(setup.INSTALL, platform))
            self.vcvars()

    def command(self, cmd):
        self.script += cmd + '\n'

    def basename(self, force_build=False):
        suffix = 'build' if force_build or self.build else 'install'
        return '{0}\\scripts\\{1}-{2}-{3}-{4}'.format(os.getcwd(), self.name, self.config, self.platform, suffix)

    def run(self):
        batchfile = self.basename() + '.bat'
        with open(batchfile, 'w') as bat:
            print(self.script, file=bat)
        with open(self.basename() + '.log', 'w') as log:
            proc = Popen(batchfile, stdout=PIPE, stderr=STDOUT, universal_newlines=True, shell=True)
            while True:
                line = proc.stdout.readline()
                print(line, file=log, end='')
                if len(line) == 0:
                    return

    def vcvars(self):
        pf = os.environ["PROGRAMFILES(x86)"]
        bat = '{0}\\Microsoft Visual Studio {1}\\VC\\vcvarsall.bat'.format(pf, setup.VC_VERSION)
        if not os.path.isfile(bat):
            raise Exception('vcvarsall.bat not found')
        self.command('call "{0}" {1}'.format(bat, self.platform))

    def devenv(self, sln):
        self.command('devenv "{0}" /upgrade'.format(sln))
        self.command('devenv "{0}" /rebuild "{1}|{2}"'.format(sln, self.config, 'win32' if self.platform=='x86' else self.platform))

    def cmake(self, opt={}):

        def cmake_params(config, platform, params):
            fixed = '-Wno-dev -C "{0}\\BuildSetup.cmake" . {1}'.format(os.getcwd(), params)
            return '{0} -DCMAKE_BUILD_TYPE={1} "-DCMAKE_INSTALL_PREFIX:PATH={2}\\{3}"'.format(fixed, config, setup.INSTALL, platform)

        target = opt.get('target', 'install')
        params = opt.get('params', '')
        gen = opt.get('gen', 'NMake Makefiles')

        self.command('del /q CMakeCache.txt')
        self.command('rd /s /q CMakeFiles')
        self.command('cmake {0} -G "{1}"'.format(cmake_params(self.config, self.platform, params), gen))
        self.command('cmake --build . --target {0} --clean-first'.format(target))

    def validate(self, match):
        with open(self.basename(True) + '.log') as log:
            for line in log:
                if match in line:
                    return
        raise Exception('build failed: name={0} config={1} platform={2}'.format(self.name, self.config, self.platform))

    def validate_devenv(self):
        self.validate('succeeded, 0 failed,')

    def validate_cmake(self):
        self.validate('[100%]')

    def dest(self, path):
        return '{0}\\{1}\\{2}'.format(setup.INSTALL, self.platform, path)

    def header(self, title):
        self.command('echo +----------------------------------------------')
        self.command('echo ^| {0}'.format(title))
        self.command('echo +----------------------------------------------')

    def include(self, path, dir=''):
        self.header('installing include...')
        src = '{0}\\{1}'.format(os.getcwd(), path)
        self.command('xcopy /s /i /f /y "{0}" "{1}"'.format(src, self.dest('include' + dir)))

    def bin(self, path32, path64=None):
        if path64 == None:
            path64 = path32
        self.header('installing bin...')
        src = '{0}\\{1}'.format(os.getcwd(), path32 if self.platform == 'x86' else path64)
        self.command('xcopy /s /i /f /y "{0}" "{1}"'.format(src, self.dest('bin')))

    def lib(self, path32, path64=None):
        if path64 == None:
            path64 = path32
        self.header('installing lib...')
        src = '{0}\\{1}'.format(os.getcwd(), path32 if self.platform == 'x86' else path64)
        self.command('xcopy /s /i /f /y "{0}" "{1}"'.format(src, self.dest('lib')))
