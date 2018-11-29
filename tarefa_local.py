import os
import requests
import json
import sys
import boto3


arg1=sys.argv[1]
arg2=sys.argv[2]

req = requests.get('http://0.0.0.0:5000/Multiplicador/{0}/{1}'.format(int(arg1),int(arg2)))

print (req.text)