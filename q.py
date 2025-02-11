import redis
from runmodel import vismusic

from rq import Queue
from rq.job import Job

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

conn=redis.Redis()
q = Queue(connection=conn)

app = Flask(__name__, static_url_path="", static_folder="output")
	
@app.route('/visjob', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      print("Received request.")
      f = request.files['file']
      f.save(secure_filename(f.filename))      
      job = q.enqueue(vismusic, connection=conn, job_timeout='35m', kwargs={
            'song': f.filename,
            'duration': request.form['duration'],
            'pitch': request.form['pitch'],
            'depth': request.form['depth'],
            'classes': request.form['classes'],
            'tempo': request.form['tempo'],
            'truncate': request.form['truncate'],
            'smooth': request.form['smooth'], 
            'jitter': request.form['jitter'],                                  
            'output': 'output/'+f.filename+'.mp4'
          })
      print("Added job.")
      print(job)
      job.meta['fname'] = f.filename+'.mp4'
      job.save_meta()
      return job.id
      
@app.route('/jobstatus', methods = ['GET'])
def jobstatus():
    print("Job status request id=", request.args.get('id'))
    job = Job.fetch(request.args.get('id'), connection=conn)
    print('Status: %s' % job.get_status())
    num = len(q.jobs)
    return {'fname':job.meta['fname'], 'started': job.enqueued_at, 
            'status':job.get_status(), 'jobs':num}
		
if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')


