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
      print("ID and filename =", f.filename)
      job = q.enqueue(vismusic, connection=conn, id=f.filename, kwargs={
            'song': f.filename,
            'duration': request.form['duration'],
            'output': 'output/'+f.filename+'o.mp4'
          })
      print("Added job.")
      print(job)
      return 'ok'
      
@app.route('/jobstatus', methods = ['GET'])
def jobstatus():
    print("Job status request id=", request.args.get('id'))
    job = Job.fetch(request.args.get('id'), connection=conn)
    print('Status: %s' % job.get_status())
    num = len(q.jobs)
    return {'started': job.enqueued_at, 'status':job.get_status(), 'jobs':num}
		
if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0')


