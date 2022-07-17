

from msilib.schema import Error
from flask import Flask, jsonify, request
from predictor import predict

PORT = 9806
LOCALHOST = '127.0.0.1'

app = Flask(__name__)



@app.route('/')
def hello():
    return jsonify('hello world')


@app.route('/predict', methods=['POST'])
def predictor():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            response = predict(data['input'])
            print('Res : '+response)
            return jsonify(response=response)
            
        except ValueError:
            return jsonify('error')

if __name__ == '__main__':
    app.run(debug=True, host=LOCALHOST, port=PORT)
