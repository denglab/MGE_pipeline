#!/usr/bin/env python
import os,sys
from Bio import Entrez
from Bio import SeqIO
import pandas as pd
import numpy as np
from Bio import SeqUtils
Entrez.email = "me@my_institute.org"

filepath=os.path.abspath(sys.argv[1])
thread=sys.argv[2]
outpath=os.path.abspath(sys.argv[3])
currdir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
os.system('mkdir '+outpath)
os.chdir(filepath)
assembly_files = [x for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith(".fna")]
assembly_paths = [os.path.abspath(x) for x in assembly_files]
os.chdir(outpath)

os.system('mkdir Conjugation')
os.system('mv ../prokka_output/prokka_FAA .')
os.system('mv ../prokka_output/prokka_GBK .')
for faa in os.listdir('prokka_FAA'):
    faa_name=faa.split('.')[0]
    for conj_type in ['typeF', 'typeB', 'typeC', 'typeFATA', 'typeFA', 'typeG', 'typeI', 'typeT']:
        conj_name=faa_name+'_'+conj_type
        os.system(currdir+'/macsyfinder-1.0.4/bin/macsyfinder '+conj_type+' -w 20 --db-type ordered_replicon -d '+currdir+'/macsyfinder-1.0.4/data/Conjugation/DEF -p '+currdir+'/macsyfinder-1.0.4/data/Conjugation/HMM --profile-suffix .HMM --sequence-db prokka_FAA/'+faa+' -o Conjugation/'+conj_name+' >> /dev/null') # stdout is already reported in output files from macsyfinder (macsyfinder.out)

os.system('awk "NR==1||FNR>1" Conjugation/*/macsyfinder.report > Conj_results')
os.system('mkdir ../ice_sequences')

if os.stat('Conj_results').st_size > 0:
    conj = pd.read_table("Conj_results")
    conj["Replicon_name"] = conj["#Hit_Id"].apply(lambda x: x.split('_')[0])
    conj.System_Id.replace("UserReplicon", conj.Replicon_name, regex=True, inplace=1)
    record_ids = []
    for sample in conj.groupby(["Replicon_name"],sort=False):
	strain = sample[1].Replicon_name.unique()[0]
	genes = conj.loc[conj['Replicon_name']==strain]['#Hit_Id']
	gbk = SeqIO.parse("prokka_GBK/{strain}.gbk".format(strain=strain), "genbank")
	genes_dir={}
	for record in gbk:
	    for feat in record.features:
		if feat.type == 'gene':
		    if "locus_tag" in feat.qualifiers:
			locus_tag = feat.qualifiers["locus_tag"][0]
			genes_dir.update({locus_tag:record.id})
	for gene in genes:
	    record_id = genes_dir[gene]
	    record_ids.append(record_id)
    conj['Contig']=record_ids
    conj.to_csv('conjugation_results.csv',index=False)

    conj_samples = list(conj.Replicon_name.unique()[0])
    all_samples  = [x.split('.')[0] for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith(".fna")]
    noconj_samples = list(set(list(all_samples)).difference(set(conj_samples)))
    for sample in noconj_samples:
	handle_sample = open('../ice_sequences/'+sample+'_ice.fasta','w')
	handle_sample.close()

    for sample in conj.groupby("Replicon_name"):
	strain = sample[1].Replicon_name.unique()[0]
	handle = open('../ice_sequences/'+strain+'_ice.fasta','w')
	for ice in sample[1].groupby("System_Id"):
	    ice_data = ice[1]
	    ice_id = ice_data.System_Id.unique()[0]
	    for contig in ice_data.groupby("Contig"):
		contig_data = contig[1]
		contig_id = contig_data.Contig.unique()[0]
		genes = contig_data['#Hit_Id']
		gene_start = genes.iloc[0]
		gene_stop = genes.iloc[-1]
		gbk = SeqIO.parse("prokka_GBK/{strain}.gbk".format(strain=strain), "genbank")
		for record in gbk:
		    for feat in record.features:
			if "locus_tag" in feat.qualifiers:
			    locus_tag = feat.qualifiers["locus_tag"][0]
			    if feat.type == 'gene':
				if locus_tag == gene_start:
				    ice_beg = feat.location.start
				if locus_tag == gene_stop:
				    ice_end = feat.location.end
				    title= '>'+contig_id+'_'+str(ice_beg+1)+'_'+str(ice_end)+' '+ice_id.split('_',1)[-1]
				    sequence = record.seq[int(ice_beg):int(ice_end)]
		handle.write(title+'\n')
		handle.write(str(sequence)+'\n')
	handle.close()
else:
    all_samples  = [x.split('.')[0] for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith(".fna")]
    for sample in all_samples:
        handle_sample = open('../ice_sequences/'+sample+'_ice.fasta','w')
        handle_sample.close()
