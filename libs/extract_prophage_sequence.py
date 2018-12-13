#!/usr/bin/env python

import sys,os
from Bio import SeqIO

filepath=os.path.abspath(sys.argv[1])
fastapath=os.path.abspath(sys.argv[2])
outpath=os.path.abspath(sys.argv[3])
os.system('mkdir '+outpath)

os.chdir(filepath)
phage_files = [x for x in os.listdir(filepath) if x.endswith(".phaster.txt")]
phage_paths = [os.path.abspath(x) for x in phage_files]

os.chdir(fastapath)
assembly_files = [x for x in os.listdir(fastapath) if x.endswith(".fasta") or x.endswith(".fna")]
assembly_paths = [os.path.abspath(x) for x in assembly_files]
os.chdir(outpath)
for phage_path in phage_paths:
    filestr=os.path.split(phage_path)[1]
    filename=filestr.split('.')[0]
    phage=open(phage_path,'r')
    assembly_path= [x for x in assembly_paths if x.split('/')[-1].split('.')[0] == filename][0]
    assembly=SeqIO.index(assembly_path,'fasta')
    handle=open(outpath+'/'+filename+'_prophage.fasta','w')
    phage_lines = [x for x in phage if 'intact(' in x]
    for line in phage_lines:
	line = '\t'.join(line.split())
	phageID = line.split('\t')[4]
        contigID=phageID.split(':')[0]
        pos_beg=phageID.split(':')[1].split('-')[0]
        pos_end=phageID.split(':')[1].split('-')[1]
        sequence=assembly[contigID].seq[int(pos_beg)-1:int(pos_end)]
        handle.write('>'+contigID.split('|')[-1]+'_'+pos_beg+'_'+pos_end+'\n')
        handle.write(str(sequence)+'\n')
    handle.close()

