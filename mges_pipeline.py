#!/usr/bin/env python

# example: ./mges_pipeline.py -i test_genomes/ -o mge_output/ -t 8 -c 90 -p 90
import argparse,os,sys

def main():
  parser = argparse.ArgumentParser(usage='mges_pipeline.py -i <assembily_path> -o <output_path> -t <threads> -c <minimum_coverage> -p <minimum_ident>')
  parser.add_argument("-i",help="<string>: input assemblies")
  parser.add_argument("-o",help="<string>: output directory")
  parser.add_argument("-t",help="<string>: threads")
  parser.add_argument("-c",default=90,help="<int>: minimum coverage of each hit for MGE verification, default 90")
  parser.add_argument("-p",default=90,help="<int>: minimum identical percentage of each hit for MGE verification, default 90")
  args=parser.parse_args()
  dirpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
  input_dir = os.path.abspath(args.i)
  output_dir = os.path.abspath(args.o)
  thread = args.t
  qcov=args.c
  ident=args.p

  os.system('mkdir '+output_dir)
  os.chdir(output_dir)
  print "Running Prokka for genome annotation..."
  os.system("python2.7 "+dirpath+"/libs/run_prokka.py "+input_dir+' '+thread+' prokka_output >> run_prokka.log 2>&1')
  os.system('mv prokka_output/prokka_fna ./')
  print "Submitting genomes to PHAST web server..."
  os.system("python2.7 "+dirpath+"/libs/run_phaster_submit.py prokka_fna  phaster_output >> run_phaster.log 2>&1")
  print "Running ISEScan for detection of insertion sequences..."
  os.system("python2.7 "+dirpath+"/libs/run_isescan.py prokka_fna "+thread+" isescan_output >> run_isescan.log 2>&1")
  print "Running Integron Finder for detection of integrons..."
  os.system("python2.7 "+dirpath+"/libs/run_IntegronFinder2_virtualenv.py prokka_fna "+thread+" integron_output >> run_integron.log 2>&1")
  print "Running CONJScan for detection of ICEs..."
  os.system("python2.7 "+dirpath+"/libs/run_conjscan.py prokka_fna "+thread+" conjscan_output >> run_conjscan.log 2>&1")
  print "Downloading results of prophage detection from PHAST web server..."
  os.system("python2.7 "+dirpath+"/libs/run_phaster_download.py phaster_output 60 >> run_phaster.log 2>&1")
  os.system("python2.7 "+dirpath+"/libs/extract_insertion_sequence.py isescan_output/prediction/prokka_fna insertion_sequences prokka_fna >> extract_sequences.log 2>&1")
  os.system("python2.7 "+dirpath+"/libs/extract_prophage_sequence.py phaster_output prokka_fna prophage_sequences >> extract_sequences.log 2>&1")
  print "Running clustering for insertion sequences..."
  os.system("python2.7 "+dirpath+"/libs/run_mges_cluster.py insertion_sequences insertion "+thread+" >> run_mges_cluster.log 2>&1")
  print "Running clustering for integron sequences..."
  os.system("python2.7 "+dirpath+"/libs/run_mges_cluster.py integron_sequences integron "+thread+" >> run_mges_cluster.log 2>&1")
  print "Running clustering for prophage sequences..."
  os.system("python2.7 "+dirpath+"/libs/run_mges_cluster.py prophage_sequences prophage "+thread+" >> run_mges_cluster.log 2>&1")
  print "Running clustering for ICE sequences..."
  os.system("python2.7 "+dirpath+"/libs/run_mges_cluster.py ice_sequences ice "+thread+" >> run_mges_cluster.log 2>&1")
  os.system('(head -n 1 prophage_sequences/prophage_matrix.csv && tail -n +2 prophage_sequences/prophage_matrix.csv | sort -V) > prophage_matrix_sorted.csv')
  os.system('(head -n 1 insertion_sequences/insertion_matrix.csv && tail -n +2 insertion_sequences/insertion_matrix.csv | sort -V) > insertion_matrix_sorted.csv')
  os.system('(head -n 1 integron_sequences/integron_matrix.csv && tail -n +2 integron_sequences/integron_matrix.csv | sort -V) > integron_matrix_sorted.csv')
  os.system('(head -n 1 ice_sequences/ice_matrix.csv && tail -n +2 ice_sequences/ice_matrix.csv | sort -V) > ice_matrix_sorted.csv')
  os.system('join -a1 -t , prophage_matrix_sorted.csv ice_matrix_sorted.csv | join -a1 -t , - insertion_matrix_sorted.csv | join -a1 -t , - integron_matrix_sorted.csv > mge_matrix.csv')
  print "Running BLAST verification for detected MGE sequences..."
  os.system("python2.7 "+dirpath+"/libs/run_mges_blast.py "+output_dir+' '+thread+' '+output_dir+' 80 80 >> run_mges_blast.log 2>&1')
  os.system("python2.7 "+dirpath+"/libs/run_mges_verify.py prokka_fna . "+thread+" "+qcov+" "+ident+" >> run_mges_verify.log 2>&1")
  os.system("python2.7 "+dirpath+"/libs/run_mges_gff.py .")
  os.system("python2.7 "+dirpath+"/libs/run_mges_dist.py mge_matrix_verified.csv")
  os.system("mkdir log")
  os.system("mv *.log log")
  os.system("rm *blastout")
  os.system("rm prokka_fna/*blastout")
  os.system("for x in *_matrix_sorted.csv;do mv $x ${x%_matrix_sorted.csv}_sequences; done")
  os.system("for x in *_representatives.fasta;do mv $x ${x%_representatives.fasta}_sequences.fasta; done")
  os.system("mv mge_matrix_verified.csv mge_matrix.csv")
  os.system("mv mge_blast_verified.txt mge_blast.txt")
  os.system('for x in prokka_fna/*fna; do s=$(basename ${x%.fna}); cat prophage_sequences/$s"_prophage.gff" insertion_sequences/$s"_insertion.gff" ice_sequences/$s"_ice.gff" integron_sequences/$s"_integron.gff" > $s"_MGE.gff";done')
  os.system("mkdir MGE_gff")
  os.system("mv *.gff MGE_gff")
  print "Done!"

if __name__ == '__main__':
  main()
