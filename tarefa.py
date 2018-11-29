import os
import requests
import json
import sys
import boto3

ip=''
ec2 = boto3.client('ec2')
existing_instances = ec2.describe_instances()
for i in range(len(existing_instances["Reservations"])):
    if ("Tags" in list(existing_instances["Reservations"][i]["Instances"][0].keys())):
        for tag in (existing_instances["Reservations"][i]["Instances"][0]["Tags"]):
            if(tag["Value"]=="tirta1"):
                ip=existing_instances["Reservations"][i]["Instances"][0]["PublicIpAddress"]



numeros = json.dumps({"arg1":sys.argv[1],"arg2":sys.argv[2]})

headers = {'content-type': 'application/json'}
req = requests.get('http://'+ip+'/Multiplicador/',data=numeros,headers=headers )

print (req.text)