import os
import struct
import platform

from cffi import FFI

ffibuilder = FFI()
# arch = "%s-%s" % (os.uname().sysname, os.uname().machine)
uname = platform.uname()


if uname.system == "Windows":
    if struct.calcsize("P") * 8 == 64:
        libdir = "./lib64"
    else:
        libdir = "./lib32"
elif uname.system == "Darwin":
    if uname.machine == "x86_64":
        libdir = "/Users/runner/work/_temp/install/lib"
    else:
        libdir = "/usr/local/lib"
else:
    libdir = "/usr/local/lib"


ffibuilder.set_source(
    "curl_cffi._wrapper",
    """
        #include "shim.h"
    """,
    libraries=["curl-impersonate-chrome"] if uname.system != "Windows" else ["libcurl"],
    library_dirs=[libdir],
    source_extension=".c",
    include_dirs=[
        os.path.join(os.path.dirname(__file__), "include"),
        os.path.join(os.path.dirname(__file__), "ffi"),
    ],
    sources=[
        os.path.join(os.path.dirname(__file__), "ffi/shim.c"),
    ],
    extra_compile_args=(
        ["-Wno-implicit-function-declaration"] if uname.system == "Darwin" else []
    ),
    # extra_link_args=["-Wl,-rpath,$ORIGIN/../libcurl/" + arch],
)

with open(os.path.join(os.path.dirname(__file__), "ffi/cdef.c")) as f:
    cdef_content = f.read()
    ffibuilder.cdef(cdef_content)


if __name__ == "__main__":
    ffibuilder.compile(verbose=False)
