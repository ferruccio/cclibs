Deprecated in favor of [vcpkg](https://github.com/Microsoft/vcpkg).

cclibs
======

Python script to build a set of C++ libraries on Windows

This script can build the following libraries for use in Windows C++ programs.

- Boost
- BerkeleyDB
- ICU
- PoDoFo
- OpenSSL
- zlib
- FreeType
- libjpeg
- libpng

It can build any combination of Debug, Release, x86 & x64 configurations.

Requirements
------------

- Visual C++ (tested with VS2010, VS2012 & VS2013)
- Python3 (tested with 3.3)
- Perl (OpenSSL only)
- CMake
- Command line tools
  - svn (PoDoFo only)
  - 7z (7-Zip)
  - sed (GnuWin32, etc.)

Setup
-----
Edit `setup.py` to control which libraries/configurations are built.

You will need to hunt down and place the following files in the `archives` directory:

- `boost_1_59_0.7z`
- `db-5.3.21.zip`
- `ft246.zip`
- `icu4c-55_1-src.zip`
- `jpegsr8c.zip`
- `lpng166.7z`
- `openssl-1.0.1e.tar.gz`
- `zlib127.zip`

You only need to do this for the libraries you actually want to build but keep in mind the following dependencies:
- Boost (requires ICU, zlib)
- PoDoFo (requires FreeType, libjpeg, libpng, OpenSSL, zlib)
- libpng (requires zlib)

Note: PoDoFo is actually fetched directly from its svn repo.

All libraries are built to be statically linked and use the static C/C++ runtime library.

Run `build.py` and if all goes well, you'll have a set of libraries ready to go. A complete rebuild of every library configuration takes about three hours on my 3Ghz Core i5 box running Windows 7 x64 with 8GB.

If you're wondering why I picked these libraries - it's because I'm actually using them in a project.
I am hoping that someday NuGet will make all this nonsense obsolete.
