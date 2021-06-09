import os
import sys
import io
from distutils import sysconfig
assert(os.name == 'nt')
diDir2 = os.path.sep.join(
    [os.path.dirname(sys.executable), 'Lib', 'distutils'])
if not os.path.exists(diDir2+'\\distutils.cfg'):
    with io.open(diDir2+'\\distutils.cfg', 'w') as cfgFile:
        print('creating distutils.cfg file')
        cfgFile.write('''[build]
compiler = mingw32
\n[build_ext]
compiler = mingw32''')

cached = []
needPatch = False
with io.open(diDir2+'\\cygwinccompiler.py', 'r') as cygpy:
    print('check cygwinccompiler config.')

    for line2 in cygpy.readlines():
        if "elif msc_ver == '1600'" in line2:
            cached.append(line2.replace("elif msc_ver == '1600'",
                          "elif int(msc_ver) >= 1600"))
            print('need patched...')
            needPatch = True
        else:
            cached.append(line2)

if needPatch:
    with io.open(diDir2+'\\cygwinccompiler.py', 'w') as cygpy:
        cygpy.writelines(cached)
    print('patch done')

cached = []
needPatch = True
with io.open(sysconfig.get_python_inc()+'\\pyconfig.h', 'r') as pyconfigh:
    print('check pyconfig.h patched.')
    for line2 in pyconfigh.readlines():
        if '//Patch for mingw32 compiler begin. version 0.1.0' in line2:
            needPatch = False
        else:
            cached.append(line2)

if needPatch:
    print('need patched...')
    with io.open(sysconfig.get_python_inc()+'\\pyconfig.h', 'w') as pyconfigh:
        pyconfigh.writelines(cached[0:2])
        pyconfigh.write('''
//Patch for mingw32 compiler begin. version 0.1.0
#ifdef __MINGW32__
  #ifdef _WIN64
    #define MS_WIN64
  #endif
#endif
//Patch for mingw32 compiler end. version 0.1.0\n''')
        pyconfigh.writelines(cached[2:])
        print('patch done')

print('done')
  
