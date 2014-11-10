"""
IPC pipes tracker for current user processes
	by Adam Balawender, Nov 10 2014
"""
from __future__ import print_function
import os, re
proc = '/proc'
uid  = os.getuid()
print( 'Processes you can follow IPC pipes of are: (uid: %i)' % uid )
pattern = r'flags:\s*([0-9]+)'

pids = [pid for pid in os.listdir(proc) if pid.isdigit() and\
				uid == os.stat( os.path.join( proc, pid, 'fd' ) ).st_uid ]

readingPipes, writingPipes, processes = dict(), dict(), dict()
for pid in pids:
    try:
	processes[pid] = open(os.path.join(proc, pid, 'cmdline')).read().split('\0')[0]
	links = [ (os.readlink(os.path.join(proc, pid, 'fd', link)), re.search( pattern, open(os.path.join(proc, pid, 'fdinfo', link)).read() ) )
						    for link in os.listdir(os.path.join(proc, pid, 'fd')) ]
	links = [ (int(link[0][6:-1]), int(link[1].expand(r'\1'))%4)
			    for link in links if link[0].startswith('pipe:') and link[1]]	# cannot expand unmatched regex
	for l in links:
	    if l[1]:	writingPipes[ l[0] ] = pid
	    else:	readingPipes[ l[0] ] = pid
    except OSError:
	pass

for k,i in writingPipes.iteritems():
	if readingPipes.has_key(k):
		print('%30s -> %30s via %i ' % (processes[i], processes[readingPipes[k]], k) )
