# Visual C++ version
#
# VS2010 -> VC++ 10.0
# VS2012 -> VC++ 11.0
# VS2013 -> VC++ 12.0
VC_VERSION = '12.0'

# installation target
INSTALL = 'C:\\cclibs-12.0'

# delete INSTALL target before build?
CLEAN = True

# delete source directories before build?
# i.e. force unpacking from archives
FRESH = True

# build ICU?
BUILD_ICU = True

# build BerkeleyDB
BUILD_BDB = True

# build Boost
BUILD_BOOST = True

# build PoDoFo and all its dependencies
BUILD_PODOFO = True

# PoDoFo SVN revision (use 'HEAD' to get latest)
PODOFO_REV = 1649

# configuration
BUILD_DEBUG = True
BUILD_RELEASE = True

# platform
BUILD_X86 = False
BUILD_X64 = True

# map dependency to archive file
ARCHIVES = {
    'boost' : 'boost_1_56_0.7z',
    'bdb' : 'db-5.3.21.zip',
    'freetype' : 'ft246.zip',
    'icu' : 'icu4c-52_1-src.zip',
    'libjpeg' : 'jpegsr8c.zip',
    'libpng' : 'lpng166.7z',
    'openssl' : 'openssl-1.0.1e.tar.gz',
    'zlib' : 'zlib127.zip'
}