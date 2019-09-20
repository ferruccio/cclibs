# Visual C++ version
#
# VS2010 -> VC++ 10.0
# VS2012 -> VC++ 11.0
# VS2013 -> VC++ 12.0
VC_VERSION = '12.0'

# installation target
INSTALL = 'C:\\cclibs'

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
BOOST_INCLUDE = 'boost-1_69'

# build PoDoFo and all its dependencies
BUILD_PODOFO = True

# PoDoFo SVN revision (use 'HEAD' to get latest)
PODOFO_SVN = "https://svn.code.sf.net/p/podofo/code/podofo/trunk"
PODOFO_REV = 1998

# configuration
BUILD_DEBUG = True
BUILD_RELEASE = True

# platform
BUILD_X86 = False
BUILD_X64 = True

# map dependency to archive file
ARCHIVES = {
    'boost' : 'boost_1_69_0.7z',
    'bdb' : 'db-5.3.21.zip',
    'freetype' : 'ft246.zip',
    'icu' : 'icu4c-55_1-src.zip',
    'libjpeg' : 'jpegsr8c.zip',
    'libpng' : 'lpng166.7z',
    'openssl' : 'openssl-1.1.0f-vs2013.7z',
    'zlib' : 'zlib128.zip'
}