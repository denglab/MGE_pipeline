#!usr/bin/env python

import sys,os
import pandas as pd

filepath=os.path.abspath(sys.argv[1])
mgetype=sys.argv[2]
threads=sys.argv[3]
os.chdir(filepath)
fa_pool=mgetype+'_pool.fasta'
os.system('cat *'+mgetype+'.fasta > '+fa_pool)
os.system('vsearch --notrunclabels --maxseqlength 200000 --sortbylength '+fa_pool+' --output '+fa_pool.replace('.fasta','_sorted.fasta'))
os.system('vsearch -cluster_fast '+fa_pool.replace('.fasta','_sorted.fasta')+' -strand both -id 0.75 -centroids '+fa_pool.replace('.fasta','_representatives.fasta')+' --notrunclabels --relabel '+mgetype+'_ --relabel_keep --qmask none --maxseqlength 200000 --threads '+threads+' --clusterout_id --otutabout '+fa_pool.replace('.fasta','_cluster.tab'))
os.system('cp '+fa_pool.replace('.fasta','_representatives.fasta ')+'../'+mgetype+'_representatives.fasta')

fa_ids = [x.split('_')[0] for x in os.listdir(filepath) if x.endswith(mgetype+'.fasta')]
l = len(fa_ids)
df = pd.read_table(fa_pool.replace('.fasta','_cluster.tab'),index_col=0, header=0)
c = len(list(df.index))
cluster_dir={}
cluster_list=[]
for mge_id in list(df.index):
  cluster_list.append(mge_id)
  a=df.loc[mge_id] != 0
  mge_list=list(a[a==True].index)
  sample_list=[item.split('_')[0] for item in mge_list]
  cluster_dir[mge_id] = sample_list
cluster_list = sorted(cluster_list,key=lambda mgeID: int(mgeID.split('_')[1]))
cluster_list.insert(0,'Sample')
mat = [ [ 0 for i in range(c+1) ] for j in range(l) ]
j=0
for fa in fa_ids:
  mat[j][0]=fa
  for key in sorted(cluster_dir.keys(),key=lambda mgeID: int(mgeID.split('_')[1])):
    if fa in cluster_dir[key]:
      mat[j][int(key.split('_')[1])]=1
  j+=1
handle=open(mgetype+'_matrix.csv','w')
handle.write(','.join(cluster_list)+'\n')
for row in mat:
  handle.write(','.join([str(x) for x in row])+'\n')
handle.close

