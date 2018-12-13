import os,sys

path=os.path.abspath(sys.argv[1])
mge_file = open(path+'/mge_blast_verified.txt','r')
mge_tab = mge_file.readlines()
mge_dic = {'insertion':'ISEScan','ice':'CONJscan','integron':'Integron finder','prophage':'Phaster'}

def mge_gff(mgetype,mgepath):
  os.chdir(path+'/'+mgepath)
  samples = [x.split('_')[0] for x in os.listdir(path+'/'+mgepath) if x.endswith('_'+mge+'.fasta') or x.endswith('.fna')]
  for sample in samples:
    handle = open(sample+'_'+mgetype+'.gff','w')
    for line in mge_tab:
      if line.startswith(mge):
	line=line.strip()
	cluster_id = line.split('\t')[0]
	f = line.split('\t')[13]
	for rec in f.split('||'):
	  rec_id = rec.split(',')[0]
	  rec_contig = rec.split(',')[1]
	  rec_start = rec.split(',')[2].split(':')[0]
	  rec_stop = rec.split(',')[2].split(':')[1]
	  if rec_id == sample:
	    handle.write(rec_contig+'\t'+mge_dic[mgetype]+'\t'+mgetype+'\t'+rec_start+'\t'+rec_stop+'\t.\t.\t.\tcluster_id "'+cluster_id+'"; length "'+str(int(rec_stop)-int(rec_start)+1)+'" \n')
	if len(line.split('\t'))==15:
	  v = line.split('\t')[14]
	  for recv in v.split('||'):
            rec_v_id = recv.split(',')[0]
	    for rec_v in recv.split(';'):
              rec_v_contig = rec_v.split(',')[1]
	      rec_v_loc = [int(rec_v.split(',')[2].split(':')[0]),int(rec_v.split(',')[2].split(':')[1])]
              rec_v_start = min(rec_v_loc)
              rec_v_stop = max(rec_v_loc)
              if rec_v_id == sample:
                handle.write(rec_v_contig+'\t'+'Blast'+'\t'+mgetype+'\t'+str(rec_v_start)+'\t'+str(rec_v_stop)+'\t.\t.\t.\tcluster_id "'+cluster_id+'"; length "'+str(rec_v_stop-rec_v_start+1)+'"\n')
    handle.close()

def mge_len(mgetype,mgepath):
  os.chdir(path+'/'+mgepath)
  samples = [x for x in os.listdir(path+'/'+mgepath) if x.endswith('_'+mge+'.gff')]
  handle = open(mgetype+'_length.csv','w')
  handle.write('sample,'+mgetype+'\n')
  for sample in samples:
    sampleID = sample.split('_')[0]
    mge_gff = open(sample,'r')
    n = 0
    for line in mge_gff:
        line = line.strip()
        m = line.split('length ')[-1].strip('"')
	n += int(m)
    handle.write(sampleID+','+str(n)+'\n')
  handle.close()

for mge in ['insertion','ice','integron','prophage']:
  mgep = mge+'_sequences'
  mge_gff(mge,mgep)
  mge_len(mge,mgep)

os.chdir(path)
os.system('(head -n 1 prophage_sequences/prophage_length.csv && tail -n +2 prophage_sequences/prophage_length.csv | sort -V) > prophage_length_sorted.csv')
os.system('(head -n 1 insertion_sequences/insertion_length.csv && tail -n +2 insertion_sequences/insertion_length.csv | sort -V) > insertion_length_sorted.csv')
os.system('(head -n 1 integron_sequences/integron_length.csv && tail -n +2 integron_sequences/integron_length.csv | sort -V) > integron_length_sorted.csv')
os.system('(head -n 1 ice_sequences/ice_length.csv && tail -n +2 ice_sequences/ice_length.csv | sort -V) > ice_length_sorted.csv')
os.system("join -a1 -t , prophage_length_sorted.csv insertion_length_sorted.csv| join -a1 -t , - ice_length_sorted.csv | join -a1 -t , - integron_length_sorted.csv > mge_length_tmp.csv")

f = open('mge_length_tmp.csv','r')
mge_csv = f.readlines()
handle_mges = open('mge_length.csv','w')
handle_mges.write(mge_csv[0].strip()+',total\n')
for line in mge_csv[1:]:
  line=line.strip()
  total=sum([int(x) for x in line.split(',')[1:]])
  handle_mges.write(line+','+str(total)+'\n')
handle_mges.close()
os.system('rm mge_length_tmp.csv *length_sorted.csv')
