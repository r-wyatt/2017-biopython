#-----------------------------------------------------------------------------
# Clustalw run and read
#-----------------------------------------------------------------------------
''' This code requires that biopython is installed (as well as, obviously, python). 
Not tested for version 3 of python, so it will probably break.

Cite trimal:


Edit the filenames below:			'''

infile = "align.aln"
outfile = "trimAlign.aln"


#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio import AlignIO
from Bio import Phylo
from StringIO import StringIO
import subprocess
import os.path
import sys
import os
import re

#-----------------------------------------------------------------------------
# Function to use trimal to trim alignment
#-----------------------------------------------------------------------------
def trim_align(alignpath,outpath):
	cmd = ['trimal', '-in', alignpath, '-out', outpath, "-automated1"]
	process = subprocess.Popen(cmd)
	process.wait()
	print('\nDone trim\n')
#-----------------------------------------------------------------------------
# Functions to condense fasta names before saving as phylip
#-----------------------------------------------------------------------------
def trim_fasta_names(alignpath, input):
	no_ext = re.sub(r'\.[A-Za-z]{3}', "", input)
	print no_ext
	outname = no_ext + "Rename.aln"
	stdout_bak = sys.stdout
	sys.stdout = open(os.path.join(alignpath, outname),"w")
	for line in open(os.path.join(alignpath, input)):
		line = re.sub(r'\>([A-Za-z]{1})[A-Za-z]{3} (\S*)', r'>\1\2', line)
		s = line[0] + line[1].lower() + line[2:]
		print s,
	sys.stdout = stdout_bak
	format_converter(sys.argv[1],outname,"phylip-relaxed")
	
def format_converter(alignpath, input, output_style):
	alignment = AlignIO.read(os.path.join(alignpath,input), "fasta")
	AlignIO.write(alignment,os.path.join(alignpath,"transfomed.phy"),output_style)
	

#-----------------------------------------------------------------------------
# Flow control
#-----------------------------------------------------------------------------
dir = sys.argv[1] # First argument is the master directory name

inpath = os.path.join(dir,infile)
outpath = os.path.join(dir,outfile)

trim_align(dir,infile)
trim_fasta_names(dir,outfile)




