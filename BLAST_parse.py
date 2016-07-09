#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio.Blast import NCBIXML
import re
import csv
import sys

dummyList = [("cp102", "Mmus"),("spd901", "Hsap"),("cp102", "Mmus"),("cp984", "Mmus")]

print dummyList
#-----------------------------------------------------------------------------
# Filter accession list
#-----------------------------------------------------------------------------
def filter_species(listOfTuples, shortSpecies):
	filtered = []
	for each in listOfTuples:
		if each[1] == shortSpecies:
			filtered.append(each)
	output = filter_duplicates(filtered)
	return output

def filter_duplicates(list):
	noDups = list(set(list))
	return noDups

#-----------------------------------------------------------------------------
# Given input file, give a csv of IDs
#-----------------------------------------------------------------------------
# First argument is the path to the XML file from a remote BLAST search, second
# is an e value threshold below which results from the BLAST search will be discarded,
# third is the name of the file to write the accessions to, and fourth is the name of the
# file to send the file names of processed BLAST searches to.

def get_ids(input, ethresh = 0.01, outfile1 = "outfile.csv"):
	eValueThresh = 0.01
	n = 1
	result = open(input) # mode omitted defaults to read only
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	hits = []
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < eValueThresh:
				stamp = '\n[[ * * * * Record No.' + str(n) + ' * * * * ]]'
				print stamp
				n += 1
				title = alignment.title
				mdata = re.match( r'.*[A-Z|a-z]{2,3}\|(.*?)\|.*?\[([A-Z])\S* ([A-Z|a-z]{3}).*\].*?', title)
				if mdata is not None:
					accession = re.match(r'([A-Z|a-z|_|0-9]*)\..*', mdata.group(1))
					acc = str(accession.group(1))
					genus = str(mdata.group(2)[0])
					species = str(mdata.group(3)[:3])
					shortSpecies = (genus + species)
					hits.append((acc, shortSpecies))
		print ".\n.\n.\n."
	spec = input[15:19]
	print "\n\n\nFiltering for: " + spec + "\n\n\n"
	filteredHits = filter_results(hits,spec)
	# Saving results
	with open(outfile1,'a') as csvfile:
		blasthits = csv.writer(csvfile)
		for each in filteredHits:
			blasthits.writerow([each[0]])		
	csvfile.close()

#-----------------------------------------------------------------------------
# Parse a series of files
#-----------------------------------------------------------------------------
def parse_files():
		with open("results\\filenames.txt",'r') as csvfile:
			reader = csv.reader(csvfile)
			files = list(reader)
			for filename in files:
				get_ids(filename)
		csvfile.close()
		with open(outfile1,'r') as csvfile2:
			read = csv.read(csvfile2)
			accs = list(read)
			filt = filter_duplicates(accs)
		csvfile2.close()
		with open("results\\accessionmaster.csv","r") as csvfile3:
			write = csv.write(csvfile3, "w")
			for each in filt:
				write.writerow([filt])
		

#-----------------------------------------------------------------------------
# Actually run the shit
#-----------------------------------------------------------------------------
# When running this script from the console, one argument is required: the name
# of the BLAST search output file

parse_files()

#get_ids(sys.argv[1])
	

