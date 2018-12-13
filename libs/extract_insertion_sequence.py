import os, sys

fastapath=os.path.abspath(sys.argv[1])
outpath=os.path.abspath(sys.argv[2])
filepath=os.path.abspath(sys.argv[3])
os.system('mkdir '+outpath)

os.chdir(fastapath)
is_files = [x for x in os.listdir(fastapath) if x.endswith("is.fna")]
is_paths = [os.path.abspath(x) for x in is_files]

is_samples = [x.split('_')[0] for x in os.listdir(fastapath) if x.endswith("is.fna")]
all_samples  = [x.split('.')[0] for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith(".fna")]
nois_samples = list(set(list(all_samples)).difference(set(is_samples)))
os.chdir(outpath)
for sample in nois_samples:
    handle_sample = open(outpath+'/'+sample+'_insertion.fasta','w')
    handle_sample.close()

for is_path in is_paths:
  filestr=os.path.split(is_path)[1]
  fname=filestr.split('.')[0]
  infile = open (is_path,'r')
  outhandle = open (outpath+'/'+fname+'_insertion.fasta','w')
  for line in infile:
    if line.startswith('>'):
      newline='>'+line.split('|',2)[-1]
      outhandle.write(newline)
    else:
      outhandle.write(line)
  outhandle.close()

