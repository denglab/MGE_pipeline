import os,sys,json
import time

filepath=os.path.abspath(sys.argv[1])
wait=int(sys.argv[2]) # default 60 seconds
os.chdir(filepath)
phaster_files = [x for x in os.listdir(filepath) if x.endswith(".phaster")]
for phaster_file in phaster_files:
  job = json.load(open(phaster_file,'r'))['job_id']
  phaster_out = phaster_file+'.out'
  os.system('wget http://phaster.ca/phaster_api?acc='+job+' -O '+phaster_out)
  status = json.load(open(phaster_out,'r'))['status']
  while status != 'Complete':
    if 'submissions ahead of yours' in status:
      time.sleep(wait*3*int(status.split(' ')[0]))
      os.system('wget http://phaster.ca/phaster_api?acc='+job+' -O '+phaster_out)
      status = json.load(open(phaster_out,'r'))['status']
    else:
      time.sleep(wait*3)
      os.system('wget http://phaster.ca/phaster_api?acc='+job+' -O '+phaster_out)
      status = json.load(open(phaster_out,'r'))['status']
  f = open(phaster_out,'r')
  s = json.load(f)
  handle = open(phaster_file+'.txt','w')
  print phaster_file+': '+status
  handle.write(s['summary'])
  handle.close()
