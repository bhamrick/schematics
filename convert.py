#!/usr/bin/env python
from os import system, popen2
from string import replace
import sys

inname=sys.argv[1]
outname=sys.argv[2]

fin = open(inname,'r')
fout = open(outname,'w')

llx = 999999
lly = 999999
uux = -999999
uuy = -999999

cstdin, cstdout = popen2('pwd')
PREFIX=cstdout.read()[:-1]

symlist={}
id = 0

outstr = '''\
1 -1 scale
/mov {
	/y 2 1 roll def
	/x 2 1 roll def
	x y translate
} def

/rot {
	/r 2 1 roll def
	r rotate
} def

/unmov {
	x -1 mul y -1 mul translate
} def

/unrot {
	r -1 mul rotate
} def

/wire {
	newpath
	moveto
	lineto
	stroke
} def

/gnd {
	mov
	rot
	newpath
	-18 0 moveto
	18 0 lineto
	0 18 lineto
	closepath
	stroke
	unrot
	unmov
} def
'''

def load_sym(s):
	global PREFIX, outstr, symlist, id
	s = replace(s,'\\','/')
	slx = 999999
	sly = 999999
	sux = -999999
	suy = -999999
	if symlist.has_key(s):
		return
	print s
	fsym = open(PREFIX+'/sym/'+s+'.asy','r')
	symstr = '/sym%d {\n\tmov\n\trot\n' % id
	lines = fsym.read().split('\n')
	fsym.close()
	for l in lines:
		li = l.split()
		if len(li)==0:
			continue
		if li[0]=='LINE':
			symstr+='\tnewpath\n'
			symstr+='\t%d %d moveto\n' % (int(li[2]),int(li[3]))
			symstr+='\t%d %d lineto\n' % (int(li[4]),int(li[5]))
			symstr+='\tstroke\n'
			if int(li[2]) < slx:
				slx = int(li[2])
			if int(li[3]) < sly:
				sly = int(li[3])
			if int(li[4]) < slx:
				slx = int(li[4])
			if int(li[5]) < sly:
				sly = int(li[5])
			if int(li[2]) > sux:
				sux = int(li[2])
			if int(li[3]) > suy:
				suy = int(li[3])
			if int(li[4]) > sux:
				sux = int(li[4])
			if int(li[5]) > suy:
				suy = int(li[5])
		elif li[0]=='CIRCLE':
			cx = (int(li[2])+int(li[4]))/2
			cy = (int(li[3])+int(li[5]))/2
			symstr+='\tnewpath\n'
			symstr+='\t%d %d %d 0 360 arc\n' % (cx, cy, int(li[2])-cx)
			symstr+='\tstroke\n'
			if int(li[2]) < slx:
				slx = int(li[2])
			if int(li[3]) < sly:
				sly = int(li[3])
			if int(li[4]) < slx:
				slx = int(li[4])
			if int(li[5]) < sly:
				sly = int(li[5])
			if int(li[2]) > sux:
				sux = int(li[2])
			if int(li[3]) > suy:
				suy = int(li[3])
			if int(li[4]) > sux:
				sux = int(li[4])
			if int(li[5]) > suy:
				suy = int(li[5])
	symstr+='\tunrot\n\tunmov\n} def\n'
	symlist[s]=(id,slx,sly,sux,suy)
	outstr+=symstr
	id+=1

def use_sym(s,x,y,r):
	global symlist, outstr, id, llx, lly, uux, uuy
	load_sym(s)
	s = replace(s,'\\','/')
	sid, slx, sly, sux, suy = symlist[s]
	if r == 0:
		if x + slx < llx:
			llx = x + slx
		if x + sux > uux:
			uux = x + sux
		if y + sly < lly:
			lly = y + sly
		if y + suy > uuy:
			uuy = y + suy
	if r == 90:
		if x + sly < llx:
			llx = x + sly
		if x + suy > uux:
			uux = x + suy
		if y - sux < lly:
			lly = y - sux
		if y - slx > uuy:
			uuy = y - slx
	if r == 180:
		if x - sux < llx:
			llx = x - sux
		if x - slx > uux:
			uux = x - slx
		if y - suy < lly:
			lly = y - suy
		if y - sly > uuy:
			uuy = y - sly
	if r == 270:
		if x - suy < llx:
			llx = x - suy
		if x - sly > uux:
			uux = x - sly
		if y + slx < lly:
			lly = y + slx
		if y + sux > uuy:
			uuy = y + sux
	outstr+='%d %d %d sym%d\n' % (r,x,y,sid)

lines = fin.read().split('\n')
fin.close()
for l in lines:
	li = l.split()
	if len(li) == 0:
		continue
	if li[0]=='WIRE':
		outstr+='%d %d %d %d wire\n' % (int(li[1]),int(li[2]),int(li[3]),int(li[4]))
		if int(li[1]) < llx:
			llx = int(li[1])
		if int(li[2]) < lly:
			lly = int(li[2])
		if int(li[3]) < llx:
			llx = int(li[3])
		if int(li[4]) < lly:
			lly = int(li[4])
		if int(li[1]) > uux:
			uux = int(li[1])
		if int(li[2]) > uuy:
			uuy = int(li[2])
		if int(li[3]) > uux:
			uux = int(li[3])
		if int(li[4]) > uuy:
			uuy = int(li[4])
	elif li[0]=='SYMBOL':
		use_sym(li[1],int(li[2]),int(li[3]),int(li[4][1:]))
	elif li[0]=='FLAG':
		if li[3]=='0':
			outstr+='0 %d %d gnd\n' % (int(li[1]),int(li[2]))
			if int(li[1])-18 < llx:
				llx = int(li[1])-18
			if int(li[1])+18 > uux:
				uux = int(li[1])+18
			if int(li[2]) < lly:
				lly = int(li[2])
			if int(li[2])+18 > uuy:
				uuy = int(li[2])+18
outstr = ('%%!\n%%%%BoundingBox %d %d %d %d\n' % (llx-3,-uuy-3,uux+3,-lly+3)) + outstr
fout.write(outstr)
fout.close()
