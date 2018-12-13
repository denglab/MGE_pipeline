#!/usr/bin/env python

import os,sys

indir = sys.argv[1]
threads = sys.argv[2]
outdir = sys.argv[3]
currdir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

activate_this_file = currdir+"/Integron_Finder2/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))
os.system('python '+currdir+'/run_integron_finder2.py '+indir+' '+threads+' '+outdir)
