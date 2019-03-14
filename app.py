from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
	
@app.route('/method',methods = ['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return f'{request.method}' 
	
@app.route('/show/<json>',methods = ['GET', 'POST'])
def show(json):
    return json.json()

	
if __name__ == '__main__':
    app.run(debug=True)