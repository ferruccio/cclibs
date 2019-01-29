import os, time, shutil
from subprocess import Popen, PIPE

from script import Script
import tools, setup

def s2m(s):
    m = int((s * 10)/60)/10
    return m if m <= 10 else int(m)

def build_combo(fn, config, platform):
    print('building {0} {1} {2}...'.format(fn.__name__, config, platform))
    bat = Script(True, fn.__name__, config, platform) #build script
    fn(bat)
    bat.run()

    print('installing {0} {1} {2}...'.format(fn.__name__, config, platform))
    bat = Script(False, fn.__name__, config, platform) #istallation script
    fn(bat)
    bat.run()

def build_all(fn):
    print('=' * 60)
    print('Building {0}...'.format(fn.__name__))
    print('=' * 60)
    start = time.time()

    if setup.BUILD_DEBUG and setup.BUILD_X86:
        build_combo(fn, 'debug', 'x86')

    if setup.BUILD_RELEASE and setup.BUILD_X86:
        build_combo(fn, 'release', 'x86')

    if setup.BUILD_DEBUG and setup.BUILD_X64:
        build_combo(fn, 'debug', 'x64')

    if setup.BUILD_RELEASE and setup.BUILD_X64:
        build_combo(fn, 'release', 'x64')

    print('-' * 60)
    print('{0} complete: {1} min'.format(fn.__name__, s2m(time.time() - start)))

def ICU(bat):
    if bat.build:
        tools.extract('icu')
        bat.command('cd icu\\source\\allinone')
        bat.devenv('allinone.sln')
    else:
        bat.validate_devenv()
        bat.include('icu\\include')
        bat.bin('icu\\bin\\*.exe')
        bat.bin('icu\\bin\\*.dll', 'icu\\bin64\\*.dll')
        bat.lib('icu\\lib\\*.lib', 'icu\\lib64\\*.lib')

def BerkeleyDB(bat):
    if bat.build:
        tools.extract('bdb')
        bat.command('cd bdb\\build_windows')
        # building the .NET solution also builds native DLLs
        bat.devenv('BDB_dotNet_vs2010.sln')
    else:
        bat.validate_devenv()
        bat.include('bdb\\build_windows\\*.h')
        bat.bin('bdb\\build_windows\\AnyCPU\\{0}\\*.dll'.format(bat.config))
        bat.bin('bdb\\build_windows\\win32\\{0}\\*.dll'.format(bat.config),
                'bdb\\build_windows\\x64\\{0}\\*.dll'.format(bat.config))
        bat.lib('bdb\\build_windows\\win32\\{0}\\*.lib'.format(bat.config),
                'bdb\\build_windows\\x64\\{0}\\*.lib'.format(bat.config))

def bjam(bat):
    if bat.build:
        tools.extract('boost')
        bat.command('cd boost')
        bat.command('bootstrap.bat >bjam.log')

def Boost(bat):

    def param(config, platform):
        p = ' --hash --without-mpi toolset=msvc-{0}'.format(setup.VC_VERSION)
        p += ' -sICU_PATH={0}\\{1}'.format(setup.INSTALL, platform)
        p += ' -sZLIB_SOURCE={0}\\zlib'.format(os.getcwd())
        p += ' variant={0} link=static runtime-link=static runtime-link=shared threading=multi'.format(config)
        p += ' --prefix={0}\\{1}'.format(setup.INSTALL, platform)
        p += ' address-model={0}'.format(64 if platform=='x64' else 32)
        return p

    if bat.build:
        tools.extract('boost')
        tools.extract('zlib')
        bat.command('cd boost')
        bat.command('b2 -a {0} install'.format(param(bat.config, bat.platform)))

def clean_boost(platform):
    tools.rename('{0}\\{1}\\include\\boost-1_59\\boost'.format(setup.INSTALL, platform),
                 '{0}\\{1}\\include\\boost'.format(setup.INSTALL, platform))

def FreeType(bat):
    if bat.build:
        tools.extract('freetype')
        # add missing x64 support
        bat.command('copy /y archives\\freetype-project\\* freetype\\builds\\win32\\vc2010')
        bat.command('cd freetype\\builds\\win32\\vc2010')
        bat.devenv('freetype.sln')
    else:
        bat.validate_devenv()
        bat.command('pushd freetype\\objs\\win32\\vc2010')
        if bat.config == 'release':
            bat.command('copy /y freetype246.lib freetype.lib')
            bat.command('del freetype246.lib')
        else:
            bat.command('copy /y freetype246_d.lib freetyped.lib')
            bat.command('del freetype246_d.lib')
        bat.command('popd')
        bat.include('freetype\\include')
        bat.lib('freetype\\objs\\win32\\vc2010\\*.lib')

def libjpeg(bat):
    if bat.build:
        tools.extract('libjpeg')
        # add missing x64 support
        bat.command('copy /y archives\\jpeg-project\\* libjpeg')
        bat.command('cd libjpeg')
        bat.command('copy /y jconfig.vc jconfig.h')
        bat.devenv('jpeg.sln')
    else:
        bat.validate_devenv()
        bat.include('libjpeg\\*.h')
        bat.lib('libjpeg\\{0}\\*.lib'.format(bat.config), 'libjpeg\\x64\\{0}\\*.lib'.format(bat.config))

def zlib(bat):
    if bat.build:
        tools.extract('zlib')
        bat.command('cd zlib')
        bat.cmake()
    else:
        bat.validate_cmake()

def libpng(bat):
    if bat.build:
        tools.extract('libpng')
        bat.command('cd libpng')
        bat.cmake()
    else:
        bat.validate_cmake()

def OpenSSL(bat):
    if bat.build:
        tools.extract('openssl')
    else:
        bat.include('openssl\\include64')
        bat.lib('openssl\\lib64')
        bat.bin('openssl\\bin64')

def PoDoFo(bat):
    if bat.build:
        if not os.path.isdir('podofo'):
            os.system('svn export -r {0} {1} podofo >scripts\\svn-export.log'.format(setup.PODOFO_REV, setup.PODOFO_SVN))
        bat.command('cd podofo')
        bat.cmake({
            'target': 'podofo_static',
            'params': '-DLIBCRYPTO_LIBRARY_NAMES=libcryptoMT{0} -DPODOFO_BUILD_STATIC:TYPE=BOOL=ON'
                .format('d' if bat.config == 'debug' else ''),
        })
    else:
        bat.validate_cmake()
        bat.include('podofo\\src\\*.h', '\\podofo')
        bat.include('podofo\\podofo_config.h', '\\podofo')
        if bat.config == 'debug':
            bat.command("copy /y podofo\\src\\podofo.lib podofo\\src\\podofod.lib")
            bat.lib("podofo\\src\\podofod.lib")
        else:
            bat.lib("podofo\\src\\podofo.lib")

def need(program):
    (out, err) = Popen(['where', program], stdout=PIPE, shell=True).communicate()
    if len(out) == 0:
        raise Exception('{0} is required.'.format(program))

def main():

    need('7z')
    need('svn')
    need('perl')
    need('cmake')
    need('sed')

    start = time.time()

    tools.kill('scripts')
    os.mkdir('scripts')

    print('Setting up {0}...'.format(setup.INSTALL))
    if setup.CLEAN:
        tools.kill(setup.INSTALL)

    try:
        os.mkdir(setup.INSTALL)

        os.mkdir('{0}/x86'.format(setup.INSTALL))
        os.mkdir('{0}/x86/include'.format(setup.INSTALL))
        os.mkdir('{0}/x86/lib'.format(setup.INSTALL))
        os.mkdir('{0}/x86/bin'.format(setup.INSTALL))

        os.mkdir('{0}/x64'.format(setup.INSTALL))
        os.mkdir('{0}/x64/include'.format(setup.INSTALL))
        os.mkdir('{0}/x64/lib'.format(setup.INSTALL))
        os.mkdir('{0}/x64/bin'.format(setup.INSTALL))
    except OSError as e:
        print('warning: {0} ({1})'.format(e.strerror, e.filename))

    if setup.FRESH:
        print('Forcing a fresh rebuild...')
        tools.kill('bdb')
        tools.kill('boost')
        tools.kill('freetype')
        tools.kill('icu')
        tools.kill('libjpeg')
        tools.kill('libpng')
        tools.kill('openssl')
        tools.kill('podofo')
        tools.kill('turtle')
        tools.kill('zlib')

    if setup.BUILD_ICU:
        build_all(ICU)

    if setup.BUILD_BOOST:
        build_combo(bjam, 'release', 'x86')
        build_all(Boost)
        if setup.BUILD_X86:
            clean_boost('x86')
        if setup.BUILD_X64:
            clean_boost('x64')

    if setup.BUILD_PODOFO:
        build_all(zlib)
        build_all(libjpeg)
        build_all(libpng) # depends on zlib
        build_all(FreeType)
        build_all(OpenSSL)
        build_all(PoDoFo) # depends on zlib, libjpeg, libpng, FreeType and OpenSSL

    if setup.BUILD_BDB:
        build_all(BerkeleyDB)

    print('=' * 60)
    print('build complete: {0} min'.format(s2m(time.time() - start)))
    print('=' * 60)

if __name__ == '__main__':
    main()