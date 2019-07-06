# !/usr/bin/env hython
# -*- coding: utf-8 -*-

import os
import sys


#for n in range(5):
#	os.system("pkill -fc -9 mantra")

from optparse import OptionParser

import parsers.hbatch

import hou

parser = OptionParser(usage="usage: %prog [options] hip_name rop_name", version="%prog 1.0")
parser.add_option('-s', '--start', dest='start', type='float', help='Start frame number.')
parser.add_option('-e', '--end', dest='end', type='float', help='End frame number.')
parser.add_option('-b', '--by', dest='by', type='float', help='Frame increment.')
parser.add_option('-t', '--take', dest='take', type='string', help='Take name.')
parser.add_option('-o', '--out', dest='output', type='string', help='Output file.')
parser.add_option('--diskfile', dest='diskfile', type='string', help='Set to generate this file only.')
parser.add_option('--numcpus', dest='numcpus', type='int', help='Number of CPUs.')
parser.add_option('-i', '--ignore_inputs', action='store_true', dest='ignore_inputs', default=False, help='Ignore inputs')

options, args = parser.parse_args()

rop = []
if len(args) < 2:
    parser.error('At least one of mandatory rop_name or hip_name argument is missed.')
elif len(args) > 2:
    parser.error('Too many arguments provided.')
else:
    hip = args[0]
    rop = args[1]

start = options.start
end = options.end
by = options.by
take = options.take
diskfile = options.diskfile
numcpus = options.numcpus
output = options.output
ignoreInputs = options.ignore_inputs
# print ignore_inputs

# Loading HIP file, and force HIP variable:
force_hip = True  # not sure, we need to force HIP variable.
# May be this code is obsolete
if force_hip:
    envhip = os.path.abspath(hip)
    envhip = os.path.dirname(envhip)

    if os.name != 'nt':
        envhip = envhip.replace('\\\\', '/')  # for nt //server/share/path is
        # the only one way

    envhip = envhip.replace('\\', '/')  # houdini always use unix-like path
    os.environ['HIP'] = envhip
    hou.allowEnvironmentToOverwriteVariable('HIP', True)
    hou.hscript('set HIP=' + envhip)

# Note that we ignore all load warnings.
try:
    hou.hipFile.load(hip)
except hou.LoadWarning:
    pass
# hou.hipFile.load( hip, True)

if force_hip:
    hou.hscript('set HIPNAME=%s' % os.path.basename(hip))
    hou.hscript('set HIP=%s' % envhip)
    print('HIP set to "%s"' % envhip)

# Establish ROP to be used
if rop[0] != '/':
    rop = '/out/' + rop

ropnode = hou.node(rop)

if ropnode is None:
    raise hou.InvalidNodeName(rop + ' rop node wasn`t found')

# Trying to set ROP to block until render comletes
# block = ropnode.parm('soho_foreground')
# if block != None:
# value = block.eval()
# if value != None:
# if value != 1:
# try:
# block.set( 1)
# except:
# print 'Failed to set node blocking.'

drivertypename = ropnode.type().name()

if drivertypename == 'ifd':

    # Set ROP to generate diskfile:
    if diskfile is not None:
        ropnode.parm('soho_outputmode').set(1)
        ropnode.parm('soho_diskfile').set(diskfile)
    else:
        # Trying to variate number of CPUs if needed:
        if numcpus is not None:
            paramcmd = ropnode.parm('soho_pipecmd')
            if paramcmd is not None:
                command = paramcmd.eval()
                if command is not None:
                    print('Trying to set mantra threads to %s' % numcpus)
                    command = command.replace(
                        'mantra',
                        'mantra -j %s' % numcpus,
                        1
                    )
                    try:
                        paramcmd.set(command)
                        print('   Command changed to:')
                        print(command)
                    except:
                        print('Failed, number of mantra theads not changed.')

        # Trying to set ROP verbose level:
        verbose = ropnode.parm('vm_verbose')
        if verbose is not None:
            value = verbose.eval()
            if value is not None:
                if value < 1:
                    print('Trying to set "Verbose Level" to 1 on mantra')
                    try:
                        verbose.set(1)
                    except:
                        print('Failed, frame verbose not available.')

        # Trying to set ROP to output progress
        progress = ropnode.parm('vm_alfprogress')
        if progress is not None:
            value = progress.eval()
            if value is not None:
                if value != 1:
                    print('Trying to set "Alfred Style Progress" on mantra')
                    try:
                        progress.set(1)
                    except:
                        print('Failed, frame progress not available.')

elif drivertypename == 'rib':

    # Trying to set ROP to output progress
    progress = ropnode.parm('soho_pipecmd')
    if progress is not None:
        command = progress.eval()
        if command is not None:
            if command.find('-progress') == -1:
                print('Trying to set "-progress" on prman')
                command = command.replace('prman', 'prman -progress', 1)
                try:
                    progress.set(command)
                except:
                    print('Failed, frame progress not available.')
elif drivertypename == "wedge":
    ropnode.parm('wrange').set(1)
    ropnode.parm('wedgenum').set(start)
    driverpath = ropnode.parm('driver').eval()
    driver = ropnode.node(driverpath)
    if driver:
        for parmName in ["vm_alfprogress", "alfprogress"]:
            progress = driver.parm(parmName)
            if progress:
                progress.set(1)

if take is not None and len(take) > 0:
    hou.hscript('takeset ' + take)

# If end wasn't specified, render single frame
if end is None:
    end = start

# If by wasn't specified, render every frame
if by is None:
    by = 1

render_output = None
if output is not None and len(output) > 0:
    render_output = output

frame = start
while frame <= end:
    render_range = (frame, frame, by)
    print(parsers.hbatch.keyframe + str(frame))
    for p in ropnode.parms():
        if os.path.exists( os.path.dirname( p.evalAsString() ) ):
            print(p.name(), p.evalAsString())
            print( "WRITING FILE: "+p.evalAsString())
    sys.stdout.flush()
    ropnode.render(
        frame_range=render_range,
        output_file=render_output,
        method=hou.renderMethod.FrameByFrame,
        ignore_inputs=ignoreInputs
    )
    frame += by
