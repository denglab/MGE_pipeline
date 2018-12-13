import os,sys
import pandas as pd

inputf = sys.argv[1] #mge_matrix_verified.csv

def compare(List1,List2):
  n = 0
  if len(List1)==len(List2):
    for i in range(0,len(List1)):
      if List1[i]==List2[i]:
        pass
      else:
        n+=1
  return n

df = pd.read_csv(inputf,index_col=0, header=0)
samples = list(df.index)
matrix = pd.DataFrame(0, index = samples, columns = samples)
for i in range(0,len(samples)):
  for j in range(0,len(samples)):
    sam_i = samples[i]
    sam_j = samples[j]
    row_i = list(df.loc[sam_i].values)
    row_j = list(df.loc[sam_j].values)
    dist = compare(row_i,row_j)
    matrix[sam_i][sam_j]=dist
matrix.to_csv('mge_dist_matrix.csv')
