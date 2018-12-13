#!/usr/bin/env python

import sys,os
import re

filepath=os.path.abspath(sys.argv[1])
thread=sys.argv[2]
outpath=os.path.abspath(sys.argv[3])
dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

#proteins=dirpath.replace('libs','databases')+'/ISfinder_insertion_042018.faa'
#hmms=dirpath.replace('libs','hmm_db')+'/Resfams.hmm'
os.system('mkdir '+outpath)

os.chdir(filepath)
assembly_files = [x for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith(".fna")]
assembly_paths = [os.path.abspath(x) for x in assembly_files]
os.chdir(outpath)
os.system('mkdir prokka_gbk')
os.system('mkdir prokka_fna')
os.system('mkdir prokka_faa')
for assembly_path in assembly_paths:
    filestr=os.path.split(assembly_path)[1]
    filename=re.split(r'[_.]',filestr)[0]
    outdir=filename+'_prokka'
    os.system('prokka --mincontiglen 1 --force --kingdom Bacteria --addgenes --centre Prokka --locustag '+filename+' --prefix '+filename+' --outdir '+outdir+' --cpus '+thread+' '+assembly_path)
os.system('cp *_prokka/*.fna prokka_fna')
os.system('cp *_prokka/*.gbk prokka_gbk')
os.system('cp *_prokka/*.faa prokka_faa')
