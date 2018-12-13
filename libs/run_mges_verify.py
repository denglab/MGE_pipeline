import os,sys
from Bio.Blast.Applications import NcbiblastnCommandline
import pandas as pd

blast_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))+'/ncbi-blast-2.7.1+/bin'
filepath=os.path.abspath(sys.argv[1])
outpath=os.path.abspath(sys.argv[2])
threads=sys.argv[3]
perc_qcov=sys.argv[4]  # e.g., 25, coverage of the query for each hit
perc_ident=sys.argv[5]  # e.g., 75, identical percentage of each hit

os.chdir(filepath)
assembly_files = [x for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith('.fna')]
assembly_paths = [os.path.abspath(x) for x in assembly_files]

blast_fmt = "'7 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qcovhsp qlen'"
os.chdir(outpath)
csv_file='mge_matrix.csv'
df = pd.read_csv(csv_file)
mge_loc_dir_add = {}
def blastn(mge,genome):
    blastdata=mge
    genome_id = genome.split('/')[-1].split('.')[0]
    blastout=filepath+'/'+mge+'_'+genome_id+'.blastout'
    os.system(blast_dir+'/makeblastdb -in '+genome+' -dbtype nucl')
    blastn_out=NcbiblastnCommandline(cmd=blast_dir+'/blastn',query=blastdata, db=genome, evalue=1e-5,outfmt=blast_fmt,out=blastout,num_threads=threads,max_hsps=5,qcov_hsp_perc=perc_qcov,perc_identity=perc_ident)
    stdout, stderr = blastn_out()
    rmindexfiles=genome+'.*'
    os.system('rm '+rmindexfiles)

    result_blast=open(blastout,'r').readlines()
    mge_dir={}
    mge_loc_dir={}
    for i in range(0,len(result_blast)):
	line = result_blast[i]
        if line.startswith('# Query'):
	    mge_id = line.split(': ')[1].split(' ')[0]
	    mge_hit = result_blast[i+2]
	    mge_loc_dir[mge_id]=[]
	    if mge_hit.startswith('# Fields'):
		mge_dir.update({mge_id:1})
		num_hit = result_blast[i+3].split(' ')[1]
		for j in range(1,int(num_hit)+1):
		    line_hit = result_blast[i+3+j]
		    hit_contig = line_hit.split('\t')[1].split('|')[2]
		    hit_sample = hit_contig.split('_')[0]
		    hit_loc = ':'.join(sorted([line_hit.split('\t')[8],line_hit.split('\t')[9]]))
		    verified_hit = hit_sample+','+hit_contig+','+hit_loc
		    mge_loc_dir[mge_id].append(verified_hit)
	    else:
		mge_dir.update({mge_id:0})
    for key in sorted(mge_dir.keys(),key=lambda mgeID: int(mgeID.split('_')[1])):
        if df.loc[df["Sample"]==genome_id, key].values[0] == 0:
	    df.loc[df["Sample"]==genome_id, key] = mge_dir[key]
	    if mge_dir[key] == 1:
		if key in mge_loc_dir_add.keys():
		    mge_loc_dir_add[key].append(';'.join(mge_loc_dir[key]))
		else:
		    mge_loc_dir_add[key]=[]
		    mge_loc_dir_add[key].append(';'.join(mge_loc_dir[key]))
    return df,mge_loc_dir_add

for mge in ['insertion','ice','integron','prophage']:
    mge_file=mge+'_representatives.fasta'
    for assembly_path in assembly_paths:
        blastn(mge_file,assembly_path)
df.to_csv("mge_matrix_verified.csv", index=False)

'''
mge_output = open('mge_blast.txt','r')
handle = open('mge_blast_verified.txt','w')
for line in mge_output:
    line=line.strip()
    if line.split('\t')[0] == 'mge_id':
	handle.write(line+'\t'+'samples_blast'+'\n')
    else:
	mge_id = line.split('\t')[0]
	if mge_id in mge_loc_dir_add.keys():
	    mge_sample = '||'.join(mge_loc_dir_add[mge_id])
	    handle.write(line+'\t'+mge_sample+'\n')
	else:
	    handle.write(line+'\n')
handle.close()
'''
