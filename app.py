from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/method', methods=['GET', 'POST', 'PUT', 'DELETE'])
def method():
    return f'{request.method}'


@app.route('/show_data', methods=['POST'])
def show():
    # json = request.args.get('json')
    json = request.get_json()
    return str(json).replace("\'", "\"")


if __name__ == '__main__':
    app.run(debug=True)
