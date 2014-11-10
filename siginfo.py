"""
SIGBLK mask getter for current user processes
	by Adam Balawender, Nov 10 2014
"""
from __future__ import print_function
import os, re, signal
proc = '/proc'
uid  = os.getuid()
print( 'Your processes (uid: %i)' % uid )
pattern = r'SigBlk:\s*([0-9a-f]+)'

signals = dict((getattr(signal, n), n) \
    for n in dir(signal) if n.startswith('SIG') and '_' not in n )

pids = [pid for pid in os.listdir(proc) if pid.isdigit() and uid == os.stat( os.path.join( proc, pid ) ).st_uid]
for pid in pids:
	if uid != os.stat( os.path.join( proc, pid ) ).st_uid:
		continue
	try:
		cmdline = open( os.path.join( proc, pid, 'cmdline' )).read().replace('\0', ' ')
		status = open( os.path.join( proc, pid, 'status' )).read()
		
		match = re.search(pattern, status)
		if not match: continue
		sigblk = match.expand(r'\1')
		
		print(str(pid) + '\t| ' + cmdline + " | ", end='')
		sig = int(sigblk, 16)
		s = ", ".join ( [signals.get(i+1) for i in range( 8 )\
						if sig & 1<<i and signals.get(i+1) ] )
		print(s)
		
	except IOError:
		pass
