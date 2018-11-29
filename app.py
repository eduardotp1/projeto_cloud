from flask import Flask, redirect, url_for, request, Response,jsonify
from flask_restful import Api, Resource
import json

app = Flask(__name__)


class Multiplica:
        def __init__(self,arg1,arg2):
                self.arg1 = arg1
                self.arg2 = arg2

@app.route('/')
def front():
        return "Bem vindo ao Multiplicador, coloque apos a URL /Multiplicador/Primeiro numero/Segundo numero, para multiplicar os numeros" 


@app.route('/Multiplicador/', methods=['GET'])
def multiplica():
        if request.method == 'GET':
                arg1 = json.loads(request.data)["arg1"]
                arg2 = json.loads(request.data)["arg2"]
                resultado=int(arg1)*int(arg2)
                return jsonify({"resultado":resultado})


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
        return Response(status=200)

app.run(host='0.0.0.0', port=5000)