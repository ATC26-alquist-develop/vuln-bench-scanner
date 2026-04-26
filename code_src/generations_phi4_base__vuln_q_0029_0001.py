from flask import Flask, render_template, request, jsonify
   from flask_socketio import SocketIO, emit
   import subprocess
   import yaml

   app = Flask(__name__)
   socketio = SocketIO(app)

   # Load configuration from a YAML file
   with open('config.yaml', 'r') as file:
       config = yaml.safe_load(file)

   @app.route('/')
   def index():
       return render_template('index.html')

   @socketio.on('run_command')
   def handle_command(data):
       command = data['command']
       try:
           result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           emit('command_result', {'result': result.stdout.decode('utf-8'), 'error': result.stderr.decode('utf-8')})
       except subprocess.CalledProcessError as e:
           emit('command_result', {'result': '', 'error': str(e)})

   if __name__ == '__main__':
       socketio.run(app, debug=True)