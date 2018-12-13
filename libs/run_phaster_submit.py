import os,sys,json

filepath=os.path.abspath(sys.argv[1])
outpath=os.path.abspath(sys.argv[2])
os.system('mkdir '+outpath)

os.chdir(filepath)
assembly_files = [x for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith('.fna')]
assembly_paths = [os.path.abspath(x) for x in assembly_files]
os.chdir(outpath)

for assembly_path in assembly_paths:
  filestr=os.path.split(assembly_path)[1]
  filename=filestr.split('.')[0]
  os.system('wget --post-file='+assembly_path+' http://phaster.ca/phaster_api?contigs=1 -O '+filename+'.phaster')

