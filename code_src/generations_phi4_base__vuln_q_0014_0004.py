from flask import Flask, abort

app = Flask(__name__)

@app.route('/restricted')
def restricted():
    abort(403)

if __name__ == '__main__':
    app.run()