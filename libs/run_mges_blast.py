#!/usr/bin/env python

import sys,os
from Bio import SeqIO
from Bio.Seq import Seq
import pandas as pd

blast_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))+'/ncbi-blast-2.7.1+/bin'
filepath=os.path.abspath(sys.argv[1])
thread = sys.argv[2]
outpath=os.path.abspath(sys.argv[3])
os.system('mkdir '+outpath)
dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
dbpath = dirpath.replace('libs','databases')
qcov=sys.argv[4]  # default 80, coverage of the query for each hit
ident=sys.argv[5]  # default 80, identical percentage of each hit

def mge_sum(inputf):
    mge_dir={}
    if os.stat(inputf).st_size > 0:
        df = pd.read_table(inputf,index_col=0, header=0)
	for mge_id in list(df.index):
	    a=df.loc[mge_id] != 0
	    mge_list=list(a[a==True].index)
	    sample_list=[item.split('_')[0]+','+item.split('_')[0]+'_'+item.split('_')[1]+','+item.split('_')[2]+':'+item.split('_')[3] for item in mge_list]
	    mge_dir[mge_id] = '||'.join(sample_list)
    return mge_dir

blast_fmt = "'6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovhsp qlen'"
os.chdir(outpath)
if os.stat('insertion_representatives.fasta').st_size > 0:
    os.system(blast_dir+'/blastn -query insertion_representatives.fasta -db '+dbpath+'/ISfinder_insertion_042018.fna -evalue 1e-5 -outfmt '+blast_fmt+' -max_hsps 1 -num_alignments 1 -qcov_hsp_perc '+qcov+' -perc_identity '+ident+' -num_threads '+thread+' -out insertion_representatives_ISfinder.blastout >> run_mges_blast.log 2>&1')
if os.stat('integron_representatives.fasta').st_size > 0:
    os.system(blast_dir+'/blastn -query integron_representatives.fasta -db '+dbpath+'/INTEGRALL_integron_052018.fna -evalue 1e-5 -outfmt '+blast_fmt+' -max_hsps 1 -num_alignments 1 -qcov_hsp_perc '+qcov+' -perc_identity '+ident+' -num_threads '+thread+' -out integron_representatives_INTEGRALL.blastout >> run_mges_blast.log 2>&1')
if os.stat('ice_representatives.fasta').st_size > 0:
    os.system(blast_dir+'/blastn -query ice_representatives.fasta -db '+dbpath+'/ICEberg_ices_052018.fna -evalue 1e-5 -outfmt '+blast_fmt+' -max_hsps 1 -num_alignments 1 -qcov_hsp_perc '+qcov+' -perc_identity '+ident+' -num_threads '+thread+' -out ice_representatives_ICEberg.blastout >> run_mges_blast.log 2>&1')
if os.stat('prophage_representatives.fasta').st_size > 0:
    os.system(blast_dir+'/blastn -query prophage_representatives.fasta -db '+dbpath+'/PHAST_prophage_DNA_fragment_032018.fna -evalue 1e-5 -outfmt '+blast_fmt+' -max_hsps 1 -num_alignments 1 -qcov_hsp_perc '+qcov+' -perc_identity '+ident+' -num_threads '+thread+' -out prophage_representatives_PHAST.blastout >> run_mges_blast.log 2>&1')

handle_mge = open('mge_blast.txt','w')
handle_mge.write('mge_id\tmge_name\talignment_identity\talignment_length\tquery_start\tquery_end\ttarget_start\ttarget_end\tquery_coverage\tquery_length\tsource\tmge_type\tmge_db\tsamples\n')

for item in [['insertion','ISfinder','ISEScan'],['integron','INTEGRALL','Integron finder'],['ice','ICEberg','CONJscan'],['prophage','PHAST','Phaster']]:
    mge_type=item[0]
    mge_db=item[1]
    mge_tool=item[2]
    mge_type_dir = mge_sum(filepath+'/'+mge_type+'_sequences/'+mge_type+'_pool_cluster.tab')
    if os.stat(mge_type+'_representatives.fasta').st_size > 0:
        mge_blast_file = open(mge_type+'_representatives_'+mge_db+'.blastout','r')
	mge_tab = mge_blast_file.readlines()
        mge_fasta = open(mge_type+'_representatives.fasta','r')
        mge_title = [x.strip().replace('>','') for x in mge_fasta if x.startswith('>')]
	mge_id_all = [x.split(' ')[0] for x in mge_title]
	mge_id_blast = [x.split('\t')[0] for x in mge_tab]
        for line in mge_tab:
	    line = line.strip()
            mge_name = line.split('\t')[0]
            mge_samples = mge_type_dir[mge_name]
            handle_mge.write(line.split('\t')[0]+'\t'+line.split('\t')[1].replace(':','')+'\t'+line.split('\t')[2]+'\t'+line.split('\t')[3]+'\t'+line.split('\t')[6]+'\t'+line.split('\t')[7]+'\t'+line.split('\t')[8]+'\t'+line.split('\t')[9]+'\t'+line.split('\t')[12]+'\t'+line.split('\t')[13]+'\t'+mge_tool+'\t'+mge_type+'\t'+mge_db+'\t'+mge_samples+'\n')
	for mge_id in mge_id_all:
            if mge_id not in mge_id_blast:
		mge_line = [x for x in mge_title if x.split(' ')[0] == mge_id]
		mge_len = int(mge_line[0].split('_')[4].split(' ')[0])-int(mge_line[0].split('_')[3])+1
		mge_samples = mge_type_dir[mge_id]
                handle_mge.write(mge_id+'\tNA\tNA\tNA\tNA\tNA\tNA\tNA\tNA\t'+str(mge_len)+'\t'+mge_tool+'\t'+mge_type+'\t'+'not found in '+mge_db+'\t'+mge_samples+'\n')
handle_mge.close()
os.system('(head -n 1 mge_blast.txt && tail -n +2 mge_blast.txt | sort -V) > mge_blast_sorted.txt')
os.system('mv mge_blast_sorted.txt mge_blast.txt')
