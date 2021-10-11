from subprocess import Popen, PIPE, CalledProcessError
from rq import get_current_job

import shlex

# depth 0.9
# jitter 0.65
#pitch sensitity 200
#tempo sensitivity 0.6
#trunaction 0.9
#smooth factor 12
#classes

def vismusic(song='song.wav',output='output.mp4',duration=2,pitch=200,tempo=0.6,
             truncate=0.9,smooth=12,classes=None, depth=0.9, jitter=0.65):
  print("Running vismusic")
  job = get_current_job()
   
  cmd = f'python visualize.py --song {song} --depth {depth} --jitter {jitter} ' \
        f'--pitch_sensitivity {pitch} --tempo_sensitivity {tempo} ' \
        f'--truncation {truncate} --smooth_factor {smooth} --batch_size 18 --duration {duration} --output_file {output} '  
  if classes != None:
    cmd += f'--classes "{classes}"' \

  args = shlex.split(cmd)      
  with Popen(args, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
      print(line, end='')     

  if p.returncode != 0:
    print("Failed")
