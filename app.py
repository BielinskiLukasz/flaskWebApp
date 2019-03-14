from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
	
@app.route('/method',methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return f'{request.method}' 
	
@app.route('/show_data/<uuid>', methods=['GET', 'POST'])
def show(uuid):
    content = request.get_json(silent=True)
    return uuid

	
if __name__ == '__main__':
    app.run(debug=True)