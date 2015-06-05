# =================================================================================
#    This file is part of pipeVFX.
#
#    pipeVFX is a software system initally authored back in 2006 and currently 
#    developed by Roberto Hradec - https://bitbucket.org/robertohradec/pipevfx
#
#    pipeVFX is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pipeVFX is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with pipeVFX.  If not, see <http://www.gnu.org/licenses/>.
# =================================================================================


class python(baseApp):
    '''
    WARNING: in newer debian/ubuntu distros, we need this to make things work correctly:
        sudo ln -s /usr/lib/python2.7/config-x86_64-linux-gnu/ /usr/lib/python2.7/config
    
    when python complains it cant open config/Makefile!
    '''
    def environ(self):
        parent = self.parent()
        # force the system libraries to be preloaded since we have OIIO and OCIO 
        # compiled with the system libraries. 
        # we have to remove this once OIIO and OCIO are properly build with the pipe gcc!
        self['LD_PRELOAD'] = pipe.base.findSharedLibrary("libstdc++.so.6")
        self['LD_PRELOAD'] = pipe.base.findSharedLibrary("libgcc_s.so.1")

        self['PYTHON_VERSION_MAJOR'] = pipe.apps.version.get('python')[:3]
        
#        if self.parent() not in ['houdini']:

        # if nuke version < 8.0 or gaffer, force to load our libpython shared lib
        sharedLib = self.path('lib/libpython$PYTHON_VERSION_MAJOR.so.1.0')
        if os.path.exists(sharedLib):
            if (self.parent()=='nuke' and float(pipe.version.get('nuke')[:3])<8) or self.parent() in ['gaffer']:
                self['LD_PRELOAD'] = sharedLib 

       
        # set PYTHONHOME for some apps...
        if self.parent() in ['python','delight','houdini','cortex']:
            self['PYTHONHOME'] = self.path()
            
        if self.parent() in ['python']:
            # initialize cortex environment so we can load its modules.
            self.update( cortex() )
            self.update( gaffer() )

            # also, initialize buildStuff in case theres some pythonmodules there.
            self.update( buildStuff() )

            # also, initialize wx 
            self.update( wxpython() )

        else:            
            self.update( qube() )

        

    def bins(self):
        return [('python', 'python')]
