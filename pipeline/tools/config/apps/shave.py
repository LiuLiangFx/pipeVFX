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


class shave(baseApp):
    def environ(self):
        # configure maya plugin/scripts/icons
        maya.addon ( self,
            plugin = self.path('maya$MAYA_VERSION/modules/JoeAlter/shaveHaircut/plug-ins'),
            script = self.path('maya$MAYA_VERSION/modules/JoeAlter/shaveHaircut/scripts'),
            icon   = [
                self.path('maya$MAYA_VERSION/modules/JoeAlter/shaveHaircut/icons'),
                self.path('maya$MAYA_VERSION/icons'),
            ],
            preset = self.path('maya$MAYA_VERSION/presets'),
            renderDesc = self.path('mtoadeploy/$MAYA_VERSION/'),
        )

        self['LD_LIBRARY_PATH'] = self.path('maya$MAYA_VERSION/lib')
        self['LD_LIBRARY_PATH'] = self.path('maya$MAYA_VERSION/mentalray/lib/')
        self['LD_LIBRARY_PATH'] = self.path('maya$MAYA_VERSION/vray/vrayplugins/')
        
    def license(self):
        self['RLM_LICENSE'] = "%s/licenses/shave/%s/joealter.lic" % (roots.tools(), self.version())
    



