#!/usr/bin/env python

import sys,os
from Bio import SeqIO
import pandas as pd

filepath=os.path.abspath(sys.argv[1])
thread=sys.argv[2]
outpath=os.path.abspath(sys.argv[3])
os.system('mkdir '+outpath)
os.system('mkdir integron_sequences')
os.chdir(filepath)
assembly_files = [x for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith('.fna')]
assembly_paths = [os.path.abspath(x) for x in assembly_files]
os.chdir(outpath)
for filepath in assembly_paths:
    filestr=os.path.split(filepath)[1]
    filename=filestr.split('.')[0]
    assembly=SeqIO.index(filepath,'fasta')
    handle=open('../integron_sequences/'+filename+'_integron.fasta','w')
    os.system('integron_finder  --local-max --func-annot --cpu '+thread+' '+filepath)
    summary='Results_Integron_Finder_'+filename+'/'+filename+'.summary'
    integron_file='Results_Integron_Finder_'+filename+'/'+filename+'.integrons'
    if os.path.isfile(summary):
        integron_sum = pd.read_table(summary)
        integron_complete = integron_sum[integron_sum['complete']==1]
        integron_table = pd.read_table(integron_file)
        for index, row in integron_complete.iterrows():
            contigID=row['ID_replicon']
            integronID=row['ID_integron']
            integron = integron_table[(integron_table['ID_replicon']==contigID)&(integron_table['ID_integron']==integronID)]
            pos_beg=integron.iloc[0]['pos_beg']
            pos_end=integron.iloc[-1]['pos_end']
            sequence=assembly[contigID].seq[int(pos_beg)-1:int(pos_end)]
            handle.write('>'+contigID.split('|')[-1]+'_'+str(pos_beg)+'_'+str(pos_end)+'\n')
            handle.write(str(sequence)+'\n')
    handle.close()

