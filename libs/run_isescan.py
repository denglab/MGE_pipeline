import sys,os

filepath=os.path.abspath(sys.argv[1])
thread=sys.argv[2]
outpath=os.path.abspath(sys.argv[3])
os.system('mkdir '+outpath)
currdir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

os.chdir(filepath)
assembly_files = [x for x in os.listdir(filepath) if x.endswith(".fasta") or x.endswith('.fna')]
assembly_paths = [os.path.abspath(x) for x in assembly_files]
os.chdir(outpath)

for assembly_path in assembly_paths:
    filestr=os.path.split(assembly_path)[1]
    filename=filestr.split('.')[0]
    os.system('python3 isescan.py '+assembly_path+' isescan_proteome isescan_hmm')
