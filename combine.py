#!/usr/bin/env python

import sys, pprint
from pybtex.database.input import bibtex
from pybtex.backends.plaintext import Backend
from StringIO import StringIO



def mostCompleteOf(rec1, rec2):
    s1 = str(rec1)
    s2 = str(rec2)
    if len(s1) > len(s2):
	return (rec1, rec2)
    else:
	return (rec2, rec1)

def mergeFile(currbt, remainder, fn):
    parser = bibtex.Parser()
    abc = open(fn).read()
    xxx = StringIO(abc.decode('utf-8', 'ignore'))
    bib_data = parser.parse_stream(xxx)
    for k, entry in  bib_data.entries.items():
	if entry.key in currbt:
	    (currbt[entry.key], other) = mostCompleteOf(currbt[entry.key], entry)
	    remainder.append(other)
	else:
	    currbt[entry.key] = entry

    return (currbt, remainder)

def writeBibTex(fn, bt):

    with open(fn, "w") as outf:
	for e in bt:
	    partlist = []
	    out = ""
	    print "Writing %s to %s" % (e.key, fn)
	    for persontype, personlist in e.persons.items():
		partlist.append("%s = {%s}" % (persontype, " and ".join([unicode(x) for x in personlist])))
	    for k,v in e.fields.items():
		    partlist.append("%s = {%s}" % (k, v))

	    out += "@%s{%s" % (e.type, e.key)
	    if len(partlist) > 0:
		out += ",\n"
		out += ",\n".join(["    %s" % x for x in partlist])
	    out += "\n}\n\n"
	    outf.write(out.encode('utf-8'))

allbibtex = {}
remainder = []

for arg in sys.argv[1:]:
    (allbibtex, remainder) = mergeFile(allbibtex, remainder, arg)

writeBibTex("merged.bib", allbibtex.values())
writeBibTex("duplicates.bib", remainder)
