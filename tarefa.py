import os
import requests
import json
import sys


numeros = json.dumps({"arg1":sys.argv[1],"arg2":sys.argv[2]})

headers = {'content-type': 'application/json'}
req = requests.get('http://52.54.237.170:5000/Multiplicador/',data=numeros,headers=headers )

print (req.text)