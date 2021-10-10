from subprocess import Popen, PIPE, CalledProcessError
from rq import get_current_job

import shlex

def vismusic(song='song.wav',output='output.mp4',duration=2):
  print("Running vismusic")
  job = get_current_job()
   
  cmd = f'python visualize.py --song {song} --depth 0.9 --jitter 0.65 ' \
        f'--pitch_sensitivity 200 --tempo_sensitivity 0.6 ' \
        f'--classes 506 611 820 812 688 682 649 646 741 323 319 947 ' \
        f'--truncation 0.9 --smooth_factor 12 --batch_size 18 --duration {duration} --output_file {output}'  
  args = shlex.split(cmd)      
  with Popen(args, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
      print(line, end='')     

  if p.returncode != 0:
    print("Failed")
