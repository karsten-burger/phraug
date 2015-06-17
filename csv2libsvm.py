#!/usr/bin/env python

"""
Based on script from http://fastml.com/
Repository https://github.com/zygmuntz/phraug/blob/master/csv2libsvm.py.

Convert CSV file to libsvm format. Works only with numeric variables.
Put -1 as label index (argv[3]) if there are no labels in your file.
Expecting no headers. If present, headers can be skipped with argv[4] == 1.
Trailing comments beginning with # are stripped out.
Example: python csv2libsvm.py data.csv data.libsvm 0 True   # (class label/target is in 1st column, ignore one header line)
         Reads data.csv and produces data.libsvm.
"""

import sys
import csv

def construct_line( label, line ):
	new_line = []
	if float( label ) == 0.0:
		label = "0"
	new_line.append( label )
	
	for i, item in enumerate( line ):
                item = item.strip()
	        if "#" in item:
	          item = item.split('#', 1)[0].strip()   # folgenden Kommentar weglassen

		if item == '' or float( item ) == 0.0:
			continue
		new_item = "%d:%s" % ( i + 1, item )
		new_line.append( new_item )
	new_line = " ".join( new_line )
	new_line += "\n"
	return new_line

# ---

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
	label_index = int( sys.argv[3] )
except IndexError:
	label_index = 0
	
try:
	skip_headers = sys.argv[4]
except IndexError:
	skip_headers = 0	

i = open( input_file )
o = open( output_file, 'wb' )

reader = csv.reader( i )
 
if skip_headers:
	print "skip header line"
	headers = reader.next()

for line in reader:
	# ignore comment lines
	if len(line) > 0: 
	    item = line[0].strip()
	    if item[0] == "#":
	        print "ignoring: ", line
	        continue
	       
	if label_index == -1:
		label = 1
	else:
		label = line.pop( label_index )
		
	# remove trailing comments:
        #print line
	new_line = construct_line( label, line )
	o.write( new_line )
